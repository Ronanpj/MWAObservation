#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 19/02/2019                                           #
# addToDictionary.py                                                #
# This file facilitates the addition of columns to the current      #
# dictionary of observations                                        #
#*******************************************************************#


import urllib.request
import urllib.error
import json
from timeConversion import GPStoUTC


def addUTCColumn( dictionary ):
    for x in range(0, len(dictionary)):
        dictionary[x].append(GPStoUTC(int(dictionary[x][0])))
        # Append a column to the end of each dictionary contained in the 2d dict
    
    return dictionary



def addFurtherInformation( dictionary ):
    BASEURL = 'http://mwa-metadata01.pawsey.org.au/metadata/obs/?obsid='
    #BASEURL is part of the URL for the MWA data base which is used no matter which variables are entered
    

    for x in range(0, len(dictionary)):
        try:
            result = json.load(urllib.request.urlopen(BASEURL + str(dictionary[x][0])))
            #This opens the data base and extracts the required observations
        
        except urllib.request.URLError as error:
            print("HTTP error from server: code = %d, response: \n %s" % (error.code, error.read()))
            return
       
        except urllib.request.URLError as error:
            print(" URL or network error: %s" % error.reason)
            return
 

        dictionary[x].append(result["rfstreams"]["0"]["vsib_frequency"] * 1.28)
        #Add frequency to the data
        dictionary[x].append(result["mode"])
        #Add Correlation Mode to the data
        dictionary[x].append(result["stoptime"] - result["starttime"])
        #Add Duration to the data
    
    return dictionary

