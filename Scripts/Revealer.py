from WhatABlock_GameLib import *

class Revealer(object):
	def __init__(self, startScreenPos, radius):

		self.screenPos = startScreenPos
		self.radius = radius

	def getRadius(self):
		return self.radius

	def reveal(self, isoBlocks):
		for block in isoBlocks:
			if Vector2.Distance(self.screenPos, IsoToScreen(block.getIsoPos(), block.getWidth(), block.getHeight() )) <= self.radius:
				block.setVisible(True)

	def setPos(self, targetScreenPos):
		self.screenPos = targetScreenPos


		