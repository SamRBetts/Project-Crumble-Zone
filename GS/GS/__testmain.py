# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 22:01:22 2024

@author: bettssr
"""

# Filename: __main.py
"""
Description: This main application will run all the required code to operate
    test commands on the flight software   

"""

from TestCmdScreen  import TestCmdScreen

import sys
from PyQt5.QtWidgets import QApplication


def main():

    # Create an application instance
    app = QApplication(sys.argv)    
    main = TestCmdScreen()   
    #show main window
    main.show()
    # Start the application event loop
    app.exec() 
    #after done executing: 
    main.xbee.disconnect()
    main.stopTimer()


if __name__ == "__main__":
    main()
    
    
    