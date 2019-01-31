#********************************************************************
# Ronan Phillips Johns                                              #
# Last Edited: 30/01/2019                                           #
# readUserInput.py                                                  #
# This file reads the user inputed details, calls the method which  #
# will read observations from the internet, and prints these        #
# observations to the desired outputs.                              #
#*******************************************************************#

from observations import readInternet
from observations import readInternetNoTime
from display import printDataToScreen
from display import printDataToFile

def readInput( results ):
    if results.RAMax != None and results.RAMin != None and results.DECMax != None and results.DECMin != None:
        if results.TIMEMax == None or results.TIMEMin == None or results.Duration == None:
            dictionary = readInternetNoTime( results.RAMin, results.RAMax, results.DECMin, results.DECMax )
        else:
            dictionary = readInternet( results.RAMin, results.RAMax, results.DECMin, results.DECMax, results.TIMEMin, results.TIMEMax, results.Duration )
        x = 1
        if results.printToScreen != None:
            printDataToScreen( dictionary, x )
        if results.outfile != None:
            printDataToFile( dictionary, results.outfile, x )
    else:
        if results.outfile == None and results.inputfile == None:
            print("\nError - when entering location details, you must enter both max and min coordinates for right ascension and declination\n")
