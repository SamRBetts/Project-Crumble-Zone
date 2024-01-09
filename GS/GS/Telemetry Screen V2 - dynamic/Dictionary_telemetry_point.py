# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 19:06:51 2023

@author: bettssr
Dictionary definitions for telemetry points

These are the arrays that will be stored in the telemetry screen to be plotted over time 

"""

telemetry_points = {
     
'TEAM_ID':          0,
'MISSION_TIME':     1,
'PACKET_COUNT':     2,
'MODE':             3,
'STATE':            4,
'ALTITUDE':         5,
'AIR_SPEED':        6,
'HS_DEPLOYED':      7,
'PC_DEPLOYED':      8,
'TEMPERATURE':      9,
'VOLTAGE':          10,
'PRESSURE':         11,
'GPS_TIME':         12,
'GPS_ALTITUDE':     13,
'GPS_LATITUDE':     14,
'GPS_LONGITUDE':    15,
'GPS_SATS':         16,
'TILT_X':           17,
'TILT_Y':           18,
'ROT_Z':            19,
'CMD_ECHO':         20,

    }

"""
1, 5-6 and 9-11 and 13-15 and 17-19 are special - they will be stored in arrays in the telemetry screen 
"""