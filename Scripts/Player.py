from WhatABlock_GameLib import *
import pygame
from pygame.locals import *
from BomRevealer import *
from MovingRevealer import *

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

	UseBombCM = 'uBomb'
	UseBulletTopCM = 'uBulletTop'
	UseBulletDownCM = 'uBulletDown'
	UseBulletRightCM = 'uBulletRight'
	UseBulletLeftCM = 'uBulletLeft'

	isWalking = False
	moveSpeed = 0
	moveAble = True

	actionQueue = []

	revealerList = []
	bomb = 1
	bullet = 3
	BulletRadius = 60
	BulletLifeTime = 300
	BulletSpeed = 1

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

		self.revealerList = []
		self.bomb = 1



	def render(self, display, camPos):

		renderRect = pygame.Rect( self.screenPos.getX() - camPos.getX()
			, self.screenPos.getY() - camPos.getY() - self.tall, self.width, self.height)
		renderRect.top += self.blockHeight/2 - self.height
		renderRect.left -= self.width/2
		display.blit(self.playerImage, renderRect)

	def update(self, isoBlocks):
		if self.actionQueue:
			if self.actionQueue[0] == Player.WalkTopCM :
				self.walkTop()
			elif self.actionQueue[0] == Player.WalkDownCM :
				self.walkDown()
			elif self.actionQueue[0] == Player.WalkRightCM :
				self.walkRight()
			elif self.actionQueue[0] == Player.WalkLeftCM :
				self.walkLeft()

			elif self.actionQueue[0] == Player.UseBombCM :
				self.useBomb()
			elif self.actionQueue[0] == Player.UseBulletTopCM :
				self.useBulletTop()
			elif self.actionQueue[0] == Player.UseBulletDownCM :
				self.useBulletDown()
			elif self.actionQueue[0] == Player.UseBulletRightCM :
				self.useBulletRight()
			elif self.actionQueue[0] == Player.UseBulletLeftCM :
				self.useBulletLeft()


		if self.fall:
			self.tall -= self.fallSpeed

		self.revealerUpdate(isoBlocks)

	def revealerUpdate(self, isoBlocks):

		deadList = []
		if self.revealerList:
			for i in range(len(self.revealerList)):
				if self.revealerList[i].isAlive():
					self.revealerList[i].reveal(isoBlocks)
				else:
					deadList.append(i)
			while deadList:
				self.revealerList.pop(deadList[len(deadList) - 1])
				deadList.pop(len(deadList) - 1)

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

	def useBomb(self):					#BOMB

		if self.bomb > 0:
			self.bomb -= 1
			self.revealerList.append(BomRevealer(self.screenPos , 300, 1.5))
			self.actionQueue.pop(0)

	def useBulletTop(self):				#Bullet_Top

		if self.bullet > 0:
			self.bullet -= 1
			self.revealerList.append(MovingRevealer(self.screenPos, Player.BulletRadius
				, Vector2(Player.BulletSpeed * getCos30(), Player.BulletSpeed * getSin30() *-1), Player.BulletLifeTime))
			self.actionQueue.pop(0)

	def useBulletDown(self):				#Bullet_Down

		if self.bullet > 0:
			self.bullet -= 1
			self.revealerList.append(MovingRevealer(self.screenPos, Player.BulletRadius
				, Vector2(Player.BulletSpeed * getCos30() *-1 , Player.BulletSpeed * getSin30()), Player.BulletLifeTime))
			self.actionQueue.pop(0)

	def useBulletRight(self):				#Bullet_Right

		if self.bullet > 0:
			self.bullet -= 1
			self.revealerList.append(MovingRevealer(self.screenPos, Player.BulletRadius
				, Vector2(Player.BulletSpeed * getCos30(), Player.BulletSpeed * getSin30()), Player.BulletLifeTime))
			self.actionQueue.pop(0)

	def useBulletLeft(self):				#Bullet_Left

		if self.bullet > 0:
			self.bullet -= 1
			self.revealerList.append(MovingRevealer(self.screenPos, Player.BulletRadius
				, Vector2(Player.BulletSpeed * getCos30() *-1, Player.BulletSpeed * getSin30() *-1), Player.BulletLifeTime))
			self.actionQueue.pop(0)




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

	def getBomb(self):
		return self.bomb

	def setBomb(self, n):
		self.bomb = n

	def getBullet(self):
		return self.bullet

	def setBullet(self, n):
		self.bullet = n



