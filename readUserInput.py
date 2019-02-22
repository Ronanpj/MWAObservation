#********************************************************************
# Ronan Phillips Johns                                              #
# Last Edited: 22/02/2019                                           #
# readUserInput.py                                                  #
# This file reads the user inputed details, calls the method which  #
# will read observations from the internet, and prints these        #
# observations to the desired outputs.                              #
#*******************************************************************#

from observations import readInternet, readInternetNoTime
from display import printDataToScreen, printDataToFile
from calcCoordinates import calcMinMax, checkSeperation
from addToDictionary import addUTCColumn, addFurtherInformation
from astropy.table import Table, Column
import numpy as np

def readInput( results ):
    
    if (results.RA != None and results.DEC != None and results.Radius != None and results.minRA == None) or (results.minRA != None and results.maxRA != None and results.minDEC != None and results.maxDEC != None):
        #Only execute if user has inputed location details correctly


        if results.RA != None:
            #Only execute if the user does a cone search
            coordinates = calcMinMax( int(results.RA), int(results.DEC), int(results.Radius) )
        
        else:
            #Execute if the user does a box search
            coordinates = [results.minRA, results.maxRA, results.minDEC, results.maxDEC]


        if results.TIMEMax == None or results.TIMEMin == None or results.Duration == None:
            #Execute if time details are not entered by the user
            dictionary = readInternetNoTime( coordinates[0], coordinates[1], coordinates[2], coordinates[3] )
            #dictionary holds all information on the current observation


        else:
            #Execute only if the user enteres all time details correctly
            dictionary = readInternet( coordinates[0], coordinates[1], coordinates[2], coordinates[3], results.TIMEMin, results.TIMEMax, results.Duration )
            #dictionary holds all information on the current observation


        dictionary = addUTCColumn( dictionary )
        #Add time to the list of details for each star
        dictionary = addFurtherInformation( dictionary )
        #Add further information to the data such as frequency and correlation mode
        
        
        if results.RA != None:
            #Only execute if the user does a cone search
            dictionary = checkSeperation( dictionary, int(results.RA), int(results.DEC), int(results.Radius) )
            #Filter all the observations which are outside of the radius of the star


        if results.printToScreen != None:
            #Execute if the user wishes to print to screen

            if results.RA != None:
                #Only execute if the user does a cone search
                printDataToScreen( dictionary, results.starName, "None" )

            else:
                #Execute if the user does a box search
                printDataToScreen( dictionary, results.starName, "minRAmaxRAminDECmaxDEC" )


        if results.outfile != None:
            #Execute if the user wishes to print to file
            
            data = Table()
            #Create an astropy table
            headings = []
            #Create a list to hold all the headings for the table

            if results.RA != None:
                #Only execute if the user does a cone search
                headings.append( Column(np.arange(len(dictionary)), name = 'RA', dtype = float) )
                headings.append( Column(np.arange(len(dictionary)), name = 'DEC', dtype = float) )
                headings.append( Column(np.arange(len(dictionary)), name = 'Radius', dtype = float) )
            
            elif results.minRA != None:
                #Only execute if the user does a box search
                headings.append( Column(np.arange(len(dictionary)), name = 'minRA', dtype = float) )
                headings.append( Column(np.arange(len(dictionary)), name = 'maxRA', dtype = float) )
                headings.append( Column(np.arange(len(dictionary)), name = 'minDEC', dtype = float) )
                headings.append( Column(np.arange(len(dictionary)), name = 'maxDEC', dtype = float) )

            if results.TIMEMin != None:
                #Only execute if the user enteres time details
                headings.append( Column(np.arange(len(dictionary)), name = 'minTime', dtype = int) )
                headings.append( Column(np.arange(len(dictionary)), name = 'maxTime', dtype = int) )
                headings.append( Column(np.arange(len(dictionary)), name = 'duration', dtype = int) )
            
            headings.append( Column(np.arange(len(dictionary)), name = 'starName', dtype = str) )
            #The above code creates all the necessary column objects for the astropy table


            obsID = Column(np.arange(len(dictionary)), name = 'ObservationID', dtype = int)
            obsName = Column(np.arange(len(dictionary)), name = 'ObservationName', dtype = str)
            Creator = Column(np.arange(len(dictionary)), name = 'Creator', dtype = str)
            projectID = Column(np.arange(len(dictionary)), name = 'ProjectID', dtype = str)
            RA = Column(np.arange(len(dictionary)), name = 'RightAscension', dtype = float)
            DEC = Column(np.arange(len(dictionary)), name = 'Declination', dtype = float)
            startTime = Column(np.arange(len(dictionary)), name = 'StartTime(UTC)', dtype = str)
            Frequency = Column(np.arange(len(dictionary)), name = 'Frequency(MHz)', dtype = str)
            mode = Column(np.arange(len(dictionary)), name = 'CorrelationMode', dtype = str)
            duration = Column(np.arange(len(dictionary)), name = 'Duration(sec)', dtype = int)
            
            if results.RA != None:
                #Only execute if the user does a cone search
                Offset = Column(np.arange(len(dictionary)), name = 'OffsetFromPointingCentre', dtype = str)

            
            for i in range(0, len(headings)):
                data.add_column(headings[i])
                #Add all the column objects to the astropy table

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

            if results.RA != None:
                #Only execute if the user does a cone search
                data.add_column(Offset)
            
            #The above code adds all the columns to the astropy table


            if results.RA != None:
                #Only execute if the user does a cone search
                data['RA'] = results.RA
                data['DEC'] = results.DEC
                data['Radius'] = results.Radius
            
            if results.minRA != None:
                #Only execute if the user does a box search
                data['minRA'] = results.minRA
                data['maxRA'] = results.maxRA
                data['minDEC'] = results.minDEC
                data['maxDEC'] = results.maxDEC

            if results.TIMEMin != None:
                #Only execute if the user enteres time details
                data['minTime'] = results.TIMEMin
                data['maxTime'] = results.TIMEMax
                data['duration'] = results.Duration

            data['starName'] = results.starName

            for i in range(0, len(dictionary)):
                data['ObservationID'][i] = dictionary[i][0]
                data['ObservationName'][i] = dictionary[i][1]
                data['Creator'][i] = dictionary[i][2]
                data['ProjectID'][i] = dictionary[i][3]
                data['RightAscension'][i] = dictionary[i][4]
                data['Declination'][i] = dictionary[i][5]
                data['StartTime(UTC)'][i] = str( dictionary[i][6] )
                data['Frequency(MHz)'][i] = dictionary[i][7]
                data['CorrelationMode'][i] = dictionary[i][8]
                data['Duration(sec)'][i] = dictionary[i][9]
                
                if results.RA != None:
                    #Only execute if the user does a cone search
                    data['OffsetFromPointingCentre'][i] = dictionary[i][10] 
            
            #The above code adds all the observation data to the astropy table


            if results.printToScreen != None and results.outfile != None:
                #This renames the output file for the command line query
                temp = results.outfile.split('.')
                temp1 = temp[0] + 'FromCommandLine' + '.' + temp[1]
                
            else:
                temp1 = results.outfile


            printDataToFile( data, temp1 )
            #Print the data to file
    else:
        
        if results.inputfile == None:
            #Output error message if data is not read in from file and input location details are not entered correctly
            print("\nError - when entering location details, you must enter right ascension, declination, and radius\n")
