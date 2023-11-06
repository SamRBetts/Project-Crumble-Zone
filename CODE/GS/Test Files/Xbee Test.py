# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:31:08 2023
Xbee example code
@author: bettssr
"""
from digi.xbee.devices import XBeeDevice

device = XBeeDevice("COM1", 9600)
device.open()
device.send_data_broadcast("Hello XBee World!")
device.close()
