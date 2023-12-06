# Filename: __main.py
"""
Description: This main application will run all the required code to operate
    the ground station including running the telemetry screen and all relevant
    classes
Author: Betts, Sam
Date: November 29, 2023
"""

"""
TODO: Launch Telemetry Screen from this application

"""


from PacketHelper import PacketHandler
from CSVHelper import CSVHandler
import pandas as pd

def main():

    #put all the main execution here
    
    """
    CLASS TESTING
    """
    
    csv_helper = CSVHandler()




    packet = pd.read_csv('telemetry_packet_example.csv',header=None,squeeze=True)
   
    csv_helper.appendCSV(packet)
    csv_helper.appendCSV(packet)
    
   
    
    
    #print(csv_helper.getCurrData())
    
    
    csv_helper.saveCSV()
    










    """
    NOMINAL OPERATIONS MODE
default mode 
1.Create blank telemetry screen (TelemetryScreen.py)
2.Initialize connection with Xbee (XBeeHandler.py)
3.Wait/Check for Xbee packet (XBeeHandler.py)
3.Send the packet to Telemetry screen and CSV class
4.Splice recieved packet (PacketHelper.py)
5.Update screen (TelemetryScreen.py)
Repeat 3-5 until Xbee disconnects or save .csv file is pressed (button on telemetry screen)
6. Save .csv (CSVHelper)

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
    
    
    