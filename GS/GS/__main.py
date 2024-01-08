# Filename: __main.py
"""
Description: This main application will run all the required code to operate
    the ground station including running the telemetry screen and all relevant
    classes
Author: Betts, Sam
Date: November 29, 2023
"""

"""
TODO: clean this up! event loop now in telemetry screen

"""


from PacketHelper import PacketHandler
from CSVHelper import CSVHandler
from CMDHelper import CMDHelper
from XBeeHandler import XbeeHelper
from TelemetryScreen import MainWindow

import pandas as pd
import time
from serial import Serial
import sys
from PyQt5.QtWidgets import QApplication




def main():

    #put all the main execution here
    
    """
    CLASS TESTING
    """
    #xbee = XbeeHelper("COM9") #initializes contact with Xbee on serial port
    ch = CSVHandler()



    # Create an application instance
    app = QApplication(sys.argv)
    #window.setGeometry(100, 100, 400, 200)
    
    # Create a label
    #label = QLabel("Altitude", main)
    #label.move(150, 80)
    
    
    #main = MainWindow(xbee)
    main = MainWindow()
    # Show the main window
    main.startTimer()
    main.show()
    
    # Start the application event loop
    app.exec() 
    
    
    
    
    #packet = pd.read_csv('telemetry_packet_example.csv',header=None,squeeze=True)
   
    #csv_helper.appendCSV(packet)
    #csv_helper.appendCSV(packet)
    
   #print(csv_helper.getCurrData())
       
    #csv_helper.saveCSV()
    

    """
    PACKET HANDLER TESTING
       
    """
    
    #ph = PacketHandler()
    #list_ex = ph.splicePacket('2033,data1,data2,data3,andmore')
    #print(list_ex)
    
    
    """
    CMDHELPER
    
    ch = CMDHelper()
    #print(ch.cmdSetTime("GPS"))
    print(ch.cmdSimMode("FARTS"))
    """
    
    
    """
    NOMINAL OPERATIONS
    """
    
    #define used classes
    
    
    """
    packeth = PacketHandler()
    cmdh = CMDHelper()
    
    
    xbee.sendData("Here is a bunch of data")
    
    
    if xbee.checkBuffer(): #if there is a start bit waiting in serial port...
        incoming_packet = xbee.getData()
        #print(incoming_packet)
        data_list = packeth.splicePacket(incoming_packet) #splice packet to list type
        #print(data_list)
        cmdh.appendCSV(data_list) #add packet (as a list) to data in csvhelper
        #print(cmdh.getCurrData())
        #send data to telemetry screen to update
        #update telemetry screen
        main.update(data_list)
    
    """
    
    
    
    """

    """
    #cmdh.saveCSV() 
    

    """
    NOMINAL OPERATIONS MODE
default mode 
1.Create blank telemetry screen (TelemetryScreen.py)
2.Initialize connection with Xbee (XBeeHandler.py)
3.Wait/Check for Xbee packet (XBeeHandler.py)
    -event is triggered when the Xbee recieved a '<' value 
4.Send the packet to Telemetry screen and CSV class
5.Splice recieved packet (PacketHelper.py)
6.Update screen (TelemetryScreen.py)
Repeat 3-5 until Xbee disconnects or save .csv file is pressed (button on telemetry screen)
7. Save .csv (CSVHelper) OR enter simulation mode 
OR enter CMD mode based on button pressed OR exit

SIMULATION MODE
entered if simulation mode button on screen is pressed
___Should this be its own class?____
1. Open up file explorer to choose .csv file (CSVHelper)
2. Splice .csv file into array of pressure values (CSVHelper)
2. Send SIM command to CanSat (CMDHelper, XBeeHandler)
3. Send Pressure values to CanSat (CMDHelper, XbeeHandler)
4. Plot Pressure value just sent (TelemetryScreen.py)
5. Continue until pressure values are depleted (CMDHelper)

COMMAND HANDLING MODE
entered if a command is selected on Telemetry screen and sent 
1. Create CMD format (CMDHelper.py)
2. Send CMD (XBeeHandler.py)
3. Exit mode
"""

"""
NOMINAL OPERATIONS MODE
"""
















if __name__ == "__main__":
    main()
    
    
    