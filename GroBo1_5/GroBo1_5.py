#Author: Francis Gillet
#Date: October 9th 2020
# Description: This code will receive serial input from the Arduino.
# the code will also plot the data received from the Arduino so that a graph of the data can be visualized.
# Hopefully the code will be stored into a database so that the entire history of the data can be read.
import csv
import serial #import the serial library
import numpy as np # this is for doing array math
import time
import matplotlib.pyplot as plt # this is for plotting the data
from drawnow import *
 # this is for saving the data into SQL database
# empty data arrays to put the sensor data into
tempF = []
humidity = []
# For counting light cycles
count = 0;
# Code for connecting the arduino serial to python
arduinoData = serial.Serial('COM3', 115200)
plt.ion() # Tell matplotlib that you want to plot live data.
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
    #serial.read().decode()
    arduinoString = arduinoData.readline().decode(); # Reads the data from the arduino serial.. as a string
    dataArray = arduinoString.split(','); # Stores the data string as an array using a comma delimiter
    print(arduinoString)
    try:
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
    except: 
        print("Exception occured")
        pass;
        


