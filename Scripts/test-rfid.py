from practicum import findDevices
from peri import PeriBoard
from time import sleep

devs = findDevices()

if len(devs) == 0:
    print "*** No MCU board found."
    exit(1)

b = PeriBoard(devs[0])
print "*** MCU board found"
print "*** Device manufacturer: %s" % b.getVendorName()
print "*** Device name: %s" % b.getDeviceName()

count = 0
while True:
    sleep(0.1)
    rfid = b.getRFID()
    print rfid

