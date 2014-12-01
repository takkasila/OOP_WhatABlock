import pygame
from pygame.locals import *
from WhatABlock_GameLib import *
from IsoBlock import *
from Camera import *
from MapCollection import *
from Player import *
from inputManager import *
from RFIDReader import *
from Revealer import *

import sys
import os

#TODOs :
#	Revealers should be manage life with player
#	Add firing-type revealer
#	Config overall control
#	Add walking sound
# 	Add BG sound
#	Add teleporting sound(change to new level)
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
	myRFIDReader = ''
	player_revealver = ''


	def __init__(self, WINDOW_SIZE):

		self.WINDOW_SIZE = WINDOW_SIZE
		self.isGameOver = False
		self.playWithRFID = True

		self.folderDir = os.path.split(os.getcwd())[0]
		self.assetDir = self.folderDir + '/Assets/'

		pygame.init()
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((WINDOW_SIZE.getX(), WINDOW_SIZE.getY()))
		pygame.display.set_caption('What A Block')

		self.loadAssets()
		
		self.cam = Camera(offSet = Vector2(WINDOW_SIZE.getX()/2 , WINDOW_SIZE.getY()/2 - self.player.getHeight()/2), camSize = WINDOW_SIZE)

		self.inputManager = InputManager()
		if self.playWithRFID:
			self.myRFIDReader = RFIDReader()
			self.inputManager.setRFIDInput(self.myRFIDReader)

		self.player_revealver = Revealer(IsoToScreen(self.player.getIsoPos(), self.mapCollection.getBlockSize().getX(), self.mapCollection.getBlockSize().getY()), 60)

	def loadAssets(self):
		
		self.mapCollection = MapCollection(currentMap = 0, assetDir = self.assetDir, WINDOW_SIZE = self.WINDOW_SIZE)
		self.player = Player(self.mapCollection.getCurrentMapObject().getPlayerStartPos(), assetDir = self.assetDir, blockWidth = self.mapCollection.getBlockSize().getX(), blockHeight = self.mapCollection.getBlockSize().getY(), moveSpeed = 0.1)


	def render(self):

		#sent player into map for order of rendering purpose
		self.mapCollection.renderCurrentMap(self.display, camPos = self.cam.getPos(), player = self.player) 

		pygame.display.flip()

	def update(self):

		self.inputs()

		self.player.update(isoBlocks = self.mapCollection.getCurrentMapObject().getBlocks())

		self.player_revealver.setPos(self.player.getScreenPos())
		self.player_revealver.reveal(isoBlocks = self.mapCollection.getCurrentMapObject().getBlocks())

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
		playerPos = self.player.getIsoPos()
		playerPos = [playerPos.getX(), playerPos.getY()]
		finishBlockPos = self.mapCollection.getCurrentMapObject().getFinishBlockIso()
		finishBlockPos = [finishBlockPos.getX(), finishBlockPos.getY()]
		if playerPos == finishBlockPos:
			self.mapCollection.setCurrentMapIndex(self.mapCollection.getCurrentMapIndex() + 1)
			startPos = self.mapCollection.getCurrentMapObject().getStartBlockIso()
			self.player.setIsoPos(startPos)
			self.player.setBomb(self.player.getBomb() + 1)
			self.player.setBullet(self.player.getBullet() + 3)


	def inputs(self):
		if self.playWithRFID:
			inRFID = self.myRFIDReader.getInput()
			if inRFID != 9999:
				self.controlPlayerByRFID(inRFID)
			else :
				self.controlPlayerByKeyboard()
		else :
			self.controlPlayerByKeyboard()
			

	def controlPlayerByRFID(self, id):

		if id == InputManager.TopRFID:
			self.player.actionQueue.append(Player.WalkTopCM)

		if id == InputManager.DownRFID:
			self.player.actionQueue.append(Player.WalkDownCM)

		if id == InputManager.RightRFID:
			self.player.actionQueue.append(Player.WalkRightCM)

		if id == InputManager.LeftRFID:
			self.player.actionQueue.append(Player.WalkLeftCM)

		if id == InputManager.BombRFID:
			self.player.actionQueue.append(Player.UseBombCM)

		if id == InputManager.BulletTopRFID:
			self.player.actionQueue.append(Player.UseBulletTopCM)

		if id == InputManager.BulletDownRFID:
			self.player.actionQueue.append(Player.UseBulletDownCM)

		if id == InputManager.BulletRightRFID:
			self.player.actionQueue.append(Player.UseBulletRightCM)

		if id == InputManager.BulletLeftRFID:
			self.player.actionQueue.append(Player.UseBulletLeftCM)



	def controlPlayerByKeyboard(self):
		for event in pygame.event.get():
			if (event.type == QUIT): 
				self.isGameOver = True

			if self.player.isMoveAble() and event.type == KEYDOWN:

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

				if event.key == self.inputManager.Bomb:
					self.player.actionQueue.append(Player.UseBombCM)

				if event.key == self.inputManager.BulletTop:
					self.player.actionQueue.append(Player.UseBulletTopCM)
				
				if event.key == self.inputManager.BulletDown:
					self.player.actionQueue.append(Player.UseBulletDownCM)

				if event.key == self.inputManager.BulletRight:
					self.player.actionQueue.append(Player.UseBulletRightCM)

				if event.key == self.inputManager.BulletLeft:
					self.player.actionQueue.append(Player.UseBulletLeftCM)



def main():

	game = WhatABlockGame(Vector2(1024, 768))


	while not game.isGameOver:

		game.render()

		game.update()
		

if __name__=='__main__':
    main()
    pygame.quit()
