# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

SELECT = 27
CONFIRM = 18

class buttons:
	busy = False

	def __init__(self, lcd_device):
		self.lcd_device = lcd_device
		# set up BCM GPIO numbering
		GPIO.setmode(GPIO.BCM)
		# set buttons as input
		GPIO.setup(SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(CONFIRM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		# initialize event callbacks / interrupts
		GPIO.add_event_detect(SELECT, GPIO.BOTH, callback=self.SelectButtonCallback, bouncetime=100)
		GPIO.add_event_detect(CONFIRM, GPIO.BOTH, callback=self.ConfirmButtonCallback, bouncetime=100)

	def SelectButtonCallback(self, pin):
		if self.busy:
			return
		# busy while operating
		self.busy = True

		self.lcd_device.write_address(14,1)
		if not GPIO.input(pin):
			print "Button pressed " + str(pin)
			self.lcd_device.putc('\xdb')
		else:
			print "Button released " + str(pin)
			self.lcd_device.putc('\x20')

		# disabling busy state
		self.busy = False

	def ConfirmButtonCallback(self, pin):
		if self.busy:
			return
		# busy while operating
		self.busy = True

		self.lcd_device.write_address(15,1)
		if not GPIO.input(pin):
			print "Button pressed " + str(pin)
			self.lcd_device.putc('\xdb')
		else:
			print "Button released " + str(pin)
			self.lcd_device.putc('\x20')

		# disabling busy state
		self.busy = False

	def GetSelectButton(self):
		return GPIO.input(SELECT)

	def GetConfirmButton(self):
		return GPIO.input(CONFIRM)