#********************************************************************
# Ronan Phillips Johns                                              #
# Last Edited: 05/02/2019                                           #
# readUserInput.py                                                  #
# This file reads the user inputed details, calls the method which  #
# will read observations from the internet, and prints these        #
# observations to the desired outputs.                              #
#*******************************************************************#

from observations import readInternet, readInternetNoTime
from display import printDataToScreen, printDataToFile
from calcCoordinates import calcMinMax, checkSeperation
from addToDictionary import addUTCColumn, addFurtherInformation


def readInput( results ):
    
    if results.RA != None and results.DEC != None and results.Radius != None:
        #Only execute if user has inputed location details correctly

        coordinates = calcMinMax( int(results.RA), int(results.DEC), int(results.Radius) )
        #coordinates holds the min and max right ascension and declination of each location given

        if results.TIMEMax == None or results.TIMEMin == None or results.Duration == None:
            #Execute if time details are not entered by the user

            dictionary = readInternetNoTime( coordinates[0], coordinates[1], coordinates[2], coordinates[3] )
        #dictionary holds all information on the current observation

        else:
            #Execute only if the user enteres all time details correctly

            dictionary = readInternet( coordinates[0], coordinates[1], coordinates[2], coordinates[3], results.TIMEMin, results.TIMEMax, results.Duration )
            #dictionary holds all information on the current observation

        x = 1
        #x is used to represent the star number - for output readability

        dictionary = checkSeperation( dictionary, int(results.RA), int(results.DEC), int(results.Radius) )
        #Filter all the observations which are outside of the radius of the star

        dictionary = addUTCColumn( dictionary )
        #Add time to the list of details for each star

        dictionary = addFurtherInformation( dictionary )
        #Add further information to the data such as frequency and correlation mode

        if results.printToScreen != None:
            #Execute if the user wishes to print to screen
            printDataToScreen( dictionary, x )

        if results.outfile != None:
            #Execute if the user wishes to print to file
            printDataToFile( dictionary, results.outfile, x )

    else:
        if results.inputfile == None:
            #Output error message if data is not read in from file and input location details are not entered correctly
            print("\nError - when entering location details, you must enter right ascension, declination, and radius\n")
