# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:05:52 2023

Creating a csv file from serial input
@author: bettssr
"""
import serial
port = "CNCA2"

term = serial.Serial(port,9600)
try:
    while True:
        #read data from a virtual serial port
        data = term.readline()
        print(data, end="")
        
        
except KeyboardInterrupt:
       term.close()
