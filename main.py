#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lcd_hd44780 import lcd
from gpio_buttons import buttons
import draw

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

class main:
	nointerrupt = True

	def analog_clock(self):
		global lcd_device
		locale.setlocale(locale.LC_TIME, '')
		# store next full minute
		starttime = time.time() - time.time() % 60 + 60
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
		global lcd_device
		lcd_device = lcd(0x20, 1)
		buttons(lcd_device)

		lcd_device.clear()
		self.analog_clock()

if __name__ == '__main__':
    main()
