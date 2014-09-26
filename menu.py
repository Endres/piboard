# -*- coding: utf-8 -*-
import main

import math
import time
import types
import threading

#MENU_CHARS = [[0x1F, 0x1A, 0x15, 0x1A, 0x15, 0x1A, 0x15, 0x1F],
#				[0x1F, 0x15, 0x0A, 0x15, 0x0A, 0x15, 0x0A, 0x1F],
#				[0x1F, 0x17, 0x0C, 0x18, 0x08, 0x14, 0x0B, 0x1F],
#				[0x1F, 0x1D, 0x06, 0x03, 0x02, 0x05, 0x1A, 0x1F],
#				[0x1F, 0x15, 0x0B, 0x15, 0x0B, 0x15, 0x0B, 0x1F]]

MENU_CHARS	 = [[0x15, 0x08, 0x04, 0x00, 0x04, 0x08, 0x15, 0x00],
				[0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x15, 0x00],
				[0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14, 0x00],
				[0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00],
				[0x15, 0x02, 0x04, 0x00, 0x04, 0x02, 0x15, 0x00]]

MENU = ("Hauptmen\x05", [
		("Status", main.MODE_STATUS),
		("Netzwerk", [
			("IP-Adresse", main.MODE_NET_IP_ADDR),
			("Netzwerkstatus", main.MODE_NET_STATUS),
			("Verbindung trennen", main.MODE_NET_IFDOWN),
			("Verbinden", main.MODE_NET_IFUP),
			("DHCP-Lease erneuern", main.MODE_NET_DHCPLEASE)]),
		("Sensoren", [
			("Temperatur", main.MODE_SENSOR_TEMP),
			("Luftfeuchtigkeit", main.MODE_SENSOR_HUMID)]),
		("Serieller Port", [
			("T\x05rsummer auf", main.MODE_SERIAL_DOOR),
			("RX-Test", main.MODE_SERIAL_RX),
			("TX-Test", main.MODE_SERIAL_TX)]),
		("Infrarot", [
			("HiFi-Receiver", [
				("Lauter", main.MODE_IR_HIFI_VOL_UP),
				("Leiser", main.MODE_IR_HIFI_VOL_DOWN),
				("Standby", main.MODE_IR_HIFI_STANDBY),
				("Quelle", main.MODE_IR_HIFI_SOURCE)]),
			("Fernbedienung", [
				("Code auslesen", main.MODE_IR_CODE_READ),
				("Code senden", main.MODE_IR_CODE_SEND)])]),
		("Einstellungen", main.MODE_SETTINGS)])
MENU_SEPARATOR = " \xA5 "
MENU_BACK = -1

def getMenuOffset(menulist, item):
	return len(''.join(menulist[0:item])) + len(MENU_SEPARATOR) * (item + 1) - main.lcd_device.width / 2 + len(menulist[item]) / 2
def rotateString(string, count):
	count = count %len(string)
	return (string[len(string)+count:]+string[count:len(string)]+string)[:len(string)]

class menu:
	selectedElement = 0

	def menuSelectCallback(self, pin):
		main.buttons.removeEventSelect()
		while not main.buttons.GetSelectButton():
			self.selectedElement = (self.selectedElement + 1) % len(self.menulist)
			nexti = getMenuOffset(self.menulist, self.selectedElement) % len(self.menustring)

			# acquire locks to keep LCD intact
			self.selectLock.acquire()
			while(self.i != nexti):
				self.i = (self.i + 1) % len(self.menustring)
				main.lcd_device.puts(rotateString(self.menustring, self.i)[:main.lcd_device.width], 1)
			self.selectLock.release()
			if self.selectLock.locked():
				return

			if not main.buttons.GetSelectButton():
				time.sleep(0.3)
		selectIsRunning = False
		main.buttons.addEventSelect(self.menuSelectCallback)

	def __init__(self):
		main.lcd_device.load_custom_chars(MENU_CHARS)
		main.lcd_device.load_custom_char(main.SPECIAL_CHARS['ü'], 5)

		last_menus = [main.MODE_SCREENSAVER]
		print "now last_menus are:", last_menus
		menu = MENU

		self.selectedElement = 1

		while True:
			if hasattr(self, 'selectLock'):
				self.selectLock.release()
			self.selectLock = threading.Lock()
			menu = (menu[0],menu[1] + [("Zur\x05ck" if menu is not MENU else "Screensaver", MENU_BACK)]) # FIXME

			title = menu[0]
			titlestring = "\x00" + ( ('\x01' * int(math.floor((main.lcd_device.width - 4 - len(title)) / 2.0)) + \
				'\x02' + title + '\x03' + \
				'\x01' * int(math.ceil((main.lcd_device.width - 4 - len(title)) / 2.0))) if len(title) else \
				'\x01' * (main.lcd_device.width - 2)) + "\x04"

			main.lcd_device.puts(titlestring[:main.lcd_device.width], 0)
			self.menulist = list((entry if type(entry) is types.StringType else entry[0]) for entry in menu[1])
			self.menustring = MENU_SEPARATOR+MENU_SEPARATOR.join(self.menulist)

			# Scrolling menu displays the active menu item in the center of the screen and scrolls if button is pressed
			self.selectedElement = 0

			self.i = getMenuOffset(self.menulist, self.selectedElement) % len(self.menustring)
			main.lcd_device.puts(rotateString(self.menustring, self.i)[:main.lcd_device.width], 1)

			main.buttons.addEventSelect(self.menuSelectCallback)
			main.buttons.waitConfirmButton()
			main.buttons.removeEventSelect()

			# acquire lock and block if select callback is not yet finished, to keep LCD intact
			self.selectLock.acquire()
			#self.selectLock.release()
			# at this state the LCD can be used again

			main.buttons.removeEventSelect()

			if type(menu[1][self.selectedElement][1]) is types.ListType:
				last_menus.append((menu, self.selectedElement))
				print "now last_menus are: ", last_menus
				menu = menu[1][self.selectedElement]
				self.selectedElement = 1
			elif menu[1][self.selectedElement][1] == MENU_BACK:
				last_menu = last_menus.pop()
				if type(last_menu) is types.TupleType:
					menu = last_menu[0]
					self.selectedElement = last_menu[1] # FIXME
				else:
					# we have no last menu and are done
					return last_menu
			else:
				# we have no submenus and are done.
				return menu[1][self.selectedElement][1]
