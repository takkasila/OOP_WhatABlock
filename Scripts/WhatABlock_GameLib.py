from math import *

def getCos30():
	return 0.866
def getSin30():
	return 0.5


class Vector2():

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def get(self):
		return (self.x, self.y)

	def setX(self, x):
		self.x = x

	def setY(self, y):
		self.y = y

	def set(self, x, y):
		self.x = x
		self.y = y

	@staticmethod
	def Zero():
		return Vector2(0,0)

	@staticmethod
	def Plus(vec1, vec2):
		return Vector2(vec1.getX() + vec2.getX(), vec1.getY() + vec2.getY())

	@staticmethod
	def Minus(vec1, vec2):
		return Vector2(vec1.getX() - vec2.getX(), vec1.getY() - vec2.getY())

	@staticmethod
	def Distance(vec1, vec2):
		return sqrt( (vec2.getX() - vec1.getX())**2 + (vec2.getY() - vec1.getY())**2 )

	@staticmethod
	def DistanceFromOrigin(vec):
		return sqrt( vec.getX()**2 + vec.getY()**2 )

	@staticmethod
	def Lerp(vec1, vec2, percent):
		diff = Vector2.Minus(vec2, vec1)
		percentVec = Vector2(diff.getX() * percent, diff.getY() * percent)
		
		if abs(Vector2.DistanceFromOrigin(percentVec)) <= 0.1 :
			return vec2
		else:
			return Vector2.Plus(vec1, percentVec)

def IsoToScreen(iso_vec ,width, height):

	return Vector2((iso_vec.getX() - iso_vec.getY()) * int(width)/2
		, (iso_vec.getX() + iso_vec.getY()) * int(height)/2)

def ScreenToIso(screen_vec, width, height):

	return Vector2((screen_vec.getX() / int(width)/2 + screen_vec.getY() / int(width)/2) /2
		, (screen_vec.getY() / int(height)/2 -(screen_vec.getX() / int(width)/2)) /2)

if __name__=='__main__':
    
    #print IsoToScreen(Vector2(2,1) , 128, 64).getX()
	pass