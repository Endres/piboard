# -*- coding: utf-8 -*-
import smbus

ON = 1
OFF = 0

class i2c_device:
	lastWritten = 0x00

	def __init__(self, addr, port):
		self.backlight = ON
		self.addr = addr
		self.bus = smbus.SMBus(port)

	def write(self, byte):
		if self.backlight:
			# switch on backlight LED
			byte = byte & 0x7F
		else:
			# switch off backlight LED
			byte = byte | 0x80

		#print "writing 0x%02x" % byte
		self.bus.write_byte(self.addr, byte)
		self.lastWritten = byte

	def read(self):
		return self.lastWritten
		#return self.bus.read_byte(self.addr)

	def backlightOn(self):
		self.backlightSet(ON)

	def backlightOff(self):
		self.backlightSet(OFF)

	def backlightSet(self, status):
		self.backlight = status
		self.write(0x00)