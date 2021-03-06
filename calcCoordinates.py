#********************************************************************
# Ronan Phillips Johns                                              #
# Last Edited: 22/02/2019                                           #
# calcCoordinates.py                                                #
# This file calculates the min and max right ascension and          #
# declination from the right ascension, declination, and radius     #
# entered by the user.                                              #
#*******************************************************************#


from astropy.coordinates import SkyCoord
from astropy import units as u
from math import cos


def calcMinMax( RA, DEC, radius ):
    coordinates = []
    #Used to hold the min and max right ascension and declination


    RAMin = RA - abs( radius / cos( DEC ) )
    RAMax = RA + abs( radius / cos( DEC ) )
    DECMin = DEC - radius
    DECMax = DEC + radius
    #The above lines of code calculate the minimum and maximum ra and dec from the initial ra and dec and the radius


    while RAMin < 0:
        RAMin = RAMin + 360
    while RAMin > 360:
        RAMin = RAMin - 360
    while RAMax < 0:
        RAMax = RAMax + 360
    while RAMax > 360:
        RAMax = RAMax - 360
    while DECMin < 0:
        DECMin = DECMin + 360
    while DECMin > 360:
        DECMin = DECMin - 360
    while DECMax < 0:
        DECMax = DECMax + 360
    while DECMax > 360:
        DECMax = DECMax - 360
    #The above code ensures the coordinates are within 0 and 360 degrees at all times
    
    
    coordinates.append( RAMin )
    coordinates.append( RAMax )
    coordinates.append( DECMin )
    coordinates.append( DECMax )
    #The above 4 lines add the data to the coordinates list

    return coordinates




def checkSeperation( dictionary, RA, DEC, radius ):
    
    initialCoord = SkyCoord(RA, DEC, unit = 'deg', frame = 'fk5')
    #initialCoord represents the SkyCoord object for the coordinates entered by the user
    listOfIndexesToRemove = []
    #This list is used to hold all the indexe numbers which need to be removed from dictionary


    for x in range(0, len(dictionary)):
        obsCoord = SkyCoord(dictionary[x][4], dictionary[x][5], unit = 'deg', frame = 'fk5')
        #obsCoord represents the SkyCoord object for each observation
        sep = obsCoord.separation( initialCoord )
        #sep represents the seperation between the two SkyCoord objects, initally in D,M,S
        degrees = sep.degree
        #degrees represents the seperation in degrees


        if radius < degrees:
            listOfIndexesToRemove.append(x)
            #Add the index number to the list which needs to be removed
        else:
            dictionary[x].append( sep )
            #Display the offset from the pointing centre, in degrees


    for y in listOfIndexesToRemove:
        dictionary.pop(y)
        #Remove the index from the dictionary

    
        for i in range(0, len(listOfIndexesToRemove)):
            listOfIndexesToRemove[i] = listOfIndexesToRemove[i] - 1
            #When the above index was removed, the entire dictionary length was reduced by one. This results in each index that needs to be removed also requiring to be reduced by 1, otherwise an index error will occur

    return dictionary
