# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:16:52 2023

@author: bettssr
"""

from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import numpy as np

pen = pg.mkPen(color=(255, 0, 0))
packet_num =0

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

               
        

        self.graphWidget.setBackground('w')

        
    
        
        
   
    def Plot(self,x_arr,y_arr):
        
        self.index = 0
        self.x_arr = x_arr
        self.y_arr = y_arr
        
        self.x =[x_arr[1]]
        self.y =[y_arr[1]]
        
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)

        #w.timer.timeout.connect(lambda: w.update_plot_data(time[packet_num],pressure_values[packet_num]))
        self.timer.timeout.connect(w.update_plot_data)
        self.timer.start()

        
    def update_plot_data(self):
      
        #self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x_arr[self.index])  # Add a new value 1 higher than the last.
        self.y.append(self.y_arr[self.index])  
        #self.y = self.y[1:]  # Remove the first
        #self.y.append(y)  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.
        self.index=self.index+1

        print(self.index)

    
arr = np.loadtxt("cansat_2023_simp.csv", delimiter=",", dtype=str)
(arr[:,1]) = '2033'

pressure_values = (arr[:,3])
pressure_values= pressure_values.astype(int)
time = np.arange(0,arr.shape[0],1)
    


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.Plot(time,pressure_values)



w.show()
sys.exit(app.exec_())