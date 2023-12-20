# Filename: XBeeHandler.py
"""
Description: This class does all the communication with xbees using it as a 
    single xbee object. It checks for packet errors and returns a csv file
Author: Betts, Sam
Date: November 29, 2023

PySerial API: https://pyserial.readthedocs.io/en/latest/pyserial_api.html

"""

"""
TODO: 
like the whole thing
"""

from serial import Serial

class XbeeHelper():
    
    """
    XbeeHandler: interfaces with Xbee
    Attributes:
    - 
    
    
    Methods:
    - __init__(): creates object
    - initializeXbee(): checks Xbee for Baud rate, connection, settings
    - getData(): returns a string with data. 
    - sendData(): sends a command with formatted command from CMDHelper
    - checkConnection()
    - clearBuffer(): clears the buffer (data that hasn't been read yet)
    
    """
    
    def __init__(self, port:str):
       #set-up communication with the Xbee for first-time startup
       self.timeo = 1000; #set number of seconds until connection times out
       self.xbee = Serial(port,baudrate=9600,timeout=self.timeo)
       print('\x1b[;30;42m' + 'Connection Established with Xbee' + '\x1b[0m')
       self.escape_bit=">".encode('utf-8')
       self.start_bit="<".encode('utf-8')
       

    
    
    def getData(self):
        #is called when data is detected in the buffer
        
        #decodes the data (utf-8)
        """
        TODO: figure out the total size
        
        """
        #recieving garbage data don't care about
        self.xbee.read_until(self.start_bit)
        #now we actually have data, save it 
        packet = self.xbee.read_until(self.escape_bit)
       
        
        #close serial port! 
        self.xbee.__del__()
        return packet.decode('utf-8')
        #return packet
    
    def sendData(self, packet:str):
       #recives a str to send
       self.xbee.write(packet.encode('utf-8'))
       #encodes the data (utf-8)
       self.xbee.flush() #wait until all data is written (probably a good idea idk)
       #sends data over serial
       
    def checkBuffer(self):
       buffer = self.xbee.in_waiting()
       if(buffer >=1 and self.startbit in buffer): 
           #check if there is a character in the buffer, and if there is, check for start bit           
       
            buffer = 0
            return 1
       else: 
           buffer = 0
           return 0 
        
        
    
    
    
    