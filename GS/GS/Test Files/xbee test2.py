# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:07:47 2024

@author: bettssr
"""

from XBeeHandler import XbeeHelper

xbee= XbeeHelper()
#xbee.connect("COM9")


#print(xbee.checkBuffer())

#xbee.printBuffer()
#xbee.readLine()

print(xbee.checkPort())
#print(xbee.checkBuffer())
if xbee.checkPort():
       pass
else:
   xbee.connect("COM9")
   print("connect")

        
   if xbee.checkBuffer()>0: #if there is a start bit waiting in serial port...
       print("Start bit found")    
       incoming_packet = xbee.getData()
       #print(incoming_packet)
       print(incoming_packet)
   else:
       print("No start bit found")
      
xbee.disconnect()