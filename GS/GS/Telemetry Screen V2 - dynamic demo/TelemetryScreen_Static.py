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
- implement Telemetry Graph to plot more than one set of data
- write update() method the TG 
- implement parameters.py to change graph appearance externally
- Test DisplayLabel()
- Add way to pick and send commands (button+label)
-create .csv file button
-add simulation mode button

"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QGridLayout, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QPainter
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import numpy as np
import WindowSettings
import Dictionary_telemetry_point

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
    def __init__(self, title,x, ylabel, parent=None):
        super().__init__(parent)
        self.setBackground('w')
        self.setTitle(title,color="k",size = "20px")
        self.x = x
        self.ylabel = ylabel
        #pen = pg.mkPen(color=(graph_color),width=5)
      #  print(np.hstack(y[0,:]))
        self.addLegend()
        self.doublePlot = 0
        
              
        styles = {'font-size':'22px'}
        self.setLabel('left', ylabel, **styles)
        self.setLabel('bottom', "time (s)", **styles) 
    
    def plotFirst(self,y1,y1label):
        #self.plot(self.x,y1,pen=WindowSettings.pen1,name=y1label)
        self.y1 = y1
        self.data_line = self.plot(self.x, y1, pen=WindowSettings.pen1,name=y1label)

        
        
    def plotSecond(self,y2,y2label): 
       
        self.data_line2= self.plot(self.x,y2,pen=WindowSettings.pen2,name=y2label)
        self.y2=y2
        self.doublePlot = 1 #flag saying there are 2 sets of data on plot 
        
    def updatePlotFirst(self, new_data):
        
        """
        TODO: write this fucntion!!!
        """
        #self.x = self.x[1:]  # Remove the first y element.
        print(self.x)
        self.x.append(len(self.x)+1)  # Add a new value 1 higher than the last.
        
        self.y1.append(new_data[0])  
        
        if self.doublePlot:
            self.y2.append(new_data[1])
            self.data_line2.setData(self.x,self.y2)
        #self.y = self.y[1:]  # Remove the first
        #self.y.append(y)  # Add a new random value.

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


#main window go brrrrrrr
class MainWindow(QMainWindow):
    """
    MainWindow: Creates the Main Window with layouts for all graphs and labels
        Handles updates to screens from packets 
    
    Methods:
    - 
    
    """
    
    def __init__(self):
        super(MainWindow, self).__init__()
        #initialize variables
        
        #import the dictionary
        self.telemetry_points = Dictionary_telemetry_point.telemetry_points
        
        #initialize lists of all telemetry to keep track of
        self.mission_time = []
        self.packet_count = []
        self.mode = []
        self.state = []
        self.altitude =[] 
        self.air_speed = []
        #self.HS_deployed = []
        #self.PC_deployed = []
        self.temperature = []
        self.voltage = []
        self.pressure = []
        self.GPS_time = []
        self.GPS_alt = []
        self.GPS_lat = []
        self.GPS_long = []
        #self.GPS_sats = []
        self.tilt_x = []
        self.tilt_y =[]
        self.rot_z = []
        # self.cmd_echo =[] 


        self.setWindowTitle("Telemetry Screen V1")

        #Create the layouts for organizing the screen
        main_layout_top = QGridLayout()
        main_layout_bottom = QGridLayout()
        main_layout = QGridLayout()
        
        #define layouts for organizing the top section where the parameters are
        parameter_layout1 = QVBoxLayout()
        parameter_layout1_b = QVBoxLayout()
        parameter_layout2 = QVBoxLayout()
        parameter_layout2_b = QVBoxLayout()
        
        command_layout = QVBoxLayout()
        main_layout_bottom.addLayout(command_layout,2,2)
        
        main_layout.addLayout(main_layout_top, 0,0)  
        main_layout.addLayout(main_layout_bottom, 1,0)
        
        main_layout_top.addLayout(parameter_layout1,0,0)
        main_layout_top.addLayout(parameter_layout1_b,0,1)
        main_layout_top.addLayout(parameter_layout2,0,2)
        main_layout_top.addLayout(parameter_layout2_b,0,3)
               
        
        #Define all data display labels
        mis_time_lbl = DisplayLabel("hh:mm:ss",1)
        parameter_layout1_b.addWidget(mis_time_lbl)
        
        GPS_time_lbl = DisplayLabel("GPS hh:mm:ss UTC",1)
        parameter_layout1_b.addWidget(GPS_time_lbl)

        pkt_rx_lbl = DisplayLabel("XX",1)
        parameter_layout1_b.addWidget(pkt_rx_lbl)
        
        cmd_echo_lbl = DisplayLabel("LAST CMD GIVEN",1)
        parameter_layout1_b.addWidget(cmd_echo_lbl)
        
        
        state_lbl = DisplayLabel("FLIGHT MODE",1)
        parameter_layout2_b.addWidget(state_lbl)
        
        HS_dpl_lbl = DisplayLabel("YES",1)
        parameter_layout2_b.addWidget(HS_dpl_lbl)
        
        PS_dpl_lbl = DisplayLabel("NO",1)
        parameter_layout2_b.addWidget(PS_dpl_lbl)
        
        GPS_sats_lbl = DisplayLabel("3",1)
        parameter_layout2_b.addWidget(GPS_sats_lbl)
        
        Mode_dpl_lbl = DisplayLabel("Mode",1)
        parameter_layout2_b.addWidget(Mode_dpl_lbl)
        
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
        
     
        
        #Example Data- will delete later 
        time = ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        example_data = [1,2,3,5,5,7,7,8,9,9,10,10,10,9,7]
        example2_data= [1,3,3,4,5,7,8,8,9,10,10,11,10,9,8]
        print(example_data)
        
       
        #define all needed graphs with placeholder data
        
        alt_graph = TelemetryGraph("Altitude",time,"m")
        alt_graph.plotFirst(example_data,"Barometer")
        alt_graph.plotSecond(example2_data, "GPS")
        main_layout_bottom.addWidget(alt_graph, 0, 0)
        
        alt_graph.updatePlotFirst([example2_data,example_data])
        
        pressure_baro_graph = TelemetryGraph("Pressure", time, "Pa")
        pressure_baro_graph.plotFirst(example_data, "Barometer")
        pressure_baro_graph.plotSecond(example2_data, "GPS")
        main_layout_bottom.addWidget(pressure_baro_graph,1,0)
        
        lat_GPS_graph = TelemetryGraph("Latitude",time, "deg")
        lat_GPS_graph.plotFirst(example_data, "Long")
        lat_GPS_graph.plotSecond(example2_data, "Lat")
        main_layout_bottom.addWidget(lat_GPS_graph, 2,0)
                
        speed_pitot_graph = TelemetryGraph("Air Speed",time, "m/s")
        speed_pitot_graph.plotFirst(example_data, "Pitot Tube")
        main_layout_bottom.addWidget(speed_pitot_graph, 0,1)
        
        tilt_graph = TelemetryGraph("Tilt", time,"degrees")
        tilt_graph.plotFirst(example_data,"X")
        tilt_graph.plotSecond(example2_data,"Y")
        main_layout_bottom.addWidget(tilt_graph,1,1)
        
        long_GPS_graph = TelemetryGraph("Z Rotation",time,"rpm")
        long_GPS_graph.plotFirst(example_data,"MPU6050")
        main_layout_bottom.addWidget(long_GPS_graph, 2,1)
        
        voltage_graph = TelemetryGraph("Voltage",time,"V")
        voltage_graph.plotFirst(example_data, "Voltage Sensor")
        main_layout_bottom.addWidget(voltage_graph,0,2)
        
        temp_graph = TelemetryGraph("Temperature",time, "deg F")
        temp_graph.plotFirst(example_data, "BMP0909")
        main_layout_bottom.addWidget(temp_graph,1,2)
        
        """
        TODO: Finalize layout, add all commands, make button trigger cmd class
        make buttons for sim mode or other things idk find a good way to do it 
        """
        cmd_combobox = QComboBox()
        cmd_combobox.addItems(['Turn telemetry on','Turn telemetry off','Set time GPS', 'Set time UTC', '',''])
        command_layout.addWidget(cmd_combobox)
        
        
        #add send command button
        send_button = QPushButton()
        send_button.setText("SEND COMMAND")
        command_layout.addWidget(send_button)
        
        
        
    
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setGeometry(0,40,1950,950)


       
    def updateData(self, incoming_packet):
        #call updates to all telemetry graphs and labels with a given incoming packet
        pass
    """
    TODO write this class 
    """

    