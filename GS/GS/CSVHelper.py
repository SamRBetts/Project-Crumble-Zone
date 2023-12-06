# Filename: CSVCreater.py
"""
Description: Handles all .csv splicing  and saving
Author: Betts, Sam
Date: November 29, 2023
"""

"""
TODO:

"""


import pandas as pd 



class CSVHandler():
    
    """
    CSVCreater: Handles all csv functions.
    
        
        Note: Telemetry Packet includes  altitude, air pressure, temperature,
            battery voltage, probe tilt angles, air speed, command echo, and GPS
            coordinates that include latitude, longitude, altitude and number of
            satellites tracked.
    Attributes:
        (all python lists)
        - alt_data = altitude
        - pressure_data = air pressure
        - temp_data = temperature
        - voltage_data = battery voltage
        - tilt_x_data = probe tilt x angle
        - tilt_y_data = probe tilt y angle
        - rot_z_data = probe rot z angle
        - pitot_data = air speed
        - CMD_echo = command echo
        - lat_GPS_data = GPS lat
        - long_GPS_data = GPS long
        - alt_GPS_data = GPS alt
        - GPS_sats_data = Sat tracked
    Methods:
        createCSV(): creates a .csv for judging from telemetry data with appropriate
        header and format, and shall save to a thumb drive for judges
        saveCSV(): could be with create idk
        openCSV(): opens file explorer to chose a csv file to splice
        spliceCSV(): returns array of values in the rows of the file ignoring columns
            preceded by # and as many arrays as there are columns
        getSimPressure(): uses openCSV and splice CSV to open csv and return an 
            of pressure values
    """
    file_name = "Flight_2033"
    file_headers = 'telemetry_headers.csv'
    data_headers = pd.read_csv(file_headers)
   
    def __init__(self):
        
        
        """
        TODO: write code lol 
            Is is a stupid idea to have a data object whose attributes are the telemetry 
        data required? ??
        
        """
        
           
        self.file_name = "Flight_2033"
        self.file_headers = 'telemetry_headers.csv'
        self.data_headers = pd.read_csv(self.file_headers)
        self.telemetry_data = None
        
                
    def saveCSV(self):
        """
        saves the csv currently created from telemetry_data and data_headers 

        """
        
        file_data = pd.concat([self.telemetry_data,self.data_headers],axis=0)
        file_data.to_csv(self.file_name,index=False)
        
        
    def appendCSV(self,telemetry_packet: str):
        
        #vertically concatonates the new packet to data already received
       
        self.telemetry_data = pd.concat([self.telemetry_data, telemetry_packet], axis=0)
       #this no worky :<
        
    

    def getCurrData(self):
        return self.telemetry_data



        
        
        
        