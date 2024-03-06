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
        TODO: Some way to check and make sure packets are complete. Wait for Xbee
        testing for common errors before implementing
        """
        
        #create a python list from comma separated values
        packet_list = packet.split(",")
        
        
        #check Team_ID, make sure is 2033, break if not 
        if packet_list[0] != "2033":
            print('\x1b[1;33;40m' + 'Warning: Team_ID does not match. Skipping packet...' + '\x1b[0m')
            packet_list=None
        elif len(packet_list) != 21:
            packet_list = None
            print('\x1b[1;33;40m' + 'Warning: Packet incomplete. Skipping packet...' + '\x1b[0m')
       
        #return list object where each item is a different telemetry point 
        return packet_list
    
    
    def createPacket(self, packet_list:list):
       
       #put all the points in the list into a string - making a packet
       """
       TODO: add an escape character or something to make it more packet-like
       
       """
       packet_string = ','.join(packet_list)
       
       return packet_string
    

        
        
        
    
    