#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 07/02/2019                                           #
# timeConversion.py                                                 #
# This file contains all the time conversion methods needed for the #
# program                                                           #
#*******************************************************************#

from astropy.time import Time


def GPStoUTC( GPSTime ):
    #Used to convert GPS time to UTC time
    UTCTime = Time( GPSTime, format = 'gps')
    UTCTime = Time(UTCTime, format = 'iso')
    
    return UTCTime
