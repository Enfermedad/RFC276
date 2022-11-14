import os
import random
import datetime
import time
import socket
import sys 
import getopt
import struct

####
#UNIX timestamps use as Jan 1 1970 as epoch whereas NTP protocol uses Jan 1 1900
####
#SECONDS 1900 to 1970
NTPDELTA = 2208988800.0
##-----------------------##
def system_to_ntp(t=0.0):
    #------#
    # Transform system timestamp to NTP timestamp
    #------#
    t+= NTPDELTA
    return (int(t) <<32) + (int(abs(t-int(t)*(1<<32))))

def ntp_to_system(x=0):
    #------#
    #Transform NTP timestamp to system timestamp
    #------#
    t = float (x>>32) + float(x & 0xffffffff )/(1<<32)
    return t - NTPDELTA
def tfmt(t = 0.0):
        ###
        #Format System Timestamp
        ###

        return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d_%H:%M:%S.%f")
