# -*- coding: utf-8 -*-
from i2c_hd44780 import i2c_device

import time

CMD_CLEAR			= 0x01
CMD_HOME			= 0x02
CMD_ENTRY_L			= 0x04
CMD_ENTRY_LS		= 0x05
CMD_ENTRY_R			= 0x06
CMD_ENTRY_RS		= 0x07
CMD_DISP_OFF		= 0x08
CMD_DISP_ON			= 0x0C
CMD_CURS_SLD		= 0x0E
CMD_CURS_BLINK		= 0x0F
CMD_SHIFT_CURS_L1	= 0x10
CMD_SHIFT_CURS_R1	= 0x14
CMD_SHIFT_DISP_L1	= 0x18
CMD_SHIFT_DISP_R1	= 0x1C
CMD_4BIT_1L			= 0x20
CMD_4BIT_2L			= 0x28
CMD_8BIT_1L			= 0x30
CMD_8BIT_2L			= 0x38
CMD_CGRAM_ADDR		= 0x40
CMD_DDRAM_ADDR		= 0x80

class lcd:
	'''
	pinout is as follows: PCF8574 - HD44780
	P0 - LCD11 - D4
	P1 - LCD12 - D5
	P2 - LCD13 - D6
	P3 - LCD14 - D7
	P4 - LCD4  - RS
	P5 - LCD5  - R/W
	P6 - LCD6  - EN
	P7 - LCD15 - LED BACKLIGHT (low active)
	'''

	# initializes objects and lcd
	def __init__(self, addr, port, width, height):
		self.width = width
		self.height = height

		self.i2c_device = i2c_device(addr, port)
		self.i2c_device.backlightOn()
		self.i2c_device.write(0x03)
		self.strobe()
		self.strobe()
		self.strobe()
		self.i2c_device.write(0x02)
		self.strobe()

		self.write(CMD_4BIT_2L if height > 1 else CMD_4BIT_1L)
		self.write(CMD_CLEAR)
		self.write(CMD_ENTRY_R)
		self.write(CMD_DISP_ON)

	# clocks EN to latch command
	def strobe(self):
		self.i2c_device.write((self.i2c_device.read() | 0x40))
		self.i2c_device.write((self.i2c_device.read() & 0xBF))
		time.sleep(0.0005)

	# write a command to lcd
	def write(self, cmd):
		self.i2c_device.write(cmd >> 4)
		self.strobe()
		self.i2c_device.write(cmd & 0x0F)
		self.strobe()

	# write a character to lcd (or character ram)
	def write_char(self, charvalue):
		self.i2c_device.write((0x10 | (charvalue >> 4)))
		self.strobe()
		self.i2c_device.write((0x10 | (charvalue & 0x0F)))
		self.strobe()

	# put char function
	def putc(self, char):
		self.write_char(ord(char))

	# put string function where 0 is the first line
	def puts(self, string, y):
		self.write_address(0, y)
		for char in string:
			self.putc(char)

	# clear lcd and set to home
	def clear(self):
		self.write(CMD_CLEAR)
		self.write(CMD_HOME)

	# add custom characters (0 - 7)
	def load_custom_chars(self, fontdata, firstchar=0):
		self.write(CMD_CGRAM_ADDR | (firstchar * 8))
		for char in fontdata:
			for line in char:
				self.write_char(line)

	def load_custom_char(self, char, number):
		self.write(CMD_CGRAM_ADDR | (number * 8))
		for line in char:
			self.write_char(line)

	# set write address to coordinates where (0,0) is the top left edge
	def write_address(self, x, y):
		self.write(CMD_DDRAM_ADDR | (0x14 if y >= 2 else 0x00) | (y * 0x40 + x))