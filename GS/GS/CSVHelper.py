# Filename: CSVCreater.py
"""
Description: Handles all .csv splicing  and saving
Author: Betts, Sam
Date: November 29, 2023
"""

import pandas as pd 
from PyQt5.QtWidgets import QFileDialog


class CSVHandler():
    
    """
    CSVCreater: Handles all csv functions.
    
        Note: Telemetry Packet includes  altitude, air pressure, temperature,
            battery voltage, probe tilt angles, air speed, command echo, and GPS
            coordinates that include latitude, longitude, altitude and number of
            satellites tracked.
    Attributes:
        (all python lists)

    Methods:
        saveCSV(): save all data from the telemetry packets to the python repository as .csv
        appendCSV: add new packet data to current telemetry data data frame
        getCurrData(): returns current data frame wit hall telemetry data
        
        openFile(): creates file diaglog to select a csv file, returns text in csv
        spliceSIMP(): returns list of pressure values (all values in columns) 
            ignoring #. List is stored as instance variable in this class
        getNextSIMP(): get the next pressure value stored in the pressure values list,
            increase line index, return next pressure value
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
        tp = pd.DataFrame(data = telemetry_packet)
        tp= tp.transpose()
        self.telemetry_data = pd.concat([self.telemetry_data, tp],ignore_index=True,axis=0)
    

    def getCurrData(self):
        return self.telemetry_data
    
    
    def openFile(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file','c:\\users/bettssr/documents/github/project-crumple-zone/GS/GS',"Text file (*.txt *.csv)")

        file = open(fname[0])
        text = file.read()
        #print(text)
        #return(text)
        self.spliceSIMP(text)

    def spliceSIMP(self,text):
        """
        Splices text of csv (type string) of pressure values and returns a list of pressure
        values
        """
        lines = text.split('\n') #list object where each line is a different row
        #num_rows = len(text.split('\n'))
        #print(num_rows)
        #print(lines)
        self.pressure_vals = list()
        
        #iterate through each line looking for comments and pressure values
        for line in lines: 
            #check for empty lines and commments, ignore them
            if len(line)>0 and line[0] != '#':
                self.pressure_vals.append(line.split(',')[-1])   
          
        #print(pressure_vals)
        self.SIMP_index = 0 

    def getNextSIMP(self):
        
        if self.SIMP_index == len(self.pressure_vals):
            send = None
        else:
            send = self.pressure_vals[self.SIMP_index]
            self.SIMP_index += 1  
        
        #print(send)
        return send 
        