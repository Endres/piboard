#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lcd_hd44780 import lcd
import gpio_buttons
import draw
import menu

import time
import datetime
import locale
import copy
import math

CIRCLE_CHARS = [[0x00, 0x01, 0x02, 0x04, 0x08, 0x08, 0x10, 0x10],
				[0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
				[0x00, 0x10, 0x08, 0x04, 0x02, 0x02, 0x01, 0x01],
				[0x10, 0x10, 0x08, 0x08, 0x04, 0x02, 0x01, 0x00],
				[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F],
				[0x01, 0x01, 0x02, 0x02, 0x04, 0x08, 0x10, 0x00]]

SPECIAL_CHARS = {'ü': [0x0A, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D, 0x00]}

MODE_MENU			= 1
MODE_SCREENSAVER	= 2
MODE_STATUS			= 3
MODE_NET_IP_ADDR	= 4
MODE_NET_STATUS		= 5
MODE_NET_IFDOWN		= 6
MODE_NET_IFUP		= 7
MODE_NET_DHCPLEASE	= 8
MODE_SENSOR_TEMP	= 9
MODE_SENSOR_HUMID	= 10
MODE_SERIAL_DOOR	= 11
MODE_SERIAL_RX		= 12
MODE_SERIAL_TX		= 13
MODE_IR_HIFI_VOL_UP	= 14
MODE_IR_HIFI_VOL_DOWN	= 15
MODE_IR_HIFI_STANDBY	= 16
MODE_IR_HIFI_SOURCE		= 17
MODE_IR_CODE_READ		= 18
MODE_IR_CODE_SEND		= 19
MODE_SETTINGS			= 20

lcd_device = lcd(0x20, 1, 16, 2)
buttons = gpio_buttons.buttons(lcd_device)

class main:
	nointerrupt = True
	mode = MODE_MENU

	SPECIAL_CHARS = {'ü': [0x0A, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D, 0x00]}

	def analog_clock(self):
		locale.setlocale(locale.LC_TIME, '')
		# store next full minute
		starttime = time.time() - time.time() % 60 + 60
		lcd_device.clear()
		while self.nointerrupt:
			t = datetime.datetime.now()
			clockcircle = copy.deepcopy(CIRCLE_CHARS)
			draw.draw_dots(clockcircle, draw.get_line(8, 8, \
				int(round(math.cos(((9 + t.hour + t.minute / 60.0) % 12) / 12.0 * 2 * math.pi + 0.00) * 4 + 8)), \
				int(round(math.sin(((9 + t.hour + t.minute / 60.0) % 12) / 12.0 * 2 * math.pi + 0.00) * 4 + 8))))
			draw.draw_dots(clockcircle, draw.get_line(8, 8, \
				int(round(math.cos(((45 + t.minute) % 60) / 60.0 * 2 * math.pi + 0.00) * 8 + 8)), \
				int(round(math.sin(((45 + t.minute) % 60) / 60.0 * 2 * math.pi + 0.00) * 8 + 8))))
			lcd_device.load_custom_chars(clockcircle)

			lcd_device.puts("\x00\x01\x02 "+t.strftime("%x"), 0)
			lcd_device.puts("\x03\x04\x05 "+t.strftime("  %H:%M"), 1)
			print "loop took %f ms" % ((time.time() - starttime) % 1.0 * 1000)
			time.sleep(60.0 - ((time.time() - starttime) % 60.0))

	def __init__(self) :
		while(True):
			self.setMode(MODE_MENU)
			#if()

	def setMode(self, mode):
		self.mode = mode
		if mode == MODE_MENU:
			print "Menu returned: " + menu.menu()
		elif mode == MODE_SCREENSAVER:
			self.analog_clock()

if __name__ == '__main__':
	main()