# -*- coding: utf-8 -*-
import main

import math
import time
import types
from threading import Thread

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

MENU = [("Status"),
		("Netzwerk", [
			("IP-Adresse"),
			("Netzwerkstatus"),
			("Verbindung trennen"),
			("Verbinden"),
			("DHCP-Lease erneuern")]),
		("Sensoren", [
			("Temperatur"),
			("Luftfeuchtigkeit")]),
		("Serieller Port", [
			("Türsummer auf"),
			("RX-Test"),
			("TX-Test")]),
		("Infrarot", [
			("HiFi-Receiver", [
				("Lauter"),
				("Leiser"),
				("Standby"),
				("Quelle")]),
			("Fernbedienung", [
				("Code auslesen"),
				("Code senden")])]),
		("Einstellungen")]
MENU_SEPARATOR = " \xA5 "

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

			while(self.i != nexti):
				self.i = (self.i + 1) % len(self.menustring)
				main.lcd_device.puts(rotateString(self.menustring, self.i)[:main.lcd_device.width], 1)

			if not main.buttons.GetSelectButton():
				time.sleep(0.3)
		main.buttons.addEventSelect(self.menuSelectCallback)

	def __init__(self):
		main.lcd_device.load_custom_chars(MENU_CHARS)
		main.lcd_device.load_custom_char(main.SPECIAL_CHARS['ü'], 5)
		title = "Hauptmen\x05"
		titlestring = "\x00" + ( ('\x01' * int(math.floor((main.lcd_device.width - 4 - len(title)) / 2.0)) + \
			'\x02' + title + '\x03' + \
			'\x01' * int(math.ceil((main.lcd_device.width - 4 - len(title)) / 2.0))) if len(title) else \
			'\x01' * (main.lcd_device.width - 2)) + "\x04"

		main.lcd_device.puts(titlestring[:main.lcd_device.width], 0)
		self.menulist = list((entry if type(entry) is types.StringType else entry[0]) for entry in MENU)
		self.menustring = MENU_SEPARATOR+MENU_SEPARATOR.join(self.menulist)

		# Scrolling menu displays the active menu item in the center of the screen and scrolls if button is pressed
		self.selectedElement = 0

		self.i = getMenuOffset(self.menulist, self.selectedElement) % len(self.menustring)
		main.lcd_device.puts(rotateString(self.menustring, self.i)[:main.lcd_device.width], 1)

		main.buttons.addEventSelect(self.menuSelectCallback)
		main.buttons.waitConfirmButton()
		main.buttons.removeEventSelect()
		print "Finished, yay, we selected m=%d" % self.selectedElement