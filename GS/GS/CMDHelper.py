# Filename: CMDHelper.py
"""
Description: Formats commands according to Mission Guidebook 
Author: Betts, Sam
Date: Dec 6, 2023
"""

"""
TODO: 
do some commmand checks to make sure works as should


"""

from datetime import datetime

cmd = "CMD"
TEAM_ID = "2033"
    

class CMDHelper():
    
    

    
    def __init__(self):
        pass
    
    def cmdToggleTelemetry(self, toggle:str):
        
        
        return f"<{cmd},{TEAM_ID},CX,{toggle}>"
        
    
    def getUTCTime(self):
        utc_time= str(datetime.utcnow())
        utc_time = utc_time[11:19]            
        return utc_time
        
    def cmdSetTime(self, mode:str):
        
        if mode == "GS":
            utc_time= self.getUTCTime()
        elif mode == "GPS":
            utc_time = "GPS"
        else:
            utc_time = None
        #uncomment below to make work correct way
        return f"<{cmd},{TEAM_ID},ST,{utc_time}>"
        #return f"{utc_time}"
   
    def cmdTogglePR(self, mode:str):
        return f"<{cmd},{TEAM_ID},PR,{mode}>"
        
    def cmdSimMode(self, mode:str):
        """
        Mode: ENABLE, ACTIVATE, DISABLE
        command ENABLE and ACTIVATE to enter simulation mode 
        """
        if mode == "ENABLE" or mode == "ACTIVATE" or mode == "DISABLE":
            return f"<{cmd},{TEAM_ID},SIM,{mode}>"
    
    def cmdSimP(self, pressure):
        """
        input pressure value in Pa, XXXXXX, no dec
        TODO: add a way to check to make sure in proper format
        """
        return f"<{cmd},{TEAM_ID},SIMP,{pressure}>"
    
    def cmdCalAlt(self):
        return f"<{cmd},{TEAM_ID},CAL>"
    
    def cmdToggleAudioBcn(self,mode:str):
        """
         Mode is "ON" or "OFF"
         TODO: add checkers to make sure this is correct
        """
        return f"<{cmd},{TEAM_ID},BCN,{mode}>"
        
        