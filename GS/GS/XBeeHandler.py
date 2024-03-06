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
import time 


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
    
    def __init__(self):
       #set-up communication with the Xbee for first-time startup
       self.timeo = .5 #set number of seconds until connection times out
       
       self.escape_bit=">".encode('utf-8')
       self.start_bit="<".encode('utf-8')
       self.xbee = Serial()
    def connect(self, port:str):
        self.xbee = Serial(port,baudrate=9600,timeout=self.timeo)
        #self.xbee.open() maybe need this -- update: don't 
        print('\x1b[;30;42m' + 'Connection Established with Xbee' + '\x1b[0m')
    
    def disconnect(self):
        self.xbee.close()
        
    def getData(self):
        #is called when data is detected in the buffer
        
        #decodes the data (utf-8)
        
        
        """
        TODO: figure out the total size, make sure this removes the start/end bit
        
        .read number of bytes,save that, then look at startbit
        struct - turn data streams into byte vice verse
        
        """
    
        #recieving garbage data don't care about
        #self.xbee.read_until(self.start_bit)
        #now we actually have data, save it 
        
        packet = self.xbee.read_until(self.escape_bit).decode('utf-8')
        print(packet)
        
        
        #return "<2033,0,1,2,3,5>"
        #return packet.decode('utf-8')
        packet = packet[:-1]
        return packet
    
    def sendData(self, packet:str):
       #recives a str to send
       self.xbee.write(packet.encode('utf-8'))
       #encodes the data (utf-8)
       self.xbee.flush() #wait until all data is written (probably a good idea idk)
       #sends data over serial
       
    def checkBuffer(self):
    
       buffer_list = None
       
       #print(self.xbee.in_waiting)
       
       if (self.xbee.in_waiting>0):  
           
           buffer = self.xbee.read_until(self.start_bit)
           #print(buffer)

    
           buffer_list = [str(x) for a,x in enumerate(str(buffer))] 
           #check if there is a character in the buffer, and if there is, 
    
           if(len(buffer_list) >= 1 and '<' in buffer_list):
               buffer = 0
               return 1
           else: 
               buffer = 0
               return 0
       else: 
           return 0 
       
       
       
     
        #experiement with reset_input_buffer() if this doesn't work :>
       
        
    def printBuffer(self):
        print(self.xbee.in_waiting)               
        
    def readLine(self):
        print(self.xbee.read_until('>'.encode('utf-8'),600))
        
    def checkPort(self):
        #return true is open
        
        return self.xbee.is_open
    
    
    
    