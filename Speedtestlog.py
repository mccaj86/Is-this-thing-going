#!/usr/bin/env python

'''
Speedtestlog.py: A program to run speed tests and save the data
A. J. McCulloch, March 2019
'''

####################################################################################################
# Import modules
####################################################################################################

import speedtest # Module to interface with speedtest.net
import os.path # Module for file verification
import schedule # Module to handle scheduling
import time # Module to retrieve system time
import datetime # Module to handle timestamp manipulation
import csv # Module to handle CSV files

####################################################################################################
# Define functions
####################################################################################################

# Function to run the speedtest and return a dictionary with the results
def dotest():
    try:
        # Generate test object
        s = speedtest.Speedtest()
        # Retrieve servers for speedtest
        s.get_servers()
        # Select the best server
        s.get_best_server()
        # Run download speed test
        s.download()
        # Run upload speed test
        s.upload()
        # Return
        return s.results.dict()
    except:
        fields = ['download', 'upload', 'ping', 'server', 'bytes_sent', 'bytes_received', 'share', 'client']
        nullreturn = dict([(i,None) for i in fields])
        nullreturn['timestamp'] = datetime.datetime.utcnow().isoformat()
        return nullreturn

# Function to write the speed test results (a dictionary) to a .csv file
def writeresults(dictionary, file = 'speedtestresults.csv'):
    # Check if the file exists
    file_exists = os.path.isfile(file)
    # Open the file in append mode
    with open(file, 'a') as f:
        # Create DictWrite object
        w = csv.DictWriter(f, dictionary.keys())
        # If creating the file, write headers
        if not file_exists:
            # Make a header for the csv
            w.writeheader()
        # Write data
        w.writerow(dictionary)

# Function to collect and write the speedtest data
def runner():
    # Run the speed test
    results = dotest()
    # Write the data
    writeresults(results)

####################################################################################################
####################################################################################################
# Code starts here
####################################################################################################
####################################################################################################

# Set the schedule for performing a speed test
schedule.every(10).minutes.do(runner)

'''
Note scheduler does not account for the time it takes to run the script!
By it nature, this is a non-negligible amount of time for this script.
'''

# Execute the program
while True:
    # Verify if a task is pending (it should be!)
    schedule.run_pending()
    # Don't do anything for a second
    time.sleep(1)
