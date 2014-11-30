import pygame
from pygame.locals import *
from WhatABlock_GameLib import *
from IsoBlock import *
from Camera import *
from MapCollection import *
from Player import *
from inputManager import *

import sys
import os

#TODOs :
#	Mark Start and FinishLine block
#	Have different textures for start, normal, finishLine
#	Change between world
#	Make the revelver with radius and centerPosition
class WhatABlockGame(object):

	WINDOW_SIZE = Vector2(1024, 768)
	Clock = 0
	isGameOver = False
	folderDir = ''
	assetDir = ''
	bgImage = ''
	cam = ''
	mapCollection = ''
	player = ''
	inputManager = ''


	def __init__(self, WINDOW_SIZE):

		self.WINDOW_SIZE = WINDOW_SIZE
		self.isGameOver = False
		self.folderDir = os.path.split(os.getcwd())[0]
		self.assetDir = self.folderDir + '/Assets/'

		pygame.init()
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((WINDOW_SIZE.getX(), WINDOW_SIZE.getY()))
		pygame.display.set_caption('What A Block')

		self.loadAssets()
		
		self.cam = Camera(offSet = Vector2(WINDOW_SIZE.getX()/2 , WINDOW_SIZE.getY()/2 - self.player.getHeight()/2), camSize = WINDOW_SIZE)

		self.inputManager = InputManage()

	def loadAssets(self):
		
		self.mapCollection = MapCollection(currentMap = 2, assetDir = self.assetDir, WINDOW_SIZE = self.WINDOW_SIZE)
		self.player = Player(self.mapCollection.getCurrentMapObject().getPlayerStartPos(), assetDir = self.assetDir, blockWidth = self.mapCollection.getBlockSize().getX(), blockHeight = self.mapCollection.getBlockSize().getY(), moveSpeed = 0.1)


	def render(self):

		#sent player into map for order of rendering purpose
		self.mapCollection.renderCurrentMap(self.display, camPos = self.cam.getPos(), player = self.player) 

		pygame.display.flip()

	def update(self):
		self.inputs()
		self.player.update()
		self.checkPlayerFall()
		self.checkPlayerFallOut()
		self.checkChangeWorld()

		self.cam.update(playerPos = self.player.getScreenPos())

	def checkPlayerFall(self):
		playerIsoPos = self.player.getIsoPos()
		playerIsoPos = [playerIsoPos.getX(), playerIsoPos.getY()]
		for blockLists in self.mapCollection.getCurrentMapObject().get2DBlockList():
			if playerIsoPos in blockLists:
				self.player.setFall(False)
				self.player.setMoveAble(True)
				return
		self.player.setFall(True)
		self.player.clearActionQueue()
		self.player.setMoveAble(False)

	def checkPlayerFallOut(self):
		if self.player.getTall() < -self.WINDOW_SIZE.getY()/2:
			self.player.setTall(0)
			self.player.setFall(False)
			self.player.setIsoPos(self.mapCollection.getCurrentMapObject().getPlayerStartPos())
			self.player.setMoveAble(True)

	def checkChangeWorld(self):
		playerPos = self.player.getIso()
		playerPos = [playerPos.getX(), playerPos.getY()]
		finishBlockPos = self.mapCollection.getCurrentMapObject().getFinishBlockIso()
		finishBlockPos = [finishBlockPos.getX(), finishBlockPos.getY()]
		if playerPos == finishBlockPos:
			self.mapCollection.setCurrentMapIndex(self.mapCollection.getCurrentMapIndex() + 1)


	def inputs(self):

		for event in pygame.event.get():

			if (event.type == QUIT): 
				self.isGameOver = True

			if (event.type == KEYDOWN ) and (self.player.isMoveAble()):

				if event.key == self.inputManager.Exit:
					self.isGameOver = True

				if event.key == self.inputManager.Top:
					self.player.actionQueue.append(Player.WalkTopCM)

				if event.key == self.inputManager.Down:
					self.player.actionQueue.append(Player.WalkDownCM)

				if event.key == self.inputManager.Right:
					self.player.actionQueue.append(Player.WalkRightCM)
					
				if event.key == self.inputManager.Left:
					self.player.actionQueue.append(Player.WalkLeftCM)

def main():

	game = WhatABlockGame(Vector2(1024, 768))


	while not game.isGameOver:

		game.render()

		game.update()
		

if __name__=='__main__':
    main()
    pygame.quit()