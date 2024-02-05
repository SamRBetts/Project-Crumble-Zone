# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:27:20 2024

@author: bettssr
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class filedialogdemo(QWidget):
   def __init__(self, parent = None):
      super(filedialogdemo, self).__init__(parent)
		
      layout = QVBoxLayout()
      self.btn = QPushButton("Open File")
      self.btn.clicked.connect(self.openFile)
		
      layout.addWidget(self.btn)
      self.le = QLabel("Hello")
		
      layout.addWidget(self.le)
      self.btn1 = QPushButton("Get file object")
      self.btn1.clicked.connect(self.getFile)
      layout.addWidget(self.btn1)
		
      self.contents = QTextEdit()
      layout.addWidget(self.contents)
      self.setLayout(layout)
      self.setWindowTitle("File Dialog demo")
      
      #filepath = QtWidgets.QFileDialog.getOpenFileName(self, 'Hey! Select a File')

		
   def openFile(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Text file (*.txt *.csv)")
      #self.le.setPixmap(QPixmap(fname))
		
   def getFile(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\users/bettssr/documents/github/project-crumple-zone/GS/GS',"Text file (*.txt *.csv)")
      file = open(fname[0])
      print(file.read())
		
   
				
def main():
   app = QApplication(sys.argv)
   ex = filedialogdemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':

   main()