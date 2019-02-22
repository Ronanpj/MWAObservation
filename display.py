#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 19/02/2019                                           #
# display.py                                                        #
# This file prints the imported json data into a human readable     #
# table                                                             #
#*******************************************************************#

from tabulate import tabulate
from astropy.table import Table


def printDataToScreen( data, x, wordList ):
    
    print("\n\nName: %s \n" % x)
    if ("minRA" in wordList) and ("maxRA" in wordList) and ("minDEC" in wordList) and ("maxDEC" in wordList):
        print(tabulate(data, headers = ["Observation ID", "Observation Name", "Creator", "Project ID", "Right Ascension", "Declination", "Start Time (UTC)", "Frequency (MHz)", "Correlation Mode", "Duration (sec)"]))
    else:
        print(tabulate(data, headers = ["Observation ID", "Observation Name", "Creator", "Project ID", "Right Ascension", "Declination", "Start Time (UTC)", "Frequency (MHz)", "Correlation Mode", "Duration (sec)", "Offset from pointing centre"]))

#The module 'printDataToScreen' prints each observation of the searched for star(s) to the terminal screen
#It uses tabulate to organise the data into an easy to read table



def printDataToFile( data, outfile ):    
    Table.write(data, outfile, overwrite = True)
