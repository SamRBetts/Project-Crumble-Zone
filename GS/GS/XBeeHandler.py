# Filename: XBeeHandler.py
"""
Description: This class does all the communication with xbees using it as a 
    single xbee object. It checks for packet errors and returns a csv file
Author: Betts, Sam
Date: November 29, 2023
"""

"""
TODO: 
like the whole thing
"""

class XBeeHandler():
    
    """
    XbeeHandler: interfaces with Xbee
    Attributes:
    - 
    
    
    Methods:
    - __init__(): creates object
    - initializeXbee(): checks Xbee for Baud rate, connection, settings
    - getData(): returns a .csv with data. 
    - sendData(): sends a command with formatted command from CMDHelper
    - checkConnection()
    - clearBuffer(): clears the buffer (data that hasn't been read yet)
    
    """
    
    def __init__(self):
       #set-up communication with the Xbee for first-time startup
        pass
    
    
    def getData():
        #is called when data is detected in the buffer
        
        #decodes the data (utf-8)
        
        #returns it as a csv
        pass
    
    def sendData():
       #recives a csv to send
       
       #encodes the data (utf-8)
       
       #sends data over serial
        pass
        
        
    
    
    
    