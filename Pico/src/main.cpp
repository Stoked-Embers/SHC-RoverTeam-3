#include <Arduino.h>

// These are inputs fro the BMP388 (Environment sensor) and BNO (orientation/IMU)
// https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
// https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx?view=all#spi-logic-pins-3022081
// It is necessary to add the libraries to Platform IO in order to be able to build correctly
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
#define SEALEVELPRESSURE_HPA (1013.25) // TODO: Does this value need to be tuned

Adafruit_BMP3XX bmp;

unsigned long IMUCheckTimeElapsed = 0UL;
unsigned long IMUUpdateInterval = 100UL;

unsigned long EnvCheckTimeElapsed = 0UL;
unsigned long EnvUpdateInterval = 100UL;

void setup()
{
  // put your setup code here, to run once:

  Serial.begin(9600); // Begin broadcasting over serial on a baud rate of 9600
  while (!Serial)
    ; // Execute while not running in serial mode

  // Set up pins for digital input and output- for help refer to the "Resources" folder for the schematic
  // Using pins 1-6 for servo output.
  //! Pin 3 is GROUND- Do not assign something to this

  pinMode(1, OUTPUT); // High Torque Servo Miuzei
  pinMode(2, OUTPUT); // Grab — MGT Servo
  pinMode(4, OUTPUT); // Rotation MGT-Servo
  pinMode(5, OUTPUT); // PWMA Driver - Is this an input?
  pinMode(6, OUTPUT); // PWMB Driver- Are these actually inputs- difficult to tell from the diagram

  pinMode(21, INPUT);  // SDA-BMP388- SDA = serial input to processor- confirm
  pinMode(22, OUTPUT); // SCL-BMP388

  pinMode(25, OUTPUT); // SCL-BNO055
  pinMode(26, INPUT);  // SDA-BNO055- SDA = serial input to processor- confirm

  pinMode(40, OUTPUT); // Output to Libre

  // Check that we are receiving input from the BMP 388, print error message if not

  if (!bmp.begin_SPI(BMP_CS, BMP_SCK, BMP_MISO, BMP_MOSI))
  {
    Serial.println("No BMP388 sensor is detected. Please check wiring, pin assignment in both hardware and software,etc. ");
    while (1)
      ; // Throw
  }
  if (!bno.begin())
  {
    Serial.print("No BNO055 sensor is detected. Please check wiring, pin assignment in both hardware and software,etc.");
    while (1)
      ;
  }

  // TODO: Tune this - currently based off of the example code: https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx?view=all#spi-logic-pins-3022081
  // TODO: Figure out what different sampling configs do
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);

  bno.setExtCrystalUse(true); //? What is this? Something to do with accuracy of measurements?
  // TODO: Take a look at the crystal
}

void loop()
{
  // put your main code here, to run repeatedly:

  // ! Temporary IMU Output for testing purposes
  // TODO: This is just temporary for testing- able to display values from the IMU, but are not truly readable and able to be interpreted.
  // TODO: Going with 2 decimal places at this time. Determine if we need to change this

  unsigned long currentIMUTime = millis(); // Get the current time in milliseconds

  if (currentIMUTime - IMUCheckTimeElapsed >= IMUUpdateInterval)
  {
    sensors_event_t getIMUEvent;
    bno.getEvent(&getIMUEvent);
    double updateIMUDelay = 200.00; // TODO: Tune this or convert to a int if needed- don't think that we will truly need a double for this, but might
    Serial.print("Current time between IMU Update:");
    Serial.print(IMUUpdateInterval);
    Serial.print("X axis: ");
    Serial.print(getIMUEvent.orientation.x, 2);
    Serial.print("\tY axis: ");
    Serial.print(getIMUEvent.orientation.y, 2);
    Serial.print("\tZ Axis: ");
    Serial.print(getIMUEvent.orientation.x, 2);
    Serial.print("=============================");

    IMUCheckTimeElapsed = currentIMUTime; // Update the previous IMU value with the current value of the time elapsed so it can trigger the conditional
  }

  // ! Test Environmental Sensor code for testing purposes
  // TODO: This is just going to output the value of the sensors to the terminal, or throw an error when the sensor is not detected

  if (!bmp.performReading())
  {
    Serial.println("Sensor is not able to perform the reading. Please check that the sensor is connected correctly (wiring and software)");
    return;
  }

  unsigned long currentEnvTime = millis(); // Get the current time in milliseconds- could this possibly be merged into the main function
  if (currentEnvTime - EnvCheckTimeElapsed >= EnvUpdateInterval)
  {
    Serial.print("Current time between Environmental sensor update");
    Serial.print(bmp.temperature); // TODO: This is in celsius! Do we want to have this in Fahrenheit?
    Serial.print(" Celsius");
    Serial.print("Pressure");
    Serial.print(bmp.pressure / 100); // TODO: This is in HPA. Do we want that?
    Serial.print("Altitude:");
    Serial.print(bmp.readAltitude(SEALEVELPRESSURE_HPA)); // TODO: This is in meters. Determine if we want to use this for units, or change to something else
    Serial.print(" meters");
  }
}

// put function definitions here:
