#********************************************************************#
# Ronan Phillips Johns                                               #
# Last Edited: 07/02/2019                                            #
# Main.py                                                            #
# This file facilitates the execution and running of the entire      #
# program                                                            #
#********************************************************************#

from observations import readInternet
from readFromFile import readFile
from readUserInput import readInput
import argparse
import sys

epilog = 'When entering time and location details on the command line, you must do either of the following: Enter only location details, and no time details, or: Enter all location details and all time details. Doing otherwise will result in an error'



parser = argparse.ArgumentParser(epilog=epilog, prefix_chars='+-')
group1 = parser.add_argument_group()

group1.add_argument('-o', dest = 'outfile', action = 'store', help = 'output filename', default = None)
#Create argument for information to be printed to file (outfile = name of output file)

group1.add_argument('-i', dest = 'inputfile', action = 'store', help = 'input filename', default = None)
#Create argument for information to be read from file (inputfile = name if the input file)

group1.add_argument('-p', dest = 'printToScreen', action = 'store', help = 'Print to screen or not. Enter yes if you do wish to print to screen', default = None)
#Create argument for observations to be printed to screen or not

group1.add_argument('+r', dest = 'RA', action = 'store', help = 'The right ascension of the location', default = None)
#Create argument for the right ascension

group1.add_argument('+d', dest = 'DEC', action = 'store', help = 'The declination of the location', default = None)
#Create argument for the declination

group1.add_argument('+R', dest = 'Radius', action = 'store', help = 'The radius of the location coordinates', default = None)
#Create argument for the radius

group1.add_argument('-t', dest = 'TIMEMin', action = 'store', help = 'Minimum limit of start time in GPS seconds', default = None)
#Create argument for the minimum start time of observation

group1.add_argument('+t', dest = 'TIMEMax', action = 'store', help = 'Maximum limit of start time in GPS seconds', default = None)
#Create argument for the maximum start time of observation

group1.add_argument('-l', dest = 'Duration', action = 'store', help = 'Duration of observation', default = None)
#Create argument for the duration of observation



results = parser.parse_args()
#Let the command line arguments be stored in 'results'


#see if there is an 'argparse' way of detecting no input
if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit()

readFile( results )
#This will check if the user has chosen to read from file, and will do so if desired

readInput( results )
#This will check if the user has chosen to read from the command line, and will do so if desired
