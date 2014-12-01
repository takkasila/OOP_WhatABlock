import pygame
from pygame.locals import *

class InputManager(object):
	
	Exit = K_ESCAPE

	Top = ord('w')
	Down = ord('s')
	Right = ord('d')
	Left = ord('a')

	Bomb = K_SPACE
	BulletTop = K_UP
	BulletDown = K_DOWN
	BulletRight = K_RIGHT
	BulletLeft = K_LEFT


	TopRFID = 0
	DownRFID = 0
	RightRFID = 0
	LeftRFID = 0
	BombRFID = 0
	BulletTopRFID = 0
	BulletDownRFID = 0
	BulletRightRFID = 0
	BulletLeftRFID = 0

	def __init__(self):
		pass

	def setRFIDInput(self, RFIDReader):
		print 'Set RFID cards for action command following this sequence'
		idList = []
		step = 0

		while len(idList) != 9:
			NoOfId = len(idList)
			if NoOfId == 0 and step == 0:
				print 'WalkTop, WalkDown, WalkRight, WalkLeft'
				step += 1
			elif NoOfId == 4 and step == 1:
				print 'UseBomb'
				step += 1
			elif NoOfId == 5 and step == 2:
				print 'Shoot Bullet: Top, Down, Right, Left'
				step += 1

			inID = RFIDReader.getInput()
			if inID != 9999 and (not inID in idList):
				idList.append(inID)

		InputManager.TopRFID = idList[0]
		InputManager.DownRFID = idList[1]
		InputManager.RightRFID = idList[2]
		InputManager.LeftRFID = idList[3]

		InputManager.BombRFID = idList[4]

		InputManager.BulletTopRFID = idList[5]
		InputManager.BulletDownRFID = idList[6]
		InputManager.BulletRightRFID = idList[7]
		InputManager.BulletLeftRFID = idList[8]

		print 'Success!'

		