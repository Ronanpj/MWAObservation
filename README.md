# Program To Search The MWA Database

Author: Ronan Phillips Johns

## Purpose
This program is designed to read, from file and or from the command line, a list of observation queries. These queries contain information regarding the location of one or more stars (in right ascension and declination), the time and duration of the desired observation of these star(s) (In GPS seconds and seconds respectively), and the name of the star(s). The program imports this information to the database of the MWA telescope, which returns a list of observations which correspond to the queries, in JSON format. The program then collects further information from a second MWA database using the obsID of each observation, before parsing the data into a human readable table. 


##Running The Program
To run the program, a number of command line parameters must be used. Simply running the program without command arguments (python3 Main.py) will result in a help message being displayed. To read queries from file, use the argument -i followed by the file name (eg. python3 Main.py -i data.csv). To read star information from the command line, use the arguments +r (right ascension), +d (declination), +R (radius), -t (minimum start time), +t (maximum start time), and -l (duration). The time details are not essential - if they are not entered, the program will display all observations of the desired location. To display the observation information to screen, use the argument -p followed by yes (eg python3 Main.py -p yes -i data.txt). To output the observation information to file, use the argument -o followed by the file name (eg. python3 Main.py -o output.csv -i data.txt).


When reading information from file or from the command line, ensure the duration variable does not contain any decimal values - the database only accepts integer values.

Always enter a name for the query - if it is a star, use the star's name, if you do not know the name of the location simply enter 'unknown'


## Examples
''' 
         python3 Main.py -o output.csv -i data.csv
		This will read from file, and print to file

          python3 Main.py -p yes -i data.csv
		This will read from file, and print to screen

          python3 main.py -o output.csv -p yes -i data.csv
		This will read from file, print to file, and print to screen

	  python3 Main.py -o output.csv -r 164 +r 165 -d 7 +d 8 -N unknown
		This will display all observations of the location entered  

	  python3 Main.py -p yes -r 164 +r 165 -d 7 +d 8 -t 1093589775 +t 1093589777 -l 240 -N moon
		This will print all observations of that location within the specified time to screen
'''



# Overview

The aim of this program is to automate the searching for large numbers of observations from the MWA database. The program can read large numbers of observation queries at once, and return all the observations from the database which correspond to these queries. Any errors in the file are accounted for, and any queries which do not correspond with MWA observations are ignored. Location details must always be entered for each query, while time details are optional.

Data can be entered into the program in two ways - first, you can define the name of an input file containing all the necessary information (this method can read large quantities of data at once), or you can define just one query at once using the command line. Both methods can be used at the same time. Observations are displayed in an easy to read table, and can be printed to screen, file, or both.

The program uses a variety of different packages, including Astropy, Units, and Tabulate. The code is spread throughout a variety of different files, but is controlled initially by the file ‘Main.py’. 

The input parameters have the following units:
    • Right ascension – Decimal degrees
    • Declination – Decimal degrees
    • Radius – Degrees
    • Minimum start time – Seconds
    • Maximum start time – Seconds
    • Duration – Seconds 
    • starName – Name of star



## Running The Program

The program is run directly from the command line – all parameters needed for the program are entered as command arguments. If no arguments are entered, a help message is displayed to terminal screen (shown below). The queries read from file are always displayed before the query from the command line.
Command arguments: 
    • ‘-p’ defines whether the information is printed to screen. If this argument is defined at all, then the observations are printed. Do not define this argument if you do not want the information printed to screen
    • ‘-i’ defines the name of the input file containing the observation queries. The argument definition must be equal to a file name within the same directory as the program
    • ‘-o’ defines the name of the output file the observations will be printed to. If you do not with to print to file, simply do not define this argument
    • ‘+r’ defines the right ascension of the command line query
    • ‘+d’ defines the declination of the command line query
    • ‘+R’ defines the radius of the command line query
    • ‘-t’ defines the minimum start time of the command line query
    • ‘+t’ defines the maximum start time of the command line query 
    • ‘-l’ defines the duration of the command line query
    • ‘-N’ defines the name of the star

Examples:
'''
    • python3 Main.py -o output.txt -p yes -i data.txt
      This reads from the file data.txt, and prints to the file output.txt and prints to terminal screen
      
    • python3 Main.py -o output.txt +r 165 +d 8 +R 3  -N unknown
      This reads a single query from the command line, with the star name unknown, and prints to the file output.txt
      
    • python3 Main.py -p yes -i data.txt +r 165 +d 8 +R 3  -N unknown
      This reads from the file data.txt and from the command line, with the command line query being of an unknown star name, and prints all data to terminal screen 
'''


## Input File Requirements

The input file must be formatted to have the correct headings, otherwise the program will not be able to read it properly. The following are the only acceptable headings:
    • RA
    • DEC
    • Radius
    • minTime
    • maxTime
    • duration
    • starName
      
Any changes in spelling, grammar, or case to these headings will result in a file read error. The order in which the columns are listed, and the space between column headings, does not matter – ensure that each line is a separate query, that each column contains only one type of information, and that the information beneath each column heading is neat and orderly, and the program will read the file correctly. Duration must be an integer, not a decimal value, otherwise the program will not return a correct result. If copy pasting information from a spreadsheet into a text file, you do not need to modify the data once it has been pasted – the program will read it as is. Ensure no empty lines are present at the bottom of the file, as this will result in a file read error. You must always enter a star name for each query – if the name of the star is unknown, simply enter ‘unknown’ for that query. Below are two crude examples of correctly formatted input files.

'''
RA    DEC    Radius    starName
164    8              10       unknown
 23     100           3        moon
 359    57            1        blue star
 6        19             5       unknown
'''

'''
RA    DEC    Radius    minTime    maxTime    duration    starName
164    8          10          23               24                240           unknown
 23     100       3           1034           1036            8		 moon
 359    57        1            49               99               103		 blue star
 6        19         5           10235         10236          999	  	 unknown
'''

## Displayed Help Message

--This message is displayed when no command line arguments are entered aside from the program name--

usage: Main.py [-h] [-o OUTFILE] [-i INPUTFILE] [-p PRINTTOSCREEN] [+r RA]
               [+d DEC] [+R RADIUS] [-t TIMEMIN] [+t TIMEMAX] [-l DURATION]


optional arguments:
  -h, --help        show this help message and exit

  -o OUTFILE                 output filename
  -i INPUTFILE               input filename
  -p PRINTTOSCREEN  Print to screen or not. Enter yes if you do wish to print
                    to screen
  +r RA                             The right ascension of the location
  +d DEC                          The declination of the location
  +R RADIUS                   The radius of the location coordinates
  -t TIMEMIN                   Minimum limit of start time in GPS seconds
  +t TIMEMAX                 Maximum limit of start time in GPS seconds
  -l DURATION                Duration of observation
  -N STARNAME             Name of the star

When entering time and location details on the command line, you must do
either of the following: Enter only location details, and no time details, or:
Enter all location details and all time details. Doing otherwise will result
in an error



## File Descriptions


addToDictionary.py

    1. addUTCColumn( dictionary )
       This function uses a for loop to cycle through each index contained in the variable ‘dictionary’, and uses the function GPStoUTC (contained in timeConversion) to append a time detail to each index contained in ‘dictionary’.
       Variables:
        ◦ dictionary – Holds all the observations’ information
	
    2. addFurtherInformation( dictionary )
       This function is used to read a second web page, containing further information on each observation. It uses the observation ID of each observation to search for the extra information. The function uses a for loop to circle through ‘dictionary’, so that the extra information can be added to each observation. The function uses urllib.request.urlopen to load the internet page, and json.load to format the returned information. The function then appends frequency, correlation mode, and duration to each observation index in ‘dictionary’. ‘dictionary’ is then returned to the calling method.\
       Variables:
            ▪ BASEURL – This is a string containing the base URL required for each search of this specific web page. The obs ID is then added to the string in each cycle of the for loop
            ▪ result – This holds all the data returned from each internet search
              

calcCoordinates.py

    1. calcMinMax( RA, DEC, radius)
       This method calculates the minimum and maximum coordinates required for the searching of the
	      MWA database, using the right ascension, declination, and radius entered by the user. It firstly finds  	      the minimum and maximum right ascension by subtracting and adding respectively the absolute         
              value of the radius / cos (declination) from the right ascension. It then finds the minimum and                        
              maximum declination by simply subtracting and adding respectively the radius to the declination.
	      The method then uses multiple while loops to ensure all min and max coordinates are within 0 and  
             360 degrees, and adds all 4 coordinates to a list which is returned to the calling method.         
	      Variables:
    • coordinates – This is a list used to hold the minimum and maximum values for the right ascension and declination
    • RAMin – Holds the value for minimum right ascension
    • RAMax – Holds the value for the maximum right ascension
    • DECMin – Holds the value for the minimum declination
    • DECMax – Holds the value for the maximum declination
      
    2. checkSeperation( dictionary, RA, DEC, radius )
       This function checks the separation between the initial coordinate and the coordinate for each separate observation. It loops through each index of the variable ‘dictionary’, so that each observation is considered. If the separation between the queried location and the observation location is greater than the given radius of the query, the observation is discarded. This ensures all observations are within the primary beam of the query. If the separation is within the beam, the offset is added to the list of details about each observation. When the function pops the indexes from the variable ‘dictionary’, each index which remains to be removed must be reduced in value by 1. This ensures the correct index is always removed. The variable dictionary is returned to the calling method, and contains all the information regarding each observation.
	      Variables:
    • initialCoord – This variable represents the SkyCoord object entered by the user, and is needed to calculate the separation between the initial coordinate and the observation coordinate
    • listOfIndexesToRemove – This is a list containing the indexes of eahc observation which has a separation greater than the radius of the primary beam. These indexes are removed from the total list of observations
    • obsCoord – This variable represents the SkyCoord object for the location of each observation, and is used to calculate the separation
    • sep – Represents the separation between the user entered coordinate and the observation coordinate
    • degrees – Represents the separation in degrees


display.py

    1. printDataToScreen( data. X )
       This function uses tabulate to print the entire list of observations contained in the variable data to screen in a nice, easy to read table. 
       Variables:
    • data – This variable holds all of the observations returned from the MWA database and all their details
    • x – This is used to represent the star number – it makes the displayed data more presentable 

    2. printDataToFile( data, outfile, x )
       This function uses tabulate and the built in python file stream functions to print the entire list of observations contained in the variable ‘data’ to the file who’s name is contained in the variable ‘outfile’. 
       Variables:
        ◦ data – This variable holds all the observations returned from the MWA database and all their details
        ◦ outfile – This is a string which represents the name of the file the user wishes to print all the information to
        ◦ x – This is used to represent the star number – it makes the displayed data more presentable


Main.py

This file initiates the running of the program. It imports the package ‘argparse’ to store and manage the command line arguments entered by the user. No matter which arguments are entered, the program will always import the arguments (stored in the variable ‘results’) into the methods readFile() and readInput(), contained in the classes readFromFile.py and readUserInput.py respectively. If the number of command line arguments are less than two, the program will exit.
Variables:
    • parser – This variable is used to parse the command line arguments once they are entered. It is set to equal argparse.ArgumentParser(epilog = epilog, prefix_chars = ‘+-’)
    • group1 – This is used to hold each command line argument
    • results – Used to access each command parameter


observations.py

    1. readInternet( minRa, maxRa, minDec, maxDec, minTime, maxTime, duration )
       This function initiates the first read of the MWA database, and collects the initial details on each observation. It uses json.load to load and format the data from the webpage, alongside urllib.request.urlopen.  The returned information contains all the observations which are within the constraints of the location and time details, and all their relevant information. When it is returned it is not readable, and must be formatted. The variable ‘result’ is returned to the calling function.
       Variables: 
        ◦ BASEURL – This variable is This is a string containing the base URL required for each search of this specific web page. The coordinates are then later added to the variable so as to define the internet search
        ◦ result – This is used to hold all of the information returned from the internet
          
    2. readInternetNoTime( minRa, maxRa, minDec, maxDec )
       This function is exactly the same as the previous function ( readInternet() ), except that no time parameters are added to the URL used in the internet search. This means all observations of the desired location are output, regardless of their start time or duration.


ReadFromFile.py

    1. readFile( results )
       This function reads the input file, and collects all the necessary details before outputting the information to other files. At the beginning of the function, the program checks if the user wishes to read from file or not. If not, the function finishes. Otherwise the function reads the file using ascii, and stores the information in ‘data’. It then creates the variable ‘wordList’ which reads the first line, and splits it whenever it finds whitespace. The variable ‘stringCount’ is then set to the length of ‘wordList’. This is done so that the program can determine whether time details have been entered in the file or not. The function then counts the number of lines in the file so that it knows how many times to iterate the for loop later in the function. If the file could not be read properly, the function exits. The function then loops the same number of times as the number of lines contained in the file – each line represents a separate query, thus each line must be dealt with separately. The function calls calcMinMax() so as to obtain the coordinates in minimum and maximum, and then calls either readInternet() or readInternetNoTime() depending on whether time details are used in the file or not. The function then calls addUTCColumn(), addFurtherInformation(), and checkSeperation(), to add extra details to each observation, and filter all observations which are outside of the primary beam. If the user wishes for the information to be printed to screen, the function will call printDataToScreen(), and if the user wishes to print to file, the function calls printDataToFile().
       Variables:
            ▪ results – This holds all the command line arguments entered by the user
            ▪ data – This hold all the information read from the input file
            ▪ wordList – This contains the headings from the input file, and is split so that the function can determine if the file contains time details or not
            ▪ stringCount – Represents the number of words in the header of the file
            ▪ count – Holds the number of lines in the file, and is used to determine the number of for loop iterations needed
            ▪ x – This represents the star number, ie the iteration number add 1. It is used to format the output of the observations
            ▪ coordinates – This is a list which holds the minimum and maximum right ascension and declination. It is used for calling the readInternet functions
            ▪ dictionary – This is a list, which contains a dictionary in each index, each of which contain all the observations returned from each query contained in the input file. The list is recreated each time the for loop is iterated, thus contains only the details for one query at a time
               


readUserInput.py

    1. readInput( results )
       This function acts in a very similar manner to readFromFile.py, except it deals with only the user inputted query (from the command line). Thus, the function firstly checks if the user has entered ALL of the location details (if they only entered some of them, the function will not continue, and instead display an error message). If the user has entered the location details correctly, the function calls calcMinMax() to convert the location details to minimum and maximum right ascension and declination. It then checks if the user entered time details – if the user entered some of the time details, but not all three, the program will discard all time information and function as if no time details were entered at all. If this is the case, the program then calls readInternetNoTime() and stores the returned information in ‘dictionary’. If the user did enter time details correctly, the function calls readInternet() and stores the returned information in ‘dictionary’. The function then calls addUTCColumn(), addFurtherInformation(), and checkSeperation(), all of which update and add to the information contained in ‘dictionary’. If the user wishes to print to screen and or file, the function will call printDataToScreen() and or printDataToFile().
       Variables:
            ▪ results – This holds all the command line arguments entered by the user
            ▪ coordinates – This is a list which holds the minimum and maximum right ascension and declination. It is used for calling the readInternet functions
            ▪ dictionary – This is a list, which contains a dictionary in each index, each of which contain all the observations returned from each query contained in the input file. The list is recreated each time the for loop is iterated, thus contains only the details for one query at a time
            ▪ x – This represents the star number, and is only used for ease of display


timeConversion.py

    1. GPStoUTC( GPSTime )
       This function simply takes the GPS time parameter and uses the functions built in to astropy.time to convert this parameter to UTC time. The UTC time variable is returned to the calling function.
       Variables:
            ▪ GPSTime – This represents the start time of each observation in GPS time
            ▪ UTCTime – This represents the start time of each observation in UTC time



## How To Modify Output Details

To change the details which are output from the program, you must change a few different pieces of code. 
To remove details:  
    • If you wish to remove observation ID, observation name, creator, project ID, right ascension, or declination, then the detail is returned from the initial read of the MWA database. Each of these details correspond to index 0 to index 5 in each observation list, in the order listed above. To remove one of these details, you must loop through each index of ‘dictionary’ and remove the desired detail from each index of ‘dictionary’. Dictionary is a list, which contains a dictionary in each index. Do this removal once all details have been read from the internet, ie just before the observations are output from the program.  
    • If the detail you wish to remove is not one of the above, then it is one which is collected from the second read of the MWA database. If the detail you wish to remove is the UTC time column, then remove the function call in the method readFile(), contained in readFromFile.py, on line 50, and the function call on line 39 in readInput(), contained in readUserInput.py. If you wish to remove the offset from pointing centre column, you must go to the method checkSeperation() in calcCorrdinates.py, and remove the append to dictionary on line 84. To remove any other detail, you must go to the method addFurtherInformation(), contained in addToDictionary.py. Beginning on line 41, you will see multiple details being appended to ‘dictionary’. Determine which of these details you wish to remove, and simply delete the line of code.  
    • When any detail is removed, regardless of where the detail is sourced from, you must go to display.py. In this file, you must remove the heading which corresponds with the detail you are removing. You must do this in both methods contained in the file. For example if I wish to remove Duration from the output, I must remove “Duration (sec)” from line 15 and line 25. 

To add details:
    • If you have previously removed one of the details returned from the initial call of the MWA database (you will have created a for loop just before the data was output from the program, removing the detail from each index of ‘dictionary’), then simply remove this code.
    • If you have previously removed the UTC time column, then add the function calls which were removed as described above.
    • If you have previously removed the offset from pointing centre column, then add the append to dictionary line, as described above
    • Any other detail you wish to add is returned from the second read of the MWA database. You must go to addFurtherInformation() contained in addToDictionary.py. The detail you wish to add to the output, if it exists at all, is contained in the variable ‘result’. You must find which index of the returned dictionary the detail is contained in, and append this to each index of the variable named ‘dictionary’.
    • Whenever a detail is added to the output, you must go to display.py and add the detail name to the list of headings on line 15 and line 25. For example if I am adding a duration column, I would add “duration (secs)” to the headings. 
    • You must ensure that whenever a detail is added, its position in the dictionary it is held in corresponds to the position of its heading in lines 15 and 25 of display.py. For example if the duration detail is in index 5 of its dictionary, its heading would be the 6th one listed on lines 15 and 
      25.



