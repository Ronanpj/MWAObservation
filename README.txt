README for the program MWAObservations

Author: Ronan Phillips Johns

Last Edited: 31/01/2019

Purpose: This program is designed to read, either from file or from the command line, information regarding the location of one or more stars (in right ascension and declination), and the time and duration of the desired observation of this star(s) (In GPS seconds and seconds). The program reads the information from the database of the MWA telescope, which returns the observation information in JSON format. The program then parses this data into a human readable table. 

Running the Program: To run the program, a number of command line parameters must be used. Simply running the program without command arguments (python3 Main.py) will result in a help message being displayed. To read star information from file, use the argument -i followed by the file name (eg. python3 Main.py -i data.csv). To read star information from the command line, use the arguments -r (minimum right ascension), +r (maximum right ascension), -d (minimum declination), +d (maximum declination), -t (minimum start time), +t (maximum start time), and -l (duration). The time details are not essential - if they are not entered, the program will display all observations of the desired location. To display the observation information to screen, use the argument -p followed by yes (eg python3 Main.py -p yes). To display the observation information to file, use the argument -o followed by the file name (eg. python3 Main.py -o output.csv).

Examples: python3 Main.py -o output.csv -i data.csv
		This will read from file, and print to file

          python3 Main.py -p yes -i data.csv
		This will read from file, and print to screen

          python3 main.py -o output.csv -p yes -i data.csv
		This will read from file, print to file, and print to screen

	  python3 Main.py -o output.csv -r 164 +r 165 -d 7 +d 8
		This will display all observations of the location entered  
