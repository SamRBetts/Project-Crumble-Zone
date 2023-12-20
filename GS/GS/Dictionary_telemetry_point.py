# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 19:06:51 2023

@author: bettssr
Dictionary definitions for telemetry points

These are the arrays that will be stored in the telemetry screen to be plotted over time 

"""

telemetry_points = {
     
0:	'TEAM_ID',
1:	 'MISSION_TIME',
2:	 'PACKET_COUNT',
3:	 'MODE',
4:	 'STATE',
5:	 'ALTITUDE',
6:	 'AIR_SPEED',
7:	 'HS_DEPLOYED',
8:	 'PC_DEPLOYED',
9:	 'TEMPERATURE',
10:	 'VOLTAGE',
11:	 'PRESSURE',
12:	 'GPS_TIME',
13:	 'GPS_ALTITUDE',
14:	 'GPS_LATITUDE',
15:	 'GPS_LONGITUDE',
16:	 'GPS_SATS',
17: 'TILT_X',
18:	'TILT_Y',
19:	 'ROT_Z',
20:	 'CMD_ECHO',

    }

"""
1, 5-6 and 9-11 and 13-15 and 17-19 are special - they will be stored in arrays in the telemetry screen 
"""