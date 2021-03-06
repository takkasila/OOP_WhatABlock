import pygame
from pygame.locals import *
from WhatABlock_GameLib import *
from Map import *

currentMap = 0
blockWidth = 0
blockHeight = 0
mapList = []
WINDOW_SIZE = 0

assetDir = ''
bgImage = ''
bgRectOnScreen = ''
isoGrassBlockImg = ''
isoStartBlockImg = ''
isoFinishBlockImg = ''
isoTopBlockImage = ''


class MapCollection(object):

	def __init__(self, currentMap, assetDir, WINDOW_SIZE):
		self.currentMap = currentMap
		self.WINDOW_SIZE = WINDOW_SIZE

		self.assetDir = assetDir
		self.loadAsset()

		map1xyBlockList = [
		[[0,0],[0,1],[0,2],[0,3],[0,4]],
		[[1,0]		,[1,2],[1,3],[1,4]],
		[[2,0],[2,1],[2,2],[2,3],[2,4]],
		[[3,0],[3,1],[3,2],[3,3],[3,4]],
		[[4,0],[4,1],[4,2],[4,3],[4,4]]
		]

		map2xyBlockList = [
		[[0,4]],
		[[1,0],[1,1],[1,2],[1,3],[1,4],[1,5]],
		[[2,5]],
		[[3,5]],
		[[4,4],[4,5]],
		[[5,4]],
		[[6,4]],
		[[7,4]]
		]

		map3xyBlockList = [
		[[0,0],[0,1],[0,2],[0,3],[0,4]],
		[[1,0]		,[1,2],[1,3],[1,4]],
		[[2,0],[2,1],[2,2],[2,3],[2,4]],
		[[3,0],[3,1]	  ,[3,3],[3,4]],
		[[4,0],[4,1],[4,2],[4,3],[4,4]],
		[[5,0],[5,1],[5,2]      ,[5,4]],
		[[6,0],[6,1],[6,2],[6,3],[6,4]],
		[[7,0],[7,1],[7,2],[7,3],[7,4]],
		]

		map4xyBlockList = [
		[[0,0],[1,0],[2,0],[3,0],[4,0]],
		[[4,1]],
		[[4,2],[5,2],[6,2]],
		[[6,3]],
		[[5,4],[6,4],[7,4],[8,4],[9,4],[10,4]],
		[[6,5]]
		]

		Map1 = Map(worldIndex = 0, playerStartPos = Vector2(0,0), blockWidth = self.blockWidth, blockHeight = self.blockHeight
			,startBlockIso = Vector2(0,0), finishBlockIso = Vector2(4,4), xyBlockList= map1xyBlockList)
		
		Map2 = Map(worldIndex = 1, playerStartPos = Vector2(1,0), blockWidth = self.blockWidth, blockHeight = self.blockHeight
			,startBlockIso = Vector2(1,0), finishBlockIso = Vector2(7,4), xyBlockList= map2xyBlockList)

		Map3 = Map(worldIndex = 2, playerStartPos = Vector2(7,0), blockWidth = self.blockWidth, blockHeight = self.blockHeight
			,startBlockIso = Vector2(7,0), finishBlockIso = Vector2(0,4), xyBlockList= map3xyBlockList)

		Map4 = Map(worldIndex = 3, playerStartPos = Vector2(10,4), blockWidth = self.blockWidth, blockHeight = self.blockHeight
			,startBlockIso = Vector2(10,4), finishBlockIso = Vector2(0,0), xyBlockList= map4xyBlockList)
		self.mapList = []
		self.mapList.append(Map1)
		self.mapList.append(Map2)
		self.mapList.append(Map3)
		self.mapList.append(Map4)

	def loadAsset(self):

		self.bgImage = pygame.image.load(self.assetDir + 'bg2.jpg').convert()
		self.bgRectOnScreen = self.bgImage.get_rect()
		self.bgRectOnScreen.left -= ( self.bgRectOnScreen.width - self.WINDOW_SIZE.getX() )/2 # shift to middle of screen

		self.isoGrassBlockImg = pygame.image.load(self.assetDir + 'grass-covered-dirt-block-full.png')
		self.isoStartBlockImg = pygame.image.load(self.assetDir + 'concrete-covered-dirt-block.png')
		self.isoFinishBlockImg = pygame.image.load(self.assetDir + 'black-block.png')
		self.isoTopBlockImage = pygame.image.load(self.assetDir + 'concrete-covered-dirt-blockTop.png')
		self.blockWidth = self.isoGrassBlockImg.get_rect().width
		self.blockHeight = self.isoTopBlockImage.get_rect().height

	def renderCurrentMap(self, display, camPos, player):

		display.blit(self.bgImage, self.bgRectOnScreen)

		self.mapList[self.currentMap].render(display = display, grassBlockImg = self.isoGrassBlockImg
			, startBlockImg = self.isoStartBlockImg, finishBlockImg = self.isoFinishBlockImg, camPos = camPos, player = player)

	def getCurrentMapObject(self):
		return self.mapList[self.currentMap]

	def getCurrentMapIndex(self):
		return self.currentMap

	def setCurrentMapIndex(self, currentMapIndex):
		self.currentMap = currentMapIndex

	def getBlockSize(self):
		return Vector2(self.blockWidth, self.blockHeight)



