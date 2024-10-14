#include <Arduino.h>

// These are inputs fro the BMP388 (Environment sensor) and BNO (orientation/IMU)
//https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
//https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx?view=all#spi-logic-pins-3022081
//It is necessary to add the libraries to Platform IO in order to be able to build correctly
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h> 
#include "Adafruit_BMP3XX.h"
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define BMP_SCK 13
#define BMP_MISO 12
#define BMP_MOSI 11
#define BMP_CS 10

Adafruit_BNO055 bno = Adafruit_BNO055(55);
#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BMP3XX bmp;
// put function declarations here:


void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600); //Begin broadcasting over serial on a baud rate of 9600
  // Set up pins for digital input and output- for help refer to the "Resources" folder for the schematic
  // Using pins 1-6 for servo output. Pin 3 is GROUND- Do not assign something to this

  pinMode(1, OUTPUT); //High Torque Servo Miuzei
  pinMode(2, OUTPUT); //Grab — MGT Servo
  pinMode(4,OUTPUT); // Rotation MGT-Servo
  pinMode(5,OUTPUT); //PWMA Driver - Is this an input?
  pinMode(6,OUTPUT); //PWMB Driver- Are these actually inputs- difficult to tell from the diagram

  pinMode(21, INPUT); //SDA-BMP388- SDA = serial input to processor- confirm
  pinMode(22, OUTPUT); //SCL-BMP388

  pinMode(25, OUTPUT); //SCL-BNO055
  pinMode(26, INPUT); //SDA-BNO055- SDA = serial input to processor- confirm

  pinMode(40, OUTPUT); //Output to Libre


}

void loop() {
  // put your main code here, to run repeatedly:
}

// put function definitions here: