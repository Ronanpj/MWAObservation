#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 07/02/2019                                           #
# observations.py                                                   #
# This file reads the required information from the MWA internet    #
# website, and returns this information to userInput.py. The two    #
# modules in this file both do the same thing, except               #
# readInternet() includes time domensions, whilst                   #
# readInternetNoTime() only uses location details                   #
#*******************************************************************#

import urllib.request
import urllib.error
import json


def readInternet( minRa, maxRa, minDec, maxDec, minTime, maxTime, duration ):
    BASEURL = 'http://mwa-metadata01.pawsey.org.au/metadata/find/?'
    #'BASEURL' is part of the URL for the MWA data base which is used no matter which variables are entered
    
    try:
        result = json.load(urllib.request.urlopen(BASEURL + '&minra=' + str(minRa) + '&maxra=' + str(maxRa) + '&mindec=' + str(minDec) + '&maxdec=' + str(maxDec) + '&mintime=' + str(minTime) + '&maxtime=' + str(maxTime) + '&minduration=' + str(duration) + '&pagesize=200'))
        #This opens the data base and extracts the required observations
    except urllib.request.URLError as error:
        print("HTTP error from server: code = %d, response: \n %s" % (error.code, error.read()))
        return
    except urllib.request.URLError as error:
        print(" URL or network error: %s" % error.reason)
        return
    return result



def readInternetNoTime( minRa, maxRa, minDec, maxDec ):
    BASEURL = 'http://mwa-metadata01.pawsey.org.au/metadata/find?'
    #'BASEURL' is part of the URL for the MWA data base which is used no matter which variables are entered
    
    try:
        result = json.load(urllib.request.urlopen(BASEURL + '&minra=' + str(minRa) + '&maxra=' + str(maxRa) + '&mindec=' + str(minDec) + '&maxdec=' + str(maxDec) + '&pagesize=200'))
        #This opens the data base and exracts the required observations

    except urllib.request.URLError as error:
        print("HTTP error from server: code = %d, response: \n %s" % (error.code, error.read()))
        return
    except urllib.request.URLError as error:
        print(" URL or network error: %s" % error.reason)
        return
    return result

