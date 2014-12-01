from Revealer import *


class MovingRevealer(Revealer):
	def __init__(self, startScreenPos, radius, speed, lifeTime):
		super(MovingRevealer, self).__init__(startScreenPos = startScreenPos, radius = radius)
		self.speed = speed
		self.lifeTime = lifeTime
		self.lifeTimeCounter = 0

	def reveal(self, isoBlocks):
		if self.alive:
			self.updateReveal()
			super(MovingRevealer, self).reveal(isoBlocks)

	def updateReveal(self):
		if self.lifeTimeCounter < self.lifeTime:
			self.lifeTime += 1
			self.updatePosition()
		else:
			self.alive = False

	def updatePosition(self):
		currentPos = self.screenPos
		self.setPos(Vector2( currentPos.getX() + self.speed.getX(), currentPos.getY() + self.speed.getY()))


