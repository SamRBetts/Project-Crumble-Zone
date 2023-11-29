# Filename: CSVCreater.py
"""
Description: Handles all .csv splicing  and saving
Author: Betts, Sam
Date: November 29, 2023
"""

"""
TODO:

"""


class CSVHandler():
     """
    CSVCreater: Handles all csv functions.
    
        
        Note: Telemetry Packet includes  altitude, air pressure, temperature,
            battery voltage, probe tilt angles, air speed, command echo, and GPS
            coordinates that include latitude, longitude, altitude and number of
            satellites tracked.
    Attributes:
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
        
    
    def __init__(self, alt_data, pressure_data, temp_data):
        file_name = "Flight_2033"
        """
        TODO: write code lol 
            Is is a stupid idea to have a data object whose attributes are the telemetry 
        data required? ??
        
        """
        
        pass
    
    





        
        
        
        