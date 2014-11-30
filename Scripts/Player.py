from WhatABlock_GameLib import *
import pygame
from pygame.locals import *

class Player(object):

	isoPos = Vector2(0, 0)
	screenPos = Vector2(0, 0)
	width = 0
	height = 0
	tall = 0
	playerImage = ''
	blockWidth = 0
	blockHeight = 0
	renderRect = 0

	WalkTopCM = 'wTop'
	WalkDownCM = 'wDown'
	WalkRightCM = 'wRight'
	WalkLeftCM = 'wLeft'
	isWalking = False
	moveSpeed = 0
	moveAble = True

	actionQueue = []

	def __init__(self, startIsoPos, assetDir, blockWidth, blockHeight, moveSpeed):
		#movespeed is percentage of lerp. Scale from 0 to 1

		self.isoPos = startIsoPos

		self.playerImage = pygame.image.load(assetDir + 'player.png')

		self.width = self.playerImage.get_rect().width
		self.height = self.playerImage.get_rect().height
		self.tall = 0

		self.blockWidth = blockWidth
		self.blockHeight = blockHeight
		self.screenPos = IsoToScreen(self.isoPos, self.blockWidth, self.blockHeight)

		self.walkTop_start = False
		self.walkDown_start = False
		self.walkRight_start = False
		self.walkLeft_start = False
		self.isWalking = False
		self.moveAble = True
		self.fall = False
		self.fallSpeed = 4

		self.moveSpeed = moveSpeed

		self.targetIsoPos = self.isoPos
		self.targetScreenPos = self.screenPos



	def render(self, display, camPos):

		renderRect = pygame.Rect( self.screenPos.getX() - camPos.getX()
			, self.screenPos.getY() - camPos.getY() - self.tall, self.width, self.height)
		renderRect.top += self.blockHeight/2 - self.height
		renderRect.left -= self.width/2
		display.blit(self.playerImage, renderRect)

	def update(self):
		if self.actionQueue:
			if self.actionQueue[0] == Player.WalkTopCM :
				self.walkTop()
			elif self.actionQueue[0] == Player.WalkDownCM :
				self.walkDown()
			elif self.actionQueue[0] == Player.WalkRightCM :
				self.walkRight()
			elif self.actionQueue[0] == Player.WalkLeftCM :
				self.walkLeft()
		if self.fall:
			self.tall -= self.fallSpeed

	def walkTop(self):					#TOP
		if not self.walkTop_start:

			self.walkTop_start = True
			self.__startMove(0, -1)
		
		else:
			self.screenPos = Vector2.Lerp(self.screenPos, self.targetScreenPos, self.moveSpeed)

			cond1 = (self.screenPos.getX() >= self.targetScreenPos.getX())
			cond2 = (self.screenPos.getY() <= self.targetScreenPos.getY())
			if cond1 and cond2: #made it to the point
				self.actionQueue.pop(0)
				self.walkTop_start = False
				self.isoPos = self.targetIsoPos


	def walkDown(self):					#DOWN
		if not self.walkDown_start:

			self.walkDown_start = True
			self.__startMove(0, 1)

		else:
			self.screenPos = Vector2.Lerp(self.screenPos, self.targetScreenPos, self.moveSpeed)

			cond1 = (self.screenPos.getX() <= self.targetScreenPos.getX())
			cond2 = (self.screenPos.getY() >= self.targetScreenPos.getY())
			if cond1 and cond2:
				self.actionQueue.pop(0)
				self.walkDown_start = False
				self.isoPos = self.targetIsoPos


	def walkRight(self):				#Right
		if not self.walkRight_start:

			self.walkRight_start = True
			self.__startMove(1, 0)

		else:
			self.screenPos = Vector2.Lerp(self.screenPos, self.targetScreenPos, self.moveSpeed)

			cond1 = (self.screenPos.getX() >= self.targetScreenPos.getX())
			cond2 = (self.screenPos.getY() >= self.targetScreenPos.getY())
			if cond1 and cond2:
				self.actionQueue.pop(0)
				self.walkRight_start = False
				self.isoPos = self.targetIsoPos


	def walkLeft(self):					#Left
		if not self.walkLeft_start:

			self.walkLeft_start = True
			self.__startMove(-1, 0)

		else:
			self.screenPos = Vector2.Lerp(self.screenPos, self.targetScreenPos, self.moveSpeed)

			cond1 = (self.screenPos.getX() <= self.targetScreenPos.getX())
			cond2 = (self.screenPos.getY() <= self.targetScreenPos.getY())
			if cond1 and cond2:
				self.actionQueue.pop(0)
				self.walkLeft_start = False
				self.isoPos = self.targetIsoPos


	def __startMove(self, x, y): #Utility

		self.targetIsoPos = Vector2(self.isoPos.getX() + x, self.isoPos.getY() + y)
		self.targetScreenPos = IsoToScreen(self.targetIsoPos, self.blockWidth, self.blockHeight) 
		self.screenPos = Vector2.Lerp(self.screenPos, self.targetScreenPos, self.moveSpeed)

	def getIsoPos(self):
		return self.isoPos

	def setIsoPos(self, inIsoPos):
		self.isoPos = inIsoPos
		self.screenPos = IsoToScreen(self.isoPos, self.blockWidth, self.blockHeight)
		self.targetIsoPos = self.isoPos

	def isFall(self):
		return self.fall

	def setFall(self, fall):
		self.fall = fall

	def getTall(self):
		return self.tall

	def setTall(self, tall):
		self.tall = tall

	def isMoveAble(self):
		return self.moveAble

	def setMoveAble(self, moveAble):
		self.moveAble = moveAble

	def getScreenPos(self):
		return self.screenPos

	def getTargetPos(self):
		return self.targetIsoPos

	def clearActionQueue(self):
		self.actionQueue = []

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height



