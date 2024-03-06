# Filename: XBeeHandler.py
"""
Description: This class does all the communication with xbees using it as a 
    single xbee object. It checks for packet errors and returns a csv file
Author: Betts, Sam
Date: November 29, 2023

PySerial API: https://pyserial.readthedocs.io/en/latest/pyserial_api.html

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
    - connect(): establishes serial object with baud and comm
    - disconnect(): closes serial communication
    - getData(): returns a string with data - reads until the stop bit is found
        returns string 
    - sendData(): sends a string through serial
    - checkPort(): returns true is serial xbee is connected, false if not
    - checkBuffer(): if data in the buffer, reads serial until start bit is found,
        Check to make sure didn't time out, return 1 (true) if start bit is found
    - printBuffer(): prints everything currently in the serial buffer (testing only)
    - readLine(): testing another way to read until start bit, testing only
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
        TODO: figure out the total size,        
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
        #remove the stop bit from packet
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
           #check if there is a start bit in the buffer, and if there is, 
    
           if(len(buffer_list) >= 1 and '<' in buffer_list):
               #reset buffer 
               buffer = 0
               return 1
           else: 
               buffer = 0
               return 0
       else: 
           return 0 
            
        #experiement with reset_input_buffer() if this doesn't work :>
       
        
    def printBuffer(self):
        #testing only
        print(self.xbee.in_waiting)               
        
    def readLine(self):
        #testing only
        print(self.xbee.read_until('>'.encode('utf-8'),600))
        
    def checkPort(self):
        #return true is open
        
        return self.xbee.is_open
    
    
    
    