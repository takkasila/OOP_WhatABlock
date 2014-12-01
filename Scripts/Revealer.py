from WhatABlock_GameLib import *

class Revealer(object):
	def __init__(self, startScreenPos, radius = 0):

		self.screenPos = startScreenPos
		self.radius = radius
		self.alive = True

	def getRadius(self):
		return self.radius

	def reveal(self, isoBlocks):
		for block in isoBlocks:
			if Vector2.Distance(self.screenPos, IsoToScreen(block.getIsoPos(), block.getWidth(), block.getHeight() )) <= self.radius:
				block.setVisible(True)

	def setPos(self, targetScreenPos):
		self.screenPos = targetScreenPos

	def isAlive(self):
		return self.alive
		