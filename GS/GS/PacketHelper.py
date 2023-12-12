# Filename: PacketHandler.py
"""
Description: takes in a packet and returns indv. data for each telemetry point
Author: Betts, Sam
Date: November 29, 2023


Telemetry Data Format: 
TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE,
AIR_SPEED, HS_DEPLOYED, PC_DEPLOYED, TEMPERATURE, VOLTAGE,
PRESSURE, GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE,
GPS_SATS, TILT_X, TILT_Y, ROT_Z, CMD_ECHO [,,OPTIONAL_DATA]
"""

"""
TODO:
    -come up with the format of the packet 
    -

"""

#import pandas as pd 


class PacketHandler():
    """
    PacketHandler: interfaces with the packet recieved by the Xbee
    Attributes:
    - 
    
    
    Methods:
    - splicePacket(): takes string from Xbee and extracts every telemetry point 
    from the recieved packet into a list object for TelemetryScreen
    - createPacket(): for testing only. Creates a correctly format packet given
    all necessary data
    """
    
    
    def __init__(self):
        pass
    
    def splicePacket(self, packet:str):
        """
        Assume that the packets incoming all have
        -no new lines
        -21 values separated by commas 
        
        return a list object with all points in a different element
        """
        
        """
        TODO: remove all the commas and return array with each data pint
        check that team_id is correct 
        does it make sense to use a dictionary here to assign a number to each
        telemetry point??? 21 data points
        """
        
        #create a python list from comma separated values
        packet_list = packet.split(",")
        
        
        #check Team_ID, make sure is 2033, break if not 
        if packet_list[0] != "2033":
            print('\x1b[1;33;40m' + 'Warning: Team_ID does not match. Skipping packet...' + '\x1b[0m')
            packet_list=None
        
        #return list object
        return packet_list
    
    
    def createPacket():
       #omg there are so many things to add into this function :<<<<<
        
       pass
    
    


        
        
        
    
    