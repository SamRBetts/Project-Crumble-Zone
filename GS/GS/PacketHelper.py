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



class PacketHandler():
    """
    PacketHandler: interfaces with the packet recieved by the Xbee
    Attributes:
    - 
    
    
    Methods:
    - splicePacket(): takes .csv from Xbee and extracts every telemetry point 
    from the recieved packet
    - createPacket(): for testing only. Creates a correctly format packet given
    all necessary data
    """
    
    def __init__(self):
        pass
        

    def splicePacket(packet:str):
        """
        TODO: remove all the commas and return array with each data pint
        check that team_id is correct 
        does it make sense to use a dictionary here to assign a number to each
        telemetry point??? 21 data points
        """
        pass
    
    
    def createPacket():
       #omg there are so many things to add into this function :<<<<<
        
       pass
    
    


        
        
        
    
    