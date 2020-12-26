//Author: Francis Gillet and Jay Miller
// Date: October 9th 2020
// Description: This code will take sensor data from the arduino and send it into python.
// When significant error is measured against the setpoints, the corresponding actuator action will takeplace
//Make sure to install the DHT-11 temp/RH sensor library and Sketch->Import Library
#include <DHT.h>
#include "Wire.h"
#define DHTPIN 2

#define DHTTYPE DHT11
//Creating the object.
DHT dht(2,11);

float tempC; // Variable to hold the temp reading in C
float tempF; // Variable to hold the temp in F
float humidity; // Varible to hold the relative humidity.
//Labling the digital pins used for the project
int fanPIN = 1; //Controlling the fan relay with digi pin 1
int heaterPIN = 3; // Controlling the heater realy with digi pin 3
int valvePIN = 4; // Controlling the water valve realy with digi pin 4
int moistureSensorPIN = 5;// Gathering analog data about the light value pin 5
int lightsPIN = 6; // Potentially controlling lights on pin 6...
//For changing the reccomended room temp
float roomTempThreshold = 70.0; // This number sets the room homeostasis
int lightReading = 0; //Initial value to prevent mem leaks, the blinking light will change this
unsigned long myTime; // Used to keep track of lighting cycles
void setup() {
  // Turn the serial monitor on, the stepping up the BAUD rate to get faster data for python
  Serial.begin(115200); // Start the serial monitor
  dht.begin(); // initialize the DHT sensor
  pinMode(fanPIN, output); //The relay requires the 5V logic signal from the arduino
  pinMode(heaterPIN, output); //The relay requires the 5V logic signal from the arduino
  pinMode(valvePIN, output); //The relay requires the 5V logic signal from the arduino
  pinMode(moistureSensorPIN, input); //This analog pin will measure the light signal from the moisture sensor
}

void loop() {

  tempC = dht.readTemperature(); //Reads the temperature in degrees C
  tempF = tempC*1.8+32.;// Converting temp to F
  humidity = dht.readHumidity(); // Reads the humidity
  lightReading = analogRead(moistureSensorPIN); // This is the phototransistor measuring blinking light 
  Serial.print(tempF);//Printing degrees in farenheight on serial
  Serial.print(",");// separates the farenheight data and the moisture data by a comma
  Serial.println(humidity);//Ln makes a new line for the print statement
  
  //Thermostat Code
  // This next part of the code is the heating logic, when room is above 70 degress = fans
  // when room is below 70 degrees = heater.
  if(tempF < roomTempThreshold)
  { digitalWrite(heaterPIN,HIGH); //HIGH send 5v voltage to the relay, turning on the heater
  } else {digitalWrite(heaterPIN,LOW);} //Low sends 0v to the relay, keepiong the heater off
  if(tempF > roomTempThreshold)
  { digitalWrite(heaterPIN,LOW); //turns off the heater
    digitalWrite(fanPIN,HIGH); // Turns on the fan
  } else {
    digitalWrite(heaterPIN,HIGH);
    digitalWrite(fanPIN,LOW);
    } //Low sends 0v to the relay, keepiong the heater off
  if(humidity > 60.0)
  { digitalWrite(fanPIN,HIGH); }
  
  //Water Reservoir Flow Valve Code
  if(lightReading > 50)// If phototransistor gets a blinking signal it will likley be greater than 50
  {digitalWrite(valvePIN,HIGH);} // Then the blinking signal tells the valve to turn on
  else {digitalWrite(valvePIN,LOW);} // Resting state of valve is closed

  //Lighting
  myTime = millis();//Counting the time in milliseconds, note 50 days max
  if(myTime % 8*pow(10,7)< 8*pow(10,7)/2  )//The modulo is used to start a 12 hour cycle
  {
    digitalWrite(lightsPIN,HIGH); //Turns on the lights
  }
  else
  {
    digitalWrite(lightsPIN,LOW); // Turns off the lights
  }
  delay(1000);
}
