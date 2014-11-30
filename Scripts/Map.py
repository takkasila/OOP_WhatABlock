from WhatABlock_GameLib import *
from IsoBlock import *

class Map(object):

	isoBlocks = []
	xyBlockList = []
	playerStartPos = 0
	startBlockIso = 0
	finishBlockIso = 0
	worldIndex = 0

	def __init__(self, worldIndex, playerStartPos, blockWidth, blockHeight, startBlockIso, finishBlockIso, xyBlockList = [[]]):
		# generate pattern
		# [
		# [[0,0],[0,1]],
		# [[1,0]]
		# ]
		self.worldIndex = worldIndex
		self.playerStartPos = playerStartPos
		self.xyBlockList = xyBlockList
		self.startBlockIso = startBlockIso
		self.finishBlockIso = finishBlockIso
		self.isoBlocks = []
		for yBlockList in self.xyBlockList:
			for block in yBlockList:
				self.isoBlocks.append(IsoBlock(isoPos = Vector2(block[0], block[1]), width = blockWidth, height = blockHeight))

	def render(self, display, grassBlockImg, startBlockImg, finishBlockImg, camPos, player):
		renderedPlayer = False
		playerIsoPos = player.getTargetPos()

		for block in self.isoBlocks:

			blockPos = [block.getIsoPos().getX(), block.getIsoPos().getY()]
			startPos = [self.startBlockIso.getX(), self.startBlockIso.getY()]
			finishPos = [self.finishBlockIso.getX(), self.finishBlockIso.getY()]
			if blockPos == startPos:
				currentBlockImg = startBlockImg
			elif blockPos == finishPos:
				currentBlockImg = finishBlockImg
			else :
				currentBlockImg = grassBlockImg

			blockX = block.getIsoPos().getX()
			blockY = block.getIsoPos().getY()

			if (renderedPlayer == False):

				if (playerIsoPos.getX() > blockX):		#lower x
					block.render(display = display, image = currentBlockImg, camPos = camPos)

				elif playerIsoPos.getX() == blockX:		# same x
					if playerIsoPos.getY() > blockY:		# lower y
						block.render(display = display, image = currentBlockImg, camPos = camPos)
					elif playerIsoPos.getY() == blockY:		# same y
						block.render(display = display, image = currentBlockImg, camPos = camPos)
						player.render(display, camPos)
						renderedPlayer = True
					elif playerIsoPos.getY() < blockY:		# higher y
						player.render(display, camPos)
						renderedPlayer = True
						block.render(display = display, image = currentBlockImg, camPos = camPos)

				elif playerIsoPos.getX() < blockX:		# higher x
					player.render(display, camPos)
					renderedPlayer = True
					block.render(display = display, image = currentBlockImg, camPos = camPos)
			else:
				block.render(display = display, image = currentBlockImg, camPos = camPos)

		if renderedPlayer == False:
			player.render(display, camPos)
			renderedPlayer = True

		self.resetVisible()

	def resetVisible(self):
		for block in self.isoBlocks:
			block.setVisible(False)

	def getBlocks(self):
		return self.isoBlocks

	def getPlayerStartPos(self):
		return self.playerStartPos

	def get2DBlockList(self):
		return self.xyBlockList

	def getStartBlockIso(self):
		return self.startBlockIso

	def getFinishBlockIso(self):
		return self.finishBlockIso

		