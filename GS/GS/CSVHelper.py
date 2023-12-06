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
        saveCSV(): save all data from the telemetry packets to the python repository as .csv
        appendCSV: add new packet data to current telemetry data data frame
        getCurrData(): returns current data frame wit hall telemetry data
        
        ~~~Yet to be implemented~~~
        openCSV(): opens file explorer to chose a csv file to splice
        spliceCSV(): returns array of values in the rows of the file ignoring columns
            preceded by # and as many arrays as there are columns
        getSimPressure(): uses openCSV and splice CSV to open csv and return an 
            of pressure values
    """
   
   
    def __init__(self):
        
        
        self.file_name = "Flight_2033.csv"
        file_headers = 'telemetry_headers.csv'
        #this here is a but scuffed, the headers have to be in the 2nd row 
        self.telemetry_data = pd.DataFrame(None) #initialize telemetry data frame
        self.df_headers= pd.read_csv(file_headers) #converts into a dataframe

                
    def saveCSV(self):
        """
        saves the csv currently created from telemetry_data and data_headers 

        """
        #creates a new data frame with the telemetry data and the headers       
        merged_df = pd.DataFrame(self.telemetry_data.values, columns=self.df_headers.iloc[0]) 
        merged_df.to_csv(self.file_name) #save merged data frame
        
        
        
    def appendCSV(self,telemetry_packet: str):
        
        #vertically concatonates the new packet to data already received
       
        self.telemetry_data = pd.concat([self.telemetry_data, telemetry_packet],ignore_index=True,axis=0)
    

    def getCurrData(self):
        return self.telemetry_data



        
        
        
        