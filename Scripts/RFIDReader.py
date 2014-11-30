from practicum import findDevices
from peri import PeriBoard
from time import sleep

class RFIDReader(object):

	board = ''


	def __init__(self):
		
		devs = findDevices()

		if len(devs) == 0:
		    print "*** No MCU board found."
		    exit(1)
		
		self.board = PeriBoard(devs[0])
		self.continueZeroCounter = 0
		self.maxContinueZeroCounter = 30
		self.sendAble = True

	def getInput(self):
		#return id of card, or 9999 if no input
		inRFID = self.board.getRFID()[0]

		if self.sendAble:
			if inRFID == 0:
				return 9999
			else:
				self.sendAble = False
				self.continueZeroCounter = 0
				return inRFID
		else:
			if self.continueZeroCounter < self.maxContinueZeroCounter:
				self.continueZeroCounter += 1
				return 9999
			elif self.continueZeroCounter >= self.maxContinueZeroCounter:
				self.continueZeroCounter = self.maxContinueZeroCounter
				self.sendAble = True
				return 9999
