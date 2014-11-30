from WhatABlock_GameLib import Vector2

class Camera(object):

	pos = Vector2.Zero
	offSet = Vector2.Zero()
	camSize = Vector2.Zero()

	def __init__(self, startPos = Vector2.Zero(), offSet = Vector2.Zero(), camSize = Vector2.Zero()):
		self.pos = startPos
		self.offSet = offSet
		self.camSize = camSize

	def update(self, playerPos = Vector2.Zero()):
		self.pos = Vector2.Minus(playerPos, self.offSet)

	def getPos(self):
		return self.pos

		