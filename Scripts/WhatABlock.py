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

	WINDOW_SIZE = Vector2(1366, 768)
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
	bgSound = ''


	def __init__(self, WINDOW_SIZE):

		self.WINDOW_SIZE = Vector2(1366, 768)
		self.isGameOver = False
		self.playWithRFID = True

		self.folderDir = os.path.split(os.getcwd())[0]
		self.assetDir = self.folderDir + '/Assets/'


		self.inputManager = InputManager()
		if self.playWithRFID:
			self.myRFIDReader = RFIDReader()
			self.inputManager.setRFIDInput(self.myRFIDReader)

		pygame.init()
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((self.WINDOW_SIZE.getX(), self.WINDOW_SIZE.getY()), pygame.FULLSCREEN)
		pygame.display.set_caption('What A Block')

		self.loadAssets()
		
		self.cam = Camera(offSet = Vector2(self.WINDOW_SIZE.getX()/2 , self.WINDOW_SIZE.getY()/2 - self.player.getHeight()/2), camSize = self.WINDOW_SIZE)

		
		self.player_revealver = Revealer(IsoToScreen(self.player.getIsoPos(), self.mapCollection.getBlockSize().getX(), self.mapCollection.getBlockSize().getY()), 60)

		pygame.mixer.music.play(-1)


	def loadAssets(self):
		
		pygame.mixer.music.load(self.assetDir + 'bgSound.mp3')
		self.mapCollection = MapCollection(currentMap = 0, assetDir = self.assetDir, WINDOW_SIZE = self.WINDOW_SIZE)
		self.player = Player(self.mapCollection.getCurrentMapObject().getPlayerStartPos(), assetDir = self.assetDir, blockWidth = self.mapCollection.getBlockSize().getX(), blockHeight = self.mapCollection.getBlockSize().getY(), moveSpeed = 0.1)
		self.mainFontSize = 50
		self.secondFontSize = 30
		self.thirdFontSize = 18
		self.mainFont = pygame.font.Font(self.assetDir + "Universe.ttf", self.mainFontSize)
		self.secondFont = pygame.font.Font(self.assetDir + "Universe.ttf", self.secondFontSize)
		self.thirdFont = pygame.font.Font(self.assetDir + "Universe.ttf", self.thirdFontSize)
		self.numberOfDeath = 0


	def render(self):

		#sent player into map for order of rendering purpose
		self.mapCollection.renderCurrentMap(self.display, camPos = self.cam.getPos(), player = self.player)


		self.renderGUI()

		pygame.display.flip()

	def renderGUI(self):

		levelText = str(self.mapCollection.getCurrentMapIndex())	#Level
		renderlevelText = self.thirdFont.render( levelText, 1, (255,255,255))
		self.display.blit(renderlevelText, (self.WINDOW_SIZE.getX()/2 - len(levelText) * self.thirdFontSize/2 + 5, self.WINDOW_SIZE.getY()*8.3/20))		

		deathCountText = str(self.numberOfDeath)	#Death
		renderDeathCountText = self.mainFont.render( deathCountText, 1, (0,0,0))
		self.display.blit(renderDeathCountText, (self.WINDOW_SIZE.getX()/2 - len(deathCountText) * self.mainFontSize/2 + 10, self.WINDOW_SIZE.getY()/9))

		bombCountText = str(self.player.getBomb())	#Bomb
		renderBombCountText = self.secondFont.render( bombCountText, 1, (127,100,0))
		self.display.blit(renderBombCountText, (self.WINDOW_SIZE.getX()*9/20 - len(deathCountText) * self.secondFontSize/2 + 10, self.WINDOW_SIZE.getY()*17/20))

		bulletCountText = str(self.player.getBullet()) #Bullet
		renderBulletCountText = self.secondFont.render( bulletCountText, 1, (127,100,0))
		self.display.blit(renderBulletCountText, (self.WINDOW_SIZE.getX()*11/20 - len(deathCountText) * self.secondFontSize/2 + 10, self.WINDOW_SIZE.getY()*17/20))

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
			self.numberOfDeath += 1

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
