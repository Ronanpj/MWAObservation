#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 30/01/2019                                           #
# readFromFile.py                                                   #
# This file will read information from file, and will print the     #
# data to the screen and to file, if the user chooses, through the  #
# calling of methods in other files.                                #
#*******************************************************************#

from astropy.io import ascii
from observations import readInternet
from observations import readInternetNoTime
from display import printDataToScreen
from display import printDataToFile
import csv

def readFile( results ):
    if results.inputfile != None:
        #Execute only if the user wishes to read info from file
        try:
            data = ascii.read(results.inputfile)
            wordList = (open(results.inputfile).readline()).split(" ")
            stringCount = len(wordList)
            count = len(open(results.inputfile).readlines())
        except:
            print("\nError - could not read file correctly\n")
            return
        x = 0
        for i in range(0, count - 1):
            x = i + 1
            if stringCount <= 6:
                dictionary = readInternetNoTime( data["minRa"][i], data["maxRa"][i], data["minDec"][i], data["maxDec"][i] )
            else:
                dictionary = readInternet( data["minRa"][i], data["maxRa"][i], data["minDec"][i], data["maxDec"][i], data["minTime"][i], data["maxTime"][i], data["duration"][i] )

            if results.printToScreen != None:
                printDataToScreen( dictionary, x )
            
            if results.outfile != None:
                printDataToFile( dictionary, results.outfile, x )
                

