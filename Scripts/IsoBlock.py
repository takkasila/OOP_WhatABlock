from WhatABlock_GameLib import *
import pygame
from pygame.locals import *

class IsoBlock(object):
	
	isoPos = 0
	screenPos = 0
	width = 0
	height = 0
	tall = 0
	worldRect = 0
	visible = True


	def __init__(self, isoPos, width, height):

		self.isoPos = isoPos
		self.width = width
		self.height = height
		self.visible = True
		
		self.screenPos = IsoToScreen(self.isoPos, self.width, self.height)
		self.worldRect = pygame.Rect(self.screenPos.getX() - self.width/2, self.screenPos.getY(), self.width, self.height)

	def render(self, display, image, camPos):

		if(self.visible):
			renderRect = pygame.Rect(self.worldRect.left - camPos.getX(), self.worldRect.top - camPos.getY(), self.worldRect.width, self.worldRect.height)
			display.blit(image, renderRect)

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getPos(self): 
		return self.screenPos

	def getIsoPos(self): #return Vector2
		return self.isoPos

	def getIsoPos2(self): #return []
		return [self.isoPos.getX(), self.isoPos.getY()]

	def getVisible(self):
		return self.visible

	def setVisible(self, visible):
		self.visible = visible


