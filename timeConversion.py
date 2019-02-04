#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 31/01/2019                                           #
# timeConversion.py                                                 #
# This file contains all the time conversion methods needed for the #
# program                                                           #
#*******************************************************************#

from astropy.time import Time

def GPStoUTC( GPSTime ):
    UTCTime = Time( GPSTime, format = 'gps')
    UTCTime = Time(UTCTime, format = 'iso')
    return UTCTime
