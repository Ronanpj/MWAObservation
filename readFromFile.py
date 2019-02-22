#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 22/02/2019                                           #
# readFromFile.py                                                   #
# This file will read information from file, and will print the     #
# data to the screen and to file, if the user chooses, through the  #
# calling of methods in other files.                                #
#*******************************************************************#

from astropy.table import Table, Column
from observations import readInternet, readInternetNoTime
from display import printDataToScreen, printDataToFile
from calcCoordinates import calcMinMax, checkSeperation
from addToDictionary import addUTCColumn, addFurtherInformation
import warnings
import numpy as np
import csv
from astropy.time import Time


def readFile( results ):
    
    warnings.filterwarnings("ignore")
    #The table used in this function truncates the start time string, and outputs a warning each time it does this. I have simply turned warnings off so that this is not output to screen
    
    if results.inputfile != None:
        #Execute only if the user wishes to read info from file
        
        try:
            data = Table.read(results.inputfile)
            #data contains the contents of the file
            wordList = open(results.inputfile).readline()
            #wordList represents the first line of the file, and is used to determine if the file contains details on the time of the observation, or just the location
            count = len(open(results.inputfile).readlines())
            #count determines the number of locations the user wants to check for in the MWA database


            obsID = Column(np.arange(count - 1), name = 'ObservationID', dtype = int)
            obsName = Column(np.arange(count - 1), name = 'ObservationName', dtype = str)
            Creator = Column(np.arange(count - 1), name = 'Creator', dtype = str)
            projectID = Column(np.arange(count - 1), name = 'ProjectID', dtype = str)
            RA = Column(np.arange(count - 1), name = 'RightAscension', dtype = float)
            DEC = Column(np.arange(count - 1), name = 'Declination', dtype = float)
            startTime = Column(np.arange(count - 1), name = 'StartTime(UTC)', dtype = str)
            Frequency = Column(np.arange(count - 1), name = 'Frequency(MHz)', dtype = str)
            mode = Column(np.arange(count - 1), name = 'CorrelationMode', dtype = str)
            duration = Column(np.arange(count - 1), name = 'Duration(sec)', dtype = int)
            
            if ("minRA" not in wordList) and ("maxRA" not in wordList) and ("minDEC" not in wordList) and ("maxDEC" not in wordList):
                #Only execute if the user does a cone search
                Offset = Column(np.arange(count - 1), name = 'OffsetFromPointingCentre', dtype = str)

            #The above code creates the column objects needed to add columns to the astropy table


            data.add_column(obsID)
            data.add_column(obsName)
            data.add_column(Creator)
            data.add_column(projectID)
            data.add_column(RA)
            data.add_column(DEC)
            data.add_column(startTime)
            data.add_column(Frequency)
            data.add_column(mode)
            data.add_column(duration)
            
            if ("minRA" not in wordList) and ("maxRA" not in wordList) and ("minDEC" not in wordList) and ("maxDEC" not in wordList):
                #Only executre if the user does a cone search
                data.add_column(Offset)

            #The above code adds the columns to the astropy table

            listToHoldObservations = []
            #This holds each observation returned from the internet search
            observationLineNumber = []
            #This holds the file line number that each observation occured on
        
            checkError = "False"
            #This checks whether the observations were returned from the internet correctly

        except Exception as e:
            #This prints the error to terminal screen
            print(e)
            return
        
        
        for i in range(0, count - 1):

            if ("minRA" in wordList) and ("maxRA" in wordList) and ("minDEC" in wordList) and ("maxDEC" in wordList):
                #Only execute if the user does a box search
                coordinates = [data["minRA"][i], data["maxRA"][i], data["minDEC"][i], data["maxDEC"][i]]

            else:
                #Execute if the user does a cone search
                coordinates = calcMinMax( data["RA"][i], data["DEC"][i], data["Radius"][i] )


            if ("minTime" in wordList) and ("maxTime" in wordList) and ("duration" in wordList):
                #Only execute if all time details are included
                dictionary = readInternet( coordinates[0], coordinates[1], coordinates[2], coordinates[3], data["minTime"][i], data["maxTime"][i], data["duration"][i] )
            
            else:
                #Execute if time details are not included
                dictionary = readInternetNoTime( coordinates[0], coordinates[1], coordinates[2], coordinates[3] )
            
            
            if dictionary != None:
                
                dictionary = addUTCColumn( dictionary )
                #This adds a UTC time column to the data
                dictionary = addFurtherInformation( dictionary )
                #Add further information to the dictionary
                
                if ("minRA" not in wordList) and ("maxRA" not in wordList) and ("minDEC" not in wordList) and ("maxDEC" not in wordList):
                    #Only execute if the user does a cone search
                    dictionary = checkSeperation( dictionary, data["RA"][i], data["DEC"][i], data["Radius"][i] )
                
                #Filter all observations which are outside of the primary beam
                starName = data["starName"][i]
                
                
                if results.printToScreen != None:
                #Print to screen 
                    printDataToScreen( dictionary, starName, wordList )
 

                if len(dictionary) != 0:
                    #Only execute if an observation is returned from the data base
                    listToHoldObservations.append(dictionary)
                    observationLineNumber.append(i)


            else:
                print("\nError - 'dictionary' has not been filled properly")
                checkError = "True"
                
            

        if checkError != "True" and results.outfile != None:
            #Only execute if the observations have been returned correctly, and the user wishes to print to file
            listOfLines = []
            #Used to hold the lines that the observations are on


            for i in range(0, len(listToHoldObservations)):
                numberOfRowsToAdd = 0
                rowToAdd = data[observationLineNumber[i]]
                #Add rows to the astropy table

                for j in range(0, len(listToHoldObservations[i])):
                    data.insert_row(observationLineNumber[i], rowToAdd)
                    #Insert the rows to the table
                    numberOfRowsToAdd = numberOfRowsToAdd + 1
                    #Determine how many rows have been added

                for j in range(0, numberOfRowsToAdd):
                    data['ObservationID'][observationLineNumber[i] + j] = int( listToHoldObservations[i][j][0] )
                    data['ObservationName'][observationLineNumber[i] + j] = str( listToHoldObservations[i][j][1] )
                    data['Creator'][observationLineNumber[i] + j] = str( listToHoldObservations[i][j][2] )
                    data['ProjectID'][observationLineNumber[i] + j] = str( listToHoldObservations[i][j][3] )
                    data['RightAscension'][observationLineNumber[i] + j] = float( listToHoldObservations[i][j][4] )
                    data['Declination'][observationLineNumber[i] + j] = float( listToHoldObservations[i][j][5] )
                    data['StartTime(UTC)'][observationLineNumber[i] + j] = str( listToHoldObservations[i][j][6] )
                    data['Frequency(MHz)'][observationLineNumber[i] + j] = str( listToHoldObservations[i][j][7] )
                    data['CorrelationMode'][observationLineNumber[i] + j] = str( listToHoldObservations[i][j][8] )
                    data['Duration(sec)'][observationLineNumber[i] + j] = int( listToHoldObservations[i][j][9] )
                    
                    if ("minRA" not in wordList) and ("maxRA" not in wordList) and ("minDEC" not in wordList) and ("maxDEC" not in wordList):
                        #Only execute if the user does a cone search
                        data['OffsetFromPointingCentre'][observationLineNumber[i] + j] = listToHoldObservations[i][j][10] 
                    listOfLines.append(j + observationLineNumber[i])   
                    #The above code adds the observation data to the astropy table
                    

            if ("minRA" not in wordList) and ("maxRA" not in wordList) and ("minDEC" not in wordList) and ("maxDEC" not in wordList):
                #Only execute if the user does a cone search
                count = len(data["RA"])
                
            else:
                count = len(data["minRA"])
            #The above code gets the new length of the astropy table


            for i in range(0, count):
                
                correction = "Yes"
                #Used to determine if a corrrection to the table is needed

                for j in range(0, len(listOfLines)):
                    
                    if i == listOfLines[j]:
                        correction = "No"
                        #A correction is not needed if the row has an observation on it

                if correction == "Yes":
                    data['ObservationID'][i] = 0
                    data['ObservationName'][i] = "0"
                    data['Creator'][i] = "0"
                    data['ProjectID'][i] = "0"
                    data['RightAscension'][i] = 0
                    data['Declination'][i] = 0
                    data['StartTime(UTC)'][i] = "0"
                    data['Frequency(MHz)'][i] = "0"
                    data['CorrelationMode'][i] = "0"
                    data['Duration(sec)'][i] = 0
                    
                    if ("minRA" not in wordList) and ("maxRA" not in wordList) and ("minDEC" not in wordList) and ("maxDEC" not in wordList):
                        #Only execute if the user does a cone search
                        data['OffsetFromPointingCentre'][i] = "0"
                    #The above code changes all data that is not an observation to 0

            printDataToFile( data, results.outfile )
            #Print the data
