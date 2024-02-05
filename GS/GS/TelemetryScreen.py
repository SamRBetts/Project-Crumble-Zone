# Filename: TelemetryScreen.py
"""
Description: The Telemetry screen creates all the necessary graphs for the screen
    and updates screens as well. This file includes classes for custom graphing
    objects 
Author: Betts, Sam
Date: November 29, 2023
"""

"""
TODO: 
- Add way to pick and send commands (button+label)
-create .csav file button
-add simulation mode button

"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QGridLayout, QHBoxLayout,QPushButton, QVBoxLayout, QWidget,QRadioButton
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QTimer,QDateTime
#import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import numpy as np
import time 
import random
#custom modules
import WindowSettings
import Dictionary_telemetry_point
from PacketHelper import PacketHandler
from CSVHelper import CSVHandler
from CMDHelper import CMDHelper
from XBeeHandler import XbeeHelper

port = "COM9"


#inherit graphing widget to create custom graphing widget
class TelemetryGraph(PlotWidget):
    """
    TelemetryGraph: inherit graphing widget to create custom graphing widget
    Attributes:
    - title: title of the graph
    - x: the data associated with the x-axis, python list 
    - y: the data associated with the y-axis
    - ylabel: label for the y data

    Methods:
    - update(): appends data to the y array and automatically updates based on 
        current mission time
    """
    def __init__(self, title,ylabel, parent=None):
        super().__init__(parent)
        self.setBackground('w')
        self.setTitle(title,color="k",size = "20px")
        self.x = [0]
        self.ylabel = ylabel
        legend = self.addLegend()
        #legend.setBrush('k') #- makes legend black, but looks really bad. 
        self.doublePlot = 0
        
              
        styles = {'font-size':'22px'}
        self.setLabel('left', ylabel, **styles)
        self.setLabel('bottom', "time (s)", **styles) 
    
    def plotFirst(self,y1label):
        #self.plot(self.x,y1,pen=WindowSettings.pen1,name=y1label)
        self.y1 = [0]
        self.data_line = self.plot(self.x, self.y1, pen=WindowSettings.pen1,name=y1label)

        
        
    def plotSecond(self,y2label): 
       
        self.y2= [0]
        self.data_line2= self.plot(self.x,self.y2,pen=WindowSettings.pen2,name=y2label)
        self.doublePlot = 1 #flag saying there are 2 sets of data on plot 
        
    def updatePlot(self, new_data):
        #where new data is a list type 
        
 
        #print(new_data)
        """
        TODO: maybe make x the time value instead of packet number
        remove 0 value - may need to make a clear list function when 0 altitude
        is set with the button 
        """
        
        #get rid of initialized 0 bc I don't know what I'm supposed to do
        if self.x[0]==0:
            self.x.pop(0)
            self.y1.pop(0)
            if self.doublePlot:
                self.y2.pop(0)
                
        self.x.append(len(self.x)+1)  # Add a new value 1 higher than the last.
        
        self.y1.append(new_data[0])  
        
        if self.doublePlot:
            self.y2.append(new_data[1])
            self.data_line2.setData(self.x,self.y2)

        self.data_line.setData(self.x, self.y1)  # Update the data.
        

        
        


class DisplayLabel(QLabel):
    """
    DisplayLabel: Inherits QLabel to add custom colors
     and font size depending on type (data or name)
    Attributes:
    - text: text to be displayed on the label (string type)
    - func: 1 for data label and 0 for a name label
    Methods:
    - paintEvent(): fills in the background color
    """
    def __init__(self, text: str, func: int, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 20px;")  # Set the stylesheet
        self.func = func
 

    def paintEvent(self, event):
         painter = QPainter(self)
         if (self.func==1):
             painter.fillRect(self.rect(), QColor(WindowSettings.default_color))
    
         super().paintEvent(event)

class CommandRadioButton(QRadioButton):
    """
    custom radio button class - all command radio buttons are members
    """
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 16px;")

class Button(QPushButton):
    """
    custom button class - all command buttons are members
    """
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 16px;")    


#main window go brrrrrrr
class MainWindow(QMainWindow):
    """
    MainWindow: Creates the Main Window with layouts for all graphs and labels
        Handles updates to screens from packets 
    
    Methods:
    - 
    
    """
    
    #def __init__(self,xbee:XbeeHelper):
    def __init__(self):
        super(MainWindow, self).__init__()
        #initialize variables
        
        #import the dictionary
        self.telemetry_points = Dictionary_telemetry_point.telemetry_points
        
        #define classes needed
        self.packet_handler = PacketHandler()
        self.cmd_helper = CMDHelper()
        self.timer = QTimer()
        self.csv_handler = CSVHandler()
        self.xbee = XbeeHelper() #initializes contact with Xbee on serial po

        self.setWindowTitle("Telemetry Screen V2.5")

        #Create the layouts for organizing the screen
        main_layout_top = QGridLayout()
        main_layout_bottom = QGridLayout()
        main_layout = QGridLayout()
        
        #define layouts for organizing the top section where the parameters are
        parameter_layout1 = QVBoxLayout()
        parameter_layout1_b = QVBoxLayout()
        parameter_layout2 = QVBoxLayout()
        parameter_layout2_b = QVBoxLayout()
        
        #defining how command layout looks (bottom box in bottom grid)
        command_layout = QGridLayout() #1x4 final, main layout of command sectiosn
        startstop_layout = QHBoxLayout()
        cmd_terminal_layout = QGridLayout() #only 1x2, but just to make it easy   
        cmd_term_layout_a = QVBoxLayout()
        cmd_term_layout_b = QVBoxLayout()
        
        cmd_terminal_layout.addLayout(cmd_term_layout_a,0,0)
        cmd_terminal_layout.addLayout(cmd_term_layout_b,0,1)

        #need to vert layouts for each column
        
        command_layout.addLayout(startstop_layout,0,0)#add top bottom layout
        command_layout.addLayout(cmd_terminal_layout,2,0)
        
        #add main layouts
        main_layout.addLayout(main_layout_top, 0,0)  
        main_layout.addLayout(main_layout_bottom, 1,0)
        #add parameter screen layouts
        main_layout_top.addLayout(parameter_layout1,0,0)
        main_layout_top.addLayout(parameter_layout1_b,0,1)
        main_layout_top.addLayout(parameter_layout2,0,2)
        main_layout_top.addLayout(parameter_layout2_b,0,3)
        #add cmd layouts 
        main_layout_bottom.addLayout(command_layout,2,2)

        
        #Define all data display labels
        self.mis_time_lbl = DisplayLabel("hh:mm:ss",1)
        parameter_layout1_b.addWidget(self.mis_time_lbl)
        
        self.GPS_time_lbl = DisplayLabel("GPS hh:mm:ss UTC",1)
        parameter_layout1_b.addWidget(self.GPS_time_lbl)

        self.packet_count = 0;
        self.pkt_tx_lbl = DisplayLabel("XX",1)
        parameter_layout1_b.addWidget(self.pkt_tx_lbl)
        
        self.cmd_echo_lbl = DisplayLabel("NONE",1)
        parameter_layout1_b.addWidget(self.cmd_echo_lbl)
        
        self.state_lbl = DisplayLabel("FLIGHT MODE",1)
        parameter_layout2_b.addWidget(self.state_lbl)
        
        self.HS_dpl_lbl = DisplayLabel("YES",1)
        parameter_layout2_b.addWidget(self.HS_dpl_lbl)
        
        self.PC_dpl_lbl = DisplayLabel("N",1)
        parameter_layout2_b.addWidget(self.PC_dpl_lbl)
        
        self.GPS_sats_lbl = DisplayLabel("3",1)
        parameter_layout2_b.addWidget(self.GPS_sats_lbl)
        
        self.mode_dpl_lbl = DisplayLabel("NONE",1)
        parameter_layout2_b.addWidget(self.mode_dpl_lbl)
        
        #define all the data labels
        parameter_layout1.addWidget(DisplayLabel("Mission Time",0))
        parameter_layout1.addWidget(DisplayLabel("GPS Time",0))
        parameter_layout1.addWidget(DisplayLabel("Packets Recieved",0))
        parameter_layout1.addWidget(DisplayLabel("CMD Echo",0))
        parameter_layout2.addWidget(DisplayLabel("FSW State",0))
        parameter_layout2.addWidget(DisplayLabel("HS Deployed",0))
        parameter_layout2.addWidget(DisplayLabel("PS Deployed",0))
        parameter_layout2.addWidget(DisplayLabel("GPS sats tracking",0))
        parameter_layout2.addWidget(DisplayLabel("Mode",0))

        #Initialize all graphs as empty axes
        
        self.alt_graph = TelemetryGraph("Altitude","m")
        self.alt_graph.plotFirst("Barometer")
        self.alt_graph.plotSecond("GPS")
        main_layout_bottom.addWidget(self.alt_graph, 0, 0)
                
        self.pressure_graph = TelemetryGraph("Pressure", "Pa")
        self.pressure_graph.plotFirst("Barometer")
        main_layout_bottom.addWidget(self.pressure_graph,1,0)
        
        self.GPS_graph = TelemetryGraph("Coordinates", "deg")
        self.GPS_graph.plotFirst("Long")
        self.GPS_graph.plotSecond("Lat")
        main_layout_bottom.addWidget(self.GPS_graph, 2,0)
                
        self.speed_pitot_graph = TelemetryGraph("Air Speed","m/s")
        self.speed_pitot_graph.plotFirst("Pitot Tube")
        main_layout_bottom.addWidget(self.speed_pitot_graph, 0,1)
        
        self.tilt_graph = TelemetryGraph("Tilt","degrees")
        self.tilt_graph.plotFirst("X")
        self.tilt_graph.plotSecond("Y")
        main_layout_bottom.addWidget(self.tilt_graph,1,1)
        
        self.rot_graph = TelemetryGraph("Z Rotation","rpm")
        self.rot_graph.plotFirst("MPU6050")
        main_layout_bottom.addWidget(self.rot_graph, 2,1)
        
        self.voltage_graph = TelemetryGraph("Voltage","V")
        self.voltage_graph.plotFirst( "Voltage Sensor")
        main_layout_bottom.addWidget(self.voltage_graph,0,2)
        
        self.temp_graph = TelemetryGraph("Temperature", "deg F")
        self.temp_graph.plotFirst("BMP0909")
        main_layout_bottom.addWidget(self.temp_graph,1,2)
        
        
        self.start_button = Button("START SCREEN")
        startstop_layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.startTimer)
        
        
        self.stop_button = Button("STOP SCREEN")
        startstop_layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stopTimer)
        
        cmd_term_lbl = DisplayLabel("~~~~~~~~~~~~~~~COMMAND TERMINAL~~~~~~~~~~~~~~~",0) 
        command_layout.addWidget(cmd_term_lbl,1,0)
                
        
        #cmd_combobox = QComboBox()
        #cmd_combobox.addItems(['Turn telemetry on','Turn telemetry off','Set time GPS', 'Set time UTC', '',''])
        #command_layout.addWidget(cmd_combobox)
        
        
        #add send command button
        self.send_button = Button("SEND COMMAND")
        command_layout.addWidget(self.send_button,3,0)
        self.send_button.clicked.connect(self.sendCommand)
        self.send_button.setEnabled(False)

        
        #define the cmd radio buttons 
        telem_on_rb = CommandRadioButton('CX - Telemetry ON', self)
        telem_on_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_a.addWidget(telem_on_rb)
        
        telem_off_rb = CommandRadioButton('CX - Telemetry OFF', self)
        telem_off_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_a.addWidget(telem_off_rb)
        
        st_gps_rb = CommandRadioButton('ST - Set time to GPS', self)
        st_gps_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_a.addWidget(st_gps_rb)
        
        st_utc_rb = CommandRadioButton('ST - Set time to GS', self)
        st_utc_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_a.addWidget(st_utc_rb)

        bcn_on_rb = CommandRadioButton('BCN - Audio Beacon ON', self)
        bcn_on_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_a.addWidget(bcn_on_rb)
        
        bcn_off_rb = CommandRadioButton('BCN - Audio Beacon OFF', self)
        bcn_off_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_a.addWidget(bcn_off_rb)
        
        pr_on_rb = CommandRadioButton('PR - Parachute Rentention ON', self)
        pr_on_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(pr_on_rb)
        
        pr_off_rb = CommandRadioButton('PR - Parachute Rentention OFF', self)
        pr_off_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(pr_off_rb)
    
        cal_rb = CommandRadioButton('CAL - Set 0m altitude', self)
        cal_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(cal_rb)        
        
        sim_act_rb = CommandRadioButton('SIM - Simulation mode ACTIVATE', self)
        sim_act_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(sim_act_rb) 
        
        sim_en_rb = CommandRadioButton('SIM - Simulation mode ENABLE', self)
        sim_en_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(sim_en_rb)
        
        sim_dis_rb = CommandRadioButton('SIM - Simulation mode DISABLE', self)
        sim_dis_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(sim_dis_rb)
        
        simp_rb = CommandRadioButton('SIMP - Send simulated altitude', self)
        simp_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(simp_rb)
        
        self.current_cmd = simp_rb #initialize as a random radio button for now
        #boolean values to check for simulation mode
        self.simmode_enabled = False
        self.simmode_activated = False
        self.simmode = False
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setGeometry(0,40,1950,950)
                
        
       # self.timer.start()
    def cmdSelected(self):
        rb = self.sender()
        
        if rb.isChecked():
            self.current_cmd = rb #set the current command to the radio button checked as an object
            self.send_button.setEnabled(True)
            
    def startTimer(self):
        #'''
        if self.xbee.checkPort():
            pass
        else:
            self.xbee.connect(port)
        #'''
        #self.xbee.connect(port)
        #time.sleep(1)
                
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.checkSerial)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
    def stopTimer(self):
        self.timer.stop()
        
        """
        TODO: create save csv button or make it so it doesn't save when stop button
        or saves something         
        """
        
        if self.csv_handler.getCurrData().empty:
            print("CSV file is empty, skipping save")
        else:  
            self.csv_handler.saveCSV()
            print("saved csv")
            
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        
       
    def updateData(self, incoming_packet):
        """
        call updates to all telemetry graphs and labels with a given incoming packet
        accesses the index in the list (found using the dictionary), update each plot or label
        """       
        self.mis_time_lbl.setText(incoming_packet[self.telemetry_points['MISSION_TIME']])
        self.GPS_time_lbl.setText(incoming_packet[self.telemetry_points['MISSION_TIME']])
        #self.GPS_time_lbl.setText(self.cmd_helper.getUTCTime())
        #TODO: change this to number of packets recieved, NOT SENT
        self.pkt_tx_lbl.setText(incoming_packet[self.telemetry_points['PACKET_COUNT']])
        self.mode_dpl_lbl.setText(incoming_packet[self.telemetry_points['MODE']])
        self.state_lbl.setText(incoming_packet[self.telemetry_points['STATE']])
        self.GPS_sats_lbl.setText(incoming_packet[self.telemetry_points['GPS_SATS']])
        self.HS_dpl_lbl.setText(incoming_packet[self.telemetry_points['HS_DEPLOYED']])
        self.PC_dpl_lbl.setText(incoming_packet[self.telemetry_points['PC_DEPLOYED']])
  
        alt = float(incoming_packet[self.telemetry_points['ALTITUDE']])
        gps_alt = float(incoming_packet[self.telemetry_points['GPS_ALTITUDE']])
        self.alt_graph.updatePlot([alt,gps_alt])        

        speed = float(incoming_packet[self.telemetry_points['AIR_SPEED']])
        self.speed_pitot_graph.updatePlot([speed])
        
        temp = float(incoming_packet[self.telemetry_points['TEMPERATURE']])
        self.temp_graph.updatePlot([temp])
        
        volt = float(incoming_packet[self.telemetry_points['VOLTAGE']])
        self.voltage_graph.updatePlot([volt])
        
        pres = float(incoming_packet[self.telemetry_points['PRESSURE']])
        self.pressure_graph.updatePlot([pres])
        
        lat = float(incoming_packet[self.telemetry_points['GPS_LATITUDE']])
        long = float(incoming_packet[self.telemetry_points['GPS_LONGITUDE']])
        self.GPS_graph.updatePlot([lat,long])
        
        x = float(incoming_packet[self.telemetry_points['TILT_X']])
        y = float(incoming_packet[self.telemetry_points['TILT_Y']])
        self.tilt_graph.updatePlot([x,y])
        
        z = float(incoming_packet[self.telemetry_points['ROT_Z']])
        self.rot_graph.updatePlot([z])
            
    def checkSerial(self):
        """
        This method checks the serial buffer using the Xbee class and is called
        at every Qtimer interval
        If Xbee sees start bit, then calls readData, then updateData
        """
                
        print("checking serial: ")
     
        if self.xbee.checkBuffer()>0: #if there is a start bit waiting in serial port...
            print("Start bit found")    
            incoming_packet = self.xbee.getData()
            #print(incoming_packet)
            self.readData(incoming_packet)
        
        else:
            print("No start bit found")
        
        if self.simmode:
            self.sendSIMP()
                   
    def readData(self,incoming_packet:str):
        """
        Once the Xbee class says it has found a start bit, this method is called
        this reads an entire packet using the xbee class and splices it for
        the csv and telemetry classes. After splicing, updateData is called in telemetry screen
        and the live plots are updated
        """        
        data_list = self.packet_handler.splicePacket(incoming_packet) #splice packet to list type
        #print(data_list)
        
        if data_list is None:
            pass
        else:
            self.csv_handler.appendCSV(data_list) #add packet (as a list) to data in csvhelper
            #print(self.csv_handler.getCurrData())
            
            #send data to telemetry screen to update
            #update telemetry screen
            self.updateData(data_list)
        
        
    def sendCommand(self):
        """
        Connected to the send command button. Reads the combo box and calls the CMD
        class to create the selected command. Use Xbee class to send the data. 
        """
        #now for a nightmare of if statemetns bc I don't know how else to do this T.T
        cmd_array = self.current_cmd.text().split(" ") #take first part of string split
        cmd_name = cmd_array[0] #option = self.current_cmd.text().
        option = cmd_array[len(cmd_array)-1]
        command = ""
        
    
        
        #get the total command string from CMDHelper class
        if cmd_name == "CX":
            command = self.cmd_helper.cmdToggleTelemetry(option)
        elif cmd_name == "ST":
            command = self.cmd_helper.cmdSetTime(option)
        elif cmd_name == "BCN":
            command = self.cmd_helper.cmdToggleAudioBcn(option)
        elif cmd_name == "PR":
            command = self.cmd_helper.cmdTogglePR(option)
        elif cmd_name == "CAL":
            command = self.cmd_helper.cmdCalAlt()
        elif cmd_name == "SIM":
            command = self.cmd_helper.cmdSimMode(option)
            if option == "ENABLE":
                self.simmode_enabled =True
            elif option == "ACTIVATE":
                self.simmode_activated = True
            elif option == "DISABLE":
                self.simmode_activated = False
                self.simmode_enabled = False
        elif cmd_name == "SIMP":
            if self.simmode_enabled and self.simmode_activated:
                print("SIM MODE ACTIVATED")
                self.SimMode()
                #open file dialog
                #TODO: if both boolean values are true, open up file dialog and automatically send pressured values. 
                #maybe implemented a ARE YOU SURE??
                
                #this one needs changed to send pressure values every second, not correct right now
            else:
                print('\x1b[0;30;41m' + 'Warning: Simulation mode NOT ENABLED/ACTIVATED' + '\x1b[0m')

        print(command)
        #send the command via the xbee serial! 
        if self.xbee.checkPort():
            self.xbee.sendData(command)
        else:
            #give an error message
            print('\x1b[0;30;41m' + 'XBEE PORT NOT OPEN' + '\x1b[0m')

        
        #self.cmd_helper.cmdToggleAudioBcn("ON")
        
    def SimMode(self):
             
        
        """
        SIMULATION MODE
       
        1. Open up file explorer to choose .csv file (CSVHelper)
        2. Splice .csv file into array of pressure values (CSVHelper)
        2. Send SIM command to CanSat (CMDHelper, XBeeHandler)
        3. Send Pressure values to CanSat (CMDHelper, XbeeHandler)
        4. Continue execution loop in nominal operations
        5. Continue until pressure values are depleted (CMDHelper)
        """
        self.setWindowTitle("Telemetry Screen - SIMULATION MODE")
        self.simmode = True
        #get file from openFile 
        file_text = self.csv_handler.openFile()
        #print(type(file_text))
        #list of pressure values and index stored in csv class 
        #self.csv_handler.spliceSIMP(file_text)
        self.startTimer()
        
    def sendSimP(self):
        """
        send next pressure value at this iteration of the loop
        """
        #use csv helper to get next value
        pressure = self.csv_handler.getNextSIMP()
        #get name of command to send to xbee
        if pressure == None: #stop the timer if out of values 
            self.stopTimer()
        else: 
            cmd = self.cmd_helper.cmdSimP(pressure)
            #use xbee helper to send next value
            self.xbee.sendData()
        