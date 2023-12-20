# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 14:58:30 2023

@author: bettssr
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QPainter
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import numpy as np

#default_color = "#A86C6C"
default_color = '#14FF00'
graph_color = '#92E726'
graph_color2 = '#26E7E6'
pen1 = pg.mkPen(color=(graph_color),width=5)
pen2 = pg.mkPen(color=(graph_color2),width=5)


#define some custom label classes a

class TelemetryGraph(PlotWidget):
    def __init__(self, title,x, y,ylabel, parent=None):
        super().__init__(parent)
        self.setBackground('w')
        self.setTitle(title,color="k",size = "20px")
        #pen = pg.mkPen(color=(graph_color),width=5)
      #  print(np.hstack(y[0,:]))
        self.plot(x,y,pen=pen1)
        print(y)
        
              
        styles = {'font-size':'22px'}
        self.setLabel('left', ylabel, **styles)
        self.setLabel('bottom', "time (s)", **styles)   
        
class TelemetryGraph2(PlotWidget):
    def __init__(self, title, x,y,ylabel1, y2, ylabel2, ylabel, parent=None):
        super().__init__(parent)
        self.setBackground('w')
        self.setTitle(title,color="k",size = "20px")
        #pen = pg.mkPen(color=(graph_color),width=5)
        self.addLegend()
        self.plot(x,y,pen=pen1,name=ylabel1)
        self.plot(x,y2,pen=pen2,name=ylabel2)
        
              
        styles = {'font-size':'22px'}
        self.setLabel('left', ylabel, **styles)
        self.setLabel('bottom', "time (s)", **styles)  
        
        


class DataDisplayLabel(QLabel):
      def __init__(self, text,parent=None):
        super().__init__(text, parent)
        self.background_color = default_color
        self.setStyleSheet("font-size: 20px;")  # Set the stylesheet
 

      def paintEvent(self, event):
         painter = QPainter(self)
         painter.fillRect(self.rect(), QColor(self.background_color))
    
         super().paintEvent(event)
         
class DisplayLabel(QLabel):
    def __init__(self, text,parent=None):
        super().__init__(text, parent)
        #self.background_color = default_color
        self.setStyleSheet("font-size: 20px;")  # Set the stylesheet
 




#main window go brrrrrrr
class MainWindow(QMainWindow):
    
    
    

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Telemetry Screen V0")

        main_layout_top = QGridLayout()
        main_layout_bottom = QGridLayout()
        main_layout = QGridLayout()
        
        parameter_layout1 = QVBoxLayout()
        parameter_layout1_b = QVBoxLayout()
        parameter_layout2 = QVBoxLayout()
        parameter_layout2_b = QVBoxLayout()
        
        main_layout.addLayout(main_layout_top, 0,0)  
        main_layout.addLayout(main_layout_bottom, 1,0)
        
        main_layout_top.addLayout(parameter_layout1,0,0)
        main_layout_top.addLayout(parameter_layout1_b,0,1)
        main_layout_top.addLayout(parameter_layout2,0,2)
   
        main_layout_top.addLayout(parameter_layout2_b,0,3)
        
        
        
        #Define all data display labels
        
       
        mis_time_lbl = DataDisplayLabel("hh:mm:ss")
        parameter_layout1_b.addWidget(mis_time_lbl)
        
        GPS_time_lbl = DataDisplayLabel("GPS hh:mm:ss UTC")
        parameter_layout1_b.addWidget(GPS_time_lbl)

        pkt_rx_lbl = DataDisplayLabel("XX")
        parameter_layout1_b.addWidget(pkt_rx_lbl)
        
        cmd_echo_lbl = DataDisplayLabel("LAST CMD GIVEN")
        parameter_layout1_b.addWidget(cmd_echo_lbl)
        
        
        state_lbl = DataDisplayLabel("FLIGHT MODE")
        parameter_layout2_b.addWidget(state_lbl)
        
        HS_dpl_lbl = DataDisplayLabel("YES")
        parameter_layout2_b.addWidget(HS_dpl_lbl)
        
        PS_dpl_lbl = DataDisplayLabel("NO")
        parameter_layout2_b.addWidget(PS_dpl_lbl)
        
        GPS_sats_lbl = DataDisplayLabel("3")
        parameter_layout2_b.addWidget(GPS_sats_lbl)
        
        Mode_dpl_lbl = DataDisplayLabel("Mode")
        parameter_layout2_b.addWidget(Mode_dpl_lbl)
        
        #define all the data labels
        parameter_layout1.addWidget(DisplayLabel("Mission Time"))
        parameter_layout1.addWidget(DisplayLabel("GPS Time"))
        parameter_layout1.addWidget(DisplayLabel("Packets Recieved"))
        parameter_layout1.addWidget(DisplayLabel("CMD Echo"))
        parameter_layout2.addWidget(DisplayLabel("FSW State"))
        parameter_layout2.addWidget(DisplayLabel("HS Deployed"))
        parameter_layout2.addWidget(DisplayLabel("PS Deployed"))
        parameter_layout2.addWidget(DisplayLabel("GPS sats tracking"))
        parameter_layout2.addWidget(DisplayLabel("Mode"))
        
     
        
     
        time = ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        example_data = [1,2,3,5,5,7,7,8,9,9,10,10,10,9,7]
        example2_data= [1,3,3,4,5,7,8,8,9,10,10,11,10,9,8]
        print(example_data)
        
        
        #define all needed graphs with placeholder data
        alt_graph = TelemetryGraph2("Altitude",time,example_data,"Baro", example2_data, "GPS", "m")
        main_layout_bottom.addWidget(alt_graph, 0, 0)
        pressure_baro_graph = TelemetryGraph("Pressure", time, example_data, "Pa")
        main_layout_bottom.addWidget(pressure_baro_graph,1,0)
        lat_GPS_graph = TelemetryGraph("Latitude",time, example_data, "xxx.xx")
        main_layout_bottom.addWidget(lat_GPS_graph, 2,0)
        speed_pitot_graph = TelemetryGraph("Air Speed",time, example_data, "m/s")
        main_layout_bottom.addWidget(speed_pitot_graph, 0,1)
        tilt_graph = TelemetryGraph2("Tilt", time, example_data,"X", example2_data,"Y", "degrees")
        main_layout_bottom.addWidget(tilt_graph,1,1)
        long_GPS_graph = TelemetryGraph("Longitude",time, example2_data, "xxx.xx")
        main_layout_bottom.addWidget(long_GPS_graph, 2,1)
        voltage_graph = TelemetryGraph("Voltage",time,example_data,"V")
        main_layout_bottom.addWidget(voltage_graph,0,2)
        temp_graph = TelemetryGraph("Temperature",time,example_data, "deg F")
        main_layout_bottom.addWidget(temp_graph,1,2)
    
    
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setGeometry(0,40,1950,950)
        
        


def main():
    # Create an application instance
    app = QApplication(sys.argv)
    #window.setGeometry(100, 100, 400, 200)
    
    # Create a label
    #label = QLabel("Altitude", main)
    #label.move(150, 80)
    
    
    main = MainWindow()
    # Show the main window
    main.show()
    
    # Start the application event loop
    app.exec()    


if __name__ == "__main__":
    main()
