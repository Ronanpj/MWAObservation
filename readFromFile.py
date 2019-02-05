#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 05/02/2019                                           #
# readFromFile.py                                                   #
# This file will read information from file, and will print the     #
# data to the screen and to file, if the user chooses, through the  #
# calling of methods in other files.                                #
#*******************************************************************#

from astropy.io import ascii
from observations import readInternet, readInternetNoTime
from display import printDataToScreen, printDataToFile
from calcCoordinates import calcMinMax, checkSeperation
from addToDictionary import addUTCColumn, addFurtherInformation
import csv

def readFile( results ):
    if results.inputfile != None:
        #Execute only if the user wishes to read info from file
        
        try:
            data = ascii.read(results.inputfile)
            #data contains the contents of the file
            
            wordList = (open(results.inputfile).readline()).split(" ")
            #wordList represents the first line of the file, and is used to determine if the file contains details on the time of the observation, or just the location
            
            stringCount = len(wordList)
            #stringCount represents the number of headings in the file, and thus the details about the star(s) contained in the file
            
            count = len(open(results.inputfile).readlines())
            #count determines the number of locations the user wants to check for in the MWA database
        
        except:
            print("\nError - could not read file correctly\n")
            return
        x = 0
        #x represents the star number - used to make output more appealing
        #try:
        for i in range(0, count - 1):
            coordinates = calcMinMax( data["RA"][i], data["DEC"][i], data["Radius"][i] )
            x = i + 1
            #Increase the star number each time the loop is iterated - each time a new location/time is checked for observation
            if stringCount < 6:
            #Only execute if time details are not included
                dictionary = readInternetNoTime( coordinates[0], coordinates[1], coordinates[2], coordinates[3] )
            else:
        #Execute if time details are included
                dictionary = readInternet( coordinates[0], coordinates[1], coordinates[2], coordinates[3] , data["minTime"][i], data["maxTime"][i], data["duration"][i] )
              
            dictionary = addUTCColumn( dictionary )
            #This adds a UTC time column to the data
           
            dictionary = addFurtherInformation( dictionary )
            #Add further information to the dictionary

            dictionary = checkSeperation( dictionary, data["RA"][i], data["DEC"][i], data["Radius"][i] )


            if results.printToScreen != None:
            #Print to screen 
                printDataToScreen( dictionary, x )
           
            if results.outfile != None:
            #Print to file
                printDataToFile( dictionary, results.outfile, x )
        #except:
            #print("\nError\n")
