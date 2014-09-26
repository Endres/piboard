# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

SELECT = 27
CONFIRM = 18

class buttons:
	busy = False
	selectEdge = 0

	def __init__(self, lcd_device):
		self.lcd_device = lcd_device
		# set up BCM GPIO numbering
		GPIO.setmode(GPIO.BCM)
		# set buttons as input
		GPIO.setup(SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(CONFIRM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		# initialize event callbacks / interrupts
		#self.addEventSelect()
		#self.addEventConfirm()

	def addEventSelect(self, callback=None):
		if callback == None:
			callback = self.SelectButtonCallback
		GPIO.add_event_detect(SELECT, GPIO.BOTH, callback=callback, bouncetime=100)

	def addEventConfirm(self):
		GPIO.add_event_detect(CONFIRM, GPIO.BOTH, callback=self.ConfirmButtonCallback, bouncetime=100)

	def removeEventSelect(self):
		GPIO.remove_event_detect(SELECT)

	def removeEventConfirm(self):
		GPIO.remove_event_detect(CONFIRM)

	def SelectButtonCallback(self, pin):
		if self.busy:
			return
		# busy while operating
		self.busy = True

		self.lcd_device.write_address(14,1)
		if not GPIO.input(pin):
			print "Button pressed " + str(pin)
			self.lcd_device.putc('\xdb')
			self.selectEdge = 1
		else:
			print "Button released " + str(pin)
			self.lcd_device.putc('\x20')
			self.selectEdge = 0

		# disabling busy state
		self.busy = False

	def ConfirmButtonCallback(self, pin):
		if self.busy:
			return
		# busy while operating
		self.busy = True

		#self.lcd_device.write_address(15,1)
		if not GPIO.input(pin):
			print "Button pressed " + str(pin)
			#self.lcd_device.putc('\xdb')
		else:
			print "Button released " + str(pin)
			#self.lcd_device.putc('\x20')

		# disabling busy state
		self.busy = False

	def GetSelectButton(self):
		return GPIO.input(SELECT)

	def GetConfirmButton(self):
		return GPIO.input(CONFIRM)

	def waitSelectButton(self):
		self.removeEventSelect()
		if self.selectEdge:
			time.sleep(0.3)
			if not GPIO.input(SELECT):
				return
			else:
				self.selectEdge = 0
		GPIO.wait_for_edge(SELECT, GPIO.FALLING)
		self.selectEdge = 1
		self.addEventSelect()

	def waitConfirmButton(self):
		self.removeEventConfirm()
		GPIO.wait_for_edge(CONFIRM, GPIO.FALLING)
		self.addEventConfirm()