# Filename: CMDHelper.py
"""
Description: Formats commands according to Mission Guidebook 
Author: Betts, Sam
Date: Dec 6, 2023
"""

"""
TODO: 

"""

from datetime import datetime

on = "ON"
off = "OFF"
cmd = "CMD"
TEAM_ID = "2033"
    

class CMDHelper():
    
    

    
    def __init__(self):
        pass
    
    def cmdSetTime(self, mode:str):
        
        if mode == "GS":
            utc_time= str(datetime.utcnow())
            utc_time = utc_time[11:19]
        elif mode == "GPS":
            utc_time = "GPS"
        else:
            utc_time = None
        
        return f"{cmd},{TEAM_ID},ST,{utc_time}"

    def cmdToggleTelemetry(self, toggle:str):
        
        
        return f"{cmd},{TEAM_ID},CX,{toggle}"
        
        
        
        