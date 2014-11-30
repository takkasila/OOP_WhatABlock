class NiceClass(object):
	A = 0
	def __init__(self):
		NiceClass.A = 1

	def getA(self):
		return NiceClass.A
		
		
def main():
	myClass = NiceClass()
	
	print NiceClass.A

if __name__=='__main__':
    main()
