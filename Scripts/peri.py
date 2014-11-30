from practicum import McuBoard

RQ_SET_LED    = 0
RQ_GET_SWITCH = 1
RQ_GET_LIGHT  = 2
RQ_GET_RFID = 3

####################################
class PeriBoard(McuBoard):

    ################################
    def setLed(self, led_no, led_val):
        '''
        Set status of LED led_no on peripheral board to led_val
        '''
        self.usbWrite(RQ_SET_LED, index=led_no, value=led_val)

    ################################
    def setLedValue(self, value):
        '''
        Display value's 3 LSBs on peripheral board's LEDs
        '''
        value = value%8
        self.setLed(2, value>>2)
        self.setLed(1, value%4>>1) 
        self.setLed(0, value%2)

    ################################
    def getSwitch(self):
        '''
        Return a boolean value indicating whether the switch on the peripheral
        board is currently pressed
        '''
        if self.usbRead(request = RQ_GET_SWITCH, length = 1) == (0,):
            return False
        else:
            return True

    ################################
    def getLight(self):
        '''
        Return the current reading of light sensor on peripheral board
        '''
        return self.usbRead(request = RQ_GET_LIGHT, length = 2)[0] + self.usbRead(request = RQ_GET_LIGHT, length = 2)[1]*256 

    ###############################
    def getRFID(self):
        """
        Return the current reading IDcard on RFID cardreader
        """ 
        return self.usbRead(request = RQ_GET_RFID, length = 1)
