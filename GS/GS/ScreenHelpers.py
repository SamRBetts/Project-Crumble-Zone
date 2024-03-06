# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:37:53 2024

@author: bettssr
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
        self.y2label = y2label
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
        
    def reset(self):
        
        self.clear()
        self.x = [0]  
        self.y1 = [0]
        self.data_line = self.plot(self.x, self.y1, pen=WindowSettings.pen1,name=self.ylabel)        

        #self.data_line.clear()
        if self.doublePlot:
             self.y2 = [0]
             self.data_line2.setData(self.x,self.y2,pen=WindowSettings.pen2,name=self.y2label)

             #  self.data_line2.clear()

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
