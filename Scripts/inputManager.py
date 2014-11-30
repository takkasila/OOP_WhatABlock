import pygame
from pygame.locals import *

class InputManager(object):
	
	Top = ord('w')
	Down = ord('s')
	Right = ord('d')
	Left = ord('a')
	Exit = K_ESCAPE 

	TopRFID = 0
	DownRFID = 0
	RightRFID = 0
	LeftRFID = 0

	def __init__(self):
		pass

	def setRFIDInput(self, RFIDReader):
		print 'Set RFID cards for action command following this sequence'
		print 'WalkTop, WalkDown, WalkRight, WalkLeft'
		idList = []

		while len(idList) != 4:
			inID = RFIDReader.getInput()
			if inID != 9999 and (not inID in idList):
				idList.append(inID)

		InputManager.TopRFID = idList[0]
		InputManager.DownRFID = idList[1]
		InputManager.RightRFID = idList[2]
		InputManager.LeftRFID = idList[3]

		print 'Success!'

		