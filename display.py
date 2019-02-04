#*******************************************************************#
# Ronan Phillips Johns                                              #
# Last Edited: 31/01/2019                                           #
# display.py                                                        #
# This file prints the json data imported into a human readable     #
# table                                                             #
#*******************************************************************#

from tabulate import tabulate


def printDataToScreen( data, x ):
    print("\n\nStar number: %d \n" % x)
    print(tabulate(data, headers = ["Observation ID", "Observation Name", "Creator", "Project ID", "Right Ascension", "Declination", "Time (UTC)", "Frequency (MHz)", "Correlation Mode"]))
#The module 'printDataToScreen' prints each observation of the searched for star(s) to the terminal screen
#It uses tabulate to organise the data into an easy to read table


def printDataToFile( data, outfile, x ):    
    fileWrite = open(outfile, "a")
    fileWrite.write("\n\nStar number: %d \n" % x)
    fileWrite.write(tabulate(data, headers = ["Observation ID", "Observation Name", "Creator", "Project ID", "Right Ascension", "Declination", "Time (UTC)", "Frequency (MHz)", "Correlation Mode"]))
#The module 'printDataToFile' prints each observation of the searched for star(s) to the file desired by the user
#It uses tabulate to organise the data into an easy to read table
#'a' is used so as to append the data to the file, instead of overwriting it
