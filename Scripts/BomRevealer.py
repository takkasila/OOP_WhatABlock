from Revealer import *

class BomRevealer(Revealer):
	def __init__(self, startScreenPos, maxRadius, revealSpeed):
		super(BomRevealer, self).__init__(startScreenPos)
		self.maxRadius = maxRadius
		self.revealSpeed = revealSpeed

	def updateReveal(self):
		if self.radius < self.maxRadius:
			self.radius += self.revealSpeed
		else :
			self.alive = False

	def reveal(self, isoBlocks):
		if self.alive:
			self.updateReveal()
			super(BomRevealer, self).reveal(isoBlocks)


