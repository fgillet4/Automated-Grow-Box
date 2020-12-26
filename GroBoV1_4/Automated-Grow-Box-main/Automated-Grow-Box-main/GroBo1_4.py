#Author: Francis Gillet
#Date: October 9th 2020
# Description: This code will receive serial input from the Arduino.
# the code will also plot the data received from the Arduino so that a graph of the data can be visualized.
# Hopefully the code will be stored into a database so that the entire history of the data can be read.
import gspread #API for google sheets
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import serial #import the serial library
import numpy as np # this is for doing array math
import matplotlib.pyplot as plt # this is for plotting the data
from drawnow import *
import time
import datetime
import sqlite3 # this is for saving the data into SQL database
# empty data arrays to put the sensor data into
tempF = []
humidity = []
# For counting light cycles
count = 0;
# Code for connecting the arduino serial to python
arduinoData = serial.Serial('COM3', 115200)
plt.ion() # Tell matplotlib that you want to plot live data.
#conn = sqlite3.connect('Data.db')# Connects to the SQL database
#Defining the Scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#Add Credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('GroBoV4-87b2ea556386.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('SensorData')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# add a sheet with 20 rows and 2 columns
sheet.add_worksheet(rows=20,cols=2,title='runs')

# get the instance of the second sheet
sheet_runs = sheet.get_worksheet(1)

sheet_runs.insert_rows(runs.values.tolist())

def make_figure(): #Create a function that makes the desired plot
    plt.ylim(32,90);
    plt.title('Live Sensor Data')
    plt.grid(True);
    plt.ylabel('Temperature [F]')
    plt.xlabel('Time')
    plt.plot(tempF, 'ro-', label='Degrees F');
    plt.legend(loc = 'upper right')
    plt2 = plt.twinx()
    plt2.plot(humidity, 'b^-', label = 'Humidity %')
    plt.ylim(0,100)
    plt2.ticklabel_format(useOffset = False) #Force matplotlib not to autoscale the y axis
    plt2.legend(loc = 'upper left')
    return
while True: #While loop that loops forever
    while (arduinoData.inWaiting() == 0): #Wait here for data.
        pass #do nothing
    #serial.read().decode()
    arduinoString = arduinoData.readline().decode(); # Reads the data from the arduino serial.. as a string
    dataArray = arduinoString.split(','); # Stores the data string as an array using a comma delimiter
    print(arduinoString)
    temp = float(dataArray[0]) #Converts the temp string into a float so we can do math and plots.
    humid = float(dataArray[1]) # Converts the humidity string into a float so we can do math and plots
    tempF.append(temp) #Add the data into the data array declared at the top
    humidity.append(humid) # adds the data into the data array at the top.
    drawnow(make_figure); # Call drawnow to update the live graph
    plt.pause(0.000001);
    count = count +1;
    if(count > 50): # here is to plot the most recent data, removing old data to make the graph cooler.
        tempF.pop(0); # This removes the 0th element of the array
        humidity.pop(0); #this pops the first element


