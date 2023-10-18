# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:36:31 2023

@author: ChatGPT
"""

import serial

# Open the virtual serial port for writing
ser = serial.Serial("CNCA2", 9600)  # Replace with your port name and baud rate

try:
    data_to_send = "Hello, Com0com!"  # Replace with the data you want to send
    ser.write(data_to_send.encode("utf-8"))  # Send the data
except Exception as e:
    print(f"Error: {e}")
finally:
    ser.close()  # Close the virtual serial por