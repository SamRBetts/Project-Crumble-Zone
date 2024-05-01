# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 22:02:42 2024

@author: bettssr
"""

# Filename: TelemetryScreen.py
"""
Description: The Telemetry screen creates all the necessary graphs for the screen
    and updates screens as well. This file includes classes for custom graphing
    objects 
Author: Betts, Sam
Date: November 29, 2023
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui


#custom modules
import Dictionary_telemetry_point
from PacketHelper import PacketHandler
from CSVHelper import CSVHandler
from CMDHelper import CMDHelper
from XBeeHandler import XbeeHelper
from ScreenHelpers import TelemetryGraph, DisplayLabel, CommandRadioButton, Button

port = "COM11"

class TestCmdScreen(QMainWindow):
    """
    MainWindow: Creates the Main Window with layouts for all graphs and labels
        Handles updates to screens from packets 
    
    """
    
    def __init__(self):
        super(TestCmdScreen, self).__init__()
        #initialize variables
        
        #import the dictionary
        self.telemetry_points = Dictionary_telemetry_point.telemetry_points
        
        #define classes needed
        self.packet_handler = PacketHandler()
        self.cmd_helper = CMDHelper()
        self.timer = QTimer()
        self.csv_handler = CSVHandler()
        self.xbee = XbeeHelper() #initializes contact with Xbee on serial po

        self.setWindowTitle("Test Command Screen")
        self.setWindowIcon(QtGui.QIcon('CrumpleZone_cv_cropped.svg'))

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
        cmd_term_layout_c = QVBoxLayout()

        
        cmd_terminal_layout.addLayout(cmd_term_layout_a,0,0)
        cmd_terminal_layout.addLayout(cmd_term_layout_b,0,1)
        cmd_terminal_layout.addLayout(cmd_term_layout_c,0,2)


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
        self.mis_time_lbl = DisplayLabel("hh:mm:ss UTC",1)
        parameter_layout1_b.addWidget(self.mis_time_lbl)
        
        self.GPS_time_lbl = DisplayLabel("hh:mm:ss UTC",1)
        parameter_layout1_b.addWidget(self.GPS_time_lbl)

        self.packet_count = 0;
        self.pkt_tx_lbl = DisplayLabel("0",1)
        parameter_layout1_b.addWidget(self.pkt_tx_lbl)
        
        self.cmd_echo_lbl = DisplayLabel("NONE",1)
        parameter_layout1_b.addWidget(self.cmd_echo_lbl)
        
        self.state_lbl = DisplayLabel("NONE",1)
        parameter_layout2_b.addWidget(self.state_lbl)
        
        self.HS_dpl_lbl = DisplayLabel("NONE",1)
        parameter_layout2_b.addWidget(self.HS_dpl_lbl)
        
        self.PC_dpl_lbl = DisplayLabel("NONE",1)
        parameter_layout2_b.addWidget(self.PC_dpl_lbl)
        
        self.GPS_sats_lbl = DisplayLabel("0",1)
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
        """
        self.alt_graph = TelemetryGraph("Altitude","m")
        self.alt_graph.plotFirst("Barometer")
        self.alt_graph.plotSecond("GPS")
        main_layout_bottom.addWidget(self.alt_graph, 0, 0)
                
        self.pressure_graph = TelemetryGraph("Pressure", "kPa")
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
        
        self.rot_graph = TelemetryGraph("Z Rotation","deg/s")
        self.rot_graph.plotFirst("MPU6050")
        main_layout_bottom.addWidget(self.rot_graph, 2,1)
        
        self.voltage_graph = TelemetryGraph("Voltage","V")
        self.voltage_graph.plotFirst( "Voltage Sensor")
        main_layout_bottom.addWidget(self.voltage_graph,0,2)
        
        self.temp_graph = TelemetryGraph("Temperature", "deg C")
        self.temp_graph.plotFirst("BMP0909")
        main_layout_bottom.addWidget(self.temp_graph,1,2)
        """
        
        
        self.start_button = Button("START SCREEN")
        startstop_layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.startTimer)
        
        
        self.stop_button = Button("STOP SCREEN")
        startstop_layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stopTimer)
       
        cmd_term_lbl = DisplayLabel("~~~~~~~~~~~~~~~~~~~~~COMMAND TERMINAL~~~~~~~~~~~~~~~~~~~~",0) 
        command_layout.addWidget(cmd_term_lbl,1,0)
        
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
        cmd_term_layout_b.addWidget(bcn_on_rb)
        
        bcn_off_rb = CommandRadioButton('BCN - Audio Beacon OFF', self)
        bcn_off_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(bcn_off_rb)
        
        pr_on_rb = CommandRadioButton('PR - Parachute Rentention ON', self)
        pr_on_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(pr_on_rb)
        
        pr_off_rb = CommandRadioButton('PR - Parachute Rentention OFF', self)
        pr_off_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(pr_off_rb)
        
    
        cal_rb = CommandRadioButton('CAL - Set 0m altitude', self)
        cal_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_a.addWidget(cal_rb)        
        
        sim_act_rb = CommandRadioButton('SIM - Simulation mode ACTIVATE', self)
        sim_act_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_c.addWidget(sim_act_rb) 
        
        sim_en_rb = CommandRadioButton('SIM - Simulation mode ENABLE', self)
        sim_en_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_c.addWidget(sim_en_rb)
        
        sim_dis_rb = CommandRadioButton('SIM - Simulation mode DISABLE', self)
        sim_dis_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_c.addWidget(sim_dis_rb)
        
        rstpkt_rb = CommandRadioButton('RSTPKT - Reset Packet Count', self)
        rstpkt_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_b.addWidget(rstpkt_rb)
        
        dtch_rb = CommandRadioButton('DTCH - Detach Nose Cone', self)
        dtch_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_c.addWidget(dtch_rb)
        
        open_rb = CommandRadioButton('OPEN - Open Nose Cone Latch', self)
        open_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_c.addWidget(open_rb)  
        
        close_rb = CommandRadioButton('CLOSE - Close Nose Cone Latch', self)
        close_rb.toggled.connect(self.cmdSelected)
        cmd_term_layout_c.addWidget(close_rb)   
        
        self.current_cmd = telem_on_rb #initialize as a random radio button for now
        #boolean values to check for simulation mode
        self.simmode_enabled = False
        self.simmode_activated = False
        self.simmode = False
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setGeometry(0,40,800,300)
        
        """
        Should connect to Xbee when click the start button or start the screen?
        """        
        try:
            self.xbee.connect(port)
            
        except: 
            self.setWindowTitle("TestCMDScreen - Xbee NOT connected")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(False)
        
        self.packets_rx =0 
        
    def cmdSelected(self):
        rb = self.sender()
        
        if rb.isChecked():
            self.current_cmd = rb #set the current command to the radio button checked as an object
            self.send_button.setEnabled(True)
            
    def startTimer(self):
       
        try: 
            self.xbee.connect(port)
        except: 
            print("NO XBEE CONNECTED")
        #self.xbee.connect(port)
        #time.sleep(1)
                
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.checkSerial)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.clearPlots()
        
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
            self.sendSimP()
                   
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
    def updateData(self, incoming_packet):
        """
        calls updates to all telemetry graphs and labels with a given incoming packet
        accesses the index in the list (found using the dictionary), update each plot or label
        """       
        self.packets_rx  = self.packets_rx +1 
        self.mis_time_lbl.setText(incoming_packet[self.telemetry_points['MISSION_TIME']])
        self.GPS_time_lbl.setText(incoming_packet[self.telemetry_points['MISSION_TIME']])
        #self.GPS_time_lbl.setText(self.cmd_helper.getUTCTime())
        #TODO: change this to number of packets recieved, NOT SENT
        self.pkt_tx_lbl.setText(f"{self.packets_rx}")

        #self.pkt_tx_lbl.setText(incoming_packet[self.telemetry_points['PACKET_COUNT']])
        self.mode_dpl_lbl.setText(incoming_packet[self.telemetry_points['MODE']])
        self.state_lbl.setText(incoming_packet[self.telemetry_points['STATE']])
        self.GPS_sats_lbl.setText(incoming_packet[self.telemetry_points['GPS_SATS']])
        self.HS_dpl_lbl.setText(incoming_packet[self.telemetry_points['HS_DEPLOYED']])
        self.PC_dpl_lbl.setText(incoming_packet[self.telemetry_points['PC_DEPLOYED']])
        self.cmd_echo_lbl.setText(incoming_packet[self.telemetry_points['CMD_ECHO']])
        alt = float(incoming_packet[self.telemetry_points['ALTITUDE']])
        gps_alt = float(incoming_packet[self.telemetry_points['GPS_ALTITUDE']])
        """
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
        """
               
    def sendCommand(self):
        """
        Connected to the send command button. Reads the radio buttons and calls the CMD
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
        elif cmd_name == "RSTPKT":
            command = self.cmd_helper.cmdResetPkt()
        elif cmd_name == "DTCH":
            command = self.cmd_helper.cmdServo("DTCH")
        elif cmd_name == "OPEN":
            command = self.cmd_helper.cmdServo("OPEN")
        elif cmd_name == "CLOSE":
                command = self.cmd_helper.cmdServo("CLOSE")
        elif cmd_name == "SIM":
            command = self.cmd_helper.cmdSimMode(option)
            if option == "ENABLE":
                self.simmode_enabled =True
            elif option == "ACTIVATE":
                self.simmode_activated = True
            elif option == "DISABLE":
                self.simmode_activated = False
                self.simmode_enabled = False
                
            else:
                print('\x1b[0;30;41m' + 'Warning: Simulation mode NOT ENABLED/ACTIVATED' + '\x1b[0m')

        print(command)
        #send the command via the xbee serial! 
        if self.xbee.checkPort():
            self.xbee.sendData(command)
        else:
            #give an error message
            print('\x1b[0;30;41m' + 'XBEE PORT NOT OPEN' + '\x1b[0m')

        if self.simmode_enabled and self.simmode_activated:
            print("SIM MODE ACTIVATED")
            self.SimMode()
        
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
            self.simmode = False
            self.simmode_activated = False
            self.simmode_enabled = False
        else: 
            cmd = self.cmd_helper.cmdSimP(pressure)
            #use xbee helper to send next value
            self.xbee.sendData(cmd)
     
    """
    def clearPlots(self):
        
        clear all plots (and maybe labels?) when start button is pressed
        TODO: TEST THIS
     
        self.pressure_graph.reset()
        self.alt_graph.reset()
        self.speed_pitot_graph.reset()
        self.temp_graph.reset()
        self.voltage_graph.reset()
        self.pressure_graph.reset()
        self.GPS_graph.reset()
        self.tilt_graph.reset()
        self.rot_graph.reset()
        
    """
