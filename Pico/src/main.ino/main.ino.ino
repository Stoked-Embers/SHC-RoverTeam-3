#include <Arduino.h>

#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"
#include <Adafruit_BNO055.h>
#include "SparkFun_TB6612.h"
#include <utility/imumaths.h>
#include "PWMDcMotor.hpp"
#include "RobotCarPinDefinitionsAndMore.h"
#include <Servo.h>


// TODO: Double check these
// #define BMP_SCK 13
// #define BMP_MISO 12
// #define BMP_MOSI 11
// #define BMP_CS 10
#define PWMB 11
#define BIN1 9
#define BIN2 10
#define STBY 41

// SPI.setSCK(18);
// SPI.setRX(16);
// SPI.setTX(19);


Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
#define SEALEVELPRESSURE_HPA (1013.25) // TODO: Does this value need to be tuned

Adafruit_BMP3XX bmp;

// Records the time since the last sensor update and recording to the SD card
unsigned long previousSensorUpdate = 0;
unsigned long lastSensorUpdate = 0;
// Update the sensor values and write to the SD card every 3 seconds
long sensorUpdateInterval = 3000;

// Declare vars for environmental sensor in preparation of writing to file
double envTemp = 0.0;
double envPressure = 0.0;
double envAltitude = 0.0;

// Declare vars for IMU sensor in preparation for writing values to a file
double posX = 0.0;
double posY = 0.0;
double posZ = 0.0;

const int basePitchOffset = 1;
const int baseRotateOffset = 1;

PWMDcMotor basePitchMotor;

// Motor baseRotateMotor = Motor(BIN1, BIN2, PWMB, baseRotateOffset, STBY);
// Motor basePitchMotor = Motor(BIN1, BIN2, PWMB, basePitchOffset, STBY);

const byte numberOfChars = 32;
char receivedValues[numberOfChars];

File sensorDataFile;
char endMarker = '\n';

const int PWMA = 8;
const int bin1 = 6;
const int bin2 = 7;
const int speed = 5;

void driveMotorA(int speed, bool direction);

int motorSpeed = 0;

Servo basePitchServo;
Servo midPitchServo;
Servo endPitchServo;
Servo endEffectorGrabServo;

String motorAssignment;
String motorSpeedAssignmentUnfiltered;
int motorSpeedAssignment;

void setup()
{
  // put your setup code here, to run once:

  Serial.begin(9600); // Begin broadcasting/receiving over serial on a baud rate of 9600
  basePitchMotor.init(6, 7, 8);

  // Set up pins for digital input and output- for help refer to the "Resources" folder for the schematic
  // Using pins 1-6 for servo output.
  //! Pin 3 is GROUND- Do not assign something to this
  pinMode(LED_BUILTIN, OUTPUT);
  // pinMode(0, OUTPUT); // High Torque Servo Miuzei - Commented this out because we are attaching a servo. 
  
  
  // Attach the base servo (value between slightly above 0- probably about 10, and slightly below 180 to prevent conflict)
  basePitchServo.attach(0,700, 2000); 
  // Attach the middle servo (value between slightly above 0- probably about 10, and slightly below 180 to prevent conflict)
  midPitchServo.attach(1,700, 2000);
  // Attach the end effector pitch servo to pin 2 (value between slightly above 0- probably about 10, and slightly below 180 to prevent conflict)
  endPitchServo.attach(2,700, 2000);
  // Attach the claw servo to pin 3 (Going to a pretty narrow band to begin with)
  endEffectorGrabServo.attach(3,1200,2000);
  // pinMode(1, OUTPUT); // Grab — MGT Servo
  // pinMode(2, OUTPUT); // Rotation MGT-Servo
  // pinMode(3, OUTPUT); // PWMA Driver - Is this an input?
  
  
  pinMode(8, OUTPUT); // PWMB Driver- Are these actually inputs- difficult to tell from the diagram

  pinMode(11, INPUT); // These are the GPIO pins - 11 and 12
  pinMode(12, OUTPUT);

  // TODO: Double check the pin assignment on this
  //pinMode(4, INPUT);  // SDA-BMP388- SDA = serial input to processor- confirm
  //pinMode(5, OUTPUT); // SCL-BMP388

  //pinMode(4, OUTPUT); // SCL-BNO055
  //pinMode(5, INPUT);  // SDA-BNO055- SDA = serial input to processor- confirm

  pinMode(40, OUTPUT); // Output to Libre

  pinMode(PWMA, OUTPUT);
  pinMode(bin1, OUTPUT);
  pinMode(bin2, OUTPUT);

  // Set pin on the pico which the SD card is on, so we can save a file
  const int sdOutputPin = 17; // Actual pin on the pico is 24

  



  

  if (!SD.begin(17))
  {
    Serial.println("initialization failed!");
  
  }
  // This should create a file if it does not exist. NOTE: Keep the file write command in the loop. It does not overwrite the file, but opens it and write data to it.
  // sensorDataFile = SD.open("sensorData.csv", FILE_WRITE);


  Serial.println("initialization done.");

  // Check that we are receiving input from the BMP 388, print error message if not
  // if (!bmp.begin_I2C())
  // {
  //   Serial.println("No BMP388 sensor is detected. Please check wiring, pin assignment in both hardware and software,etc. ");
   
  // }
  if (!bno.begin())
  {
    Serial.print("No BNO055 sensor is detected. Please check wiring, pin assignment in both hardware and software,etc.");
    
  }
  // Throw if the SD card cant be written to
  // if (!SD.begin(sdOutputPin))
  // {
  //   Serial.println("SD card initialization failed. Please check the wiring and ensure that pins are initialized correctly in software.");
  //   return;
  // }

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
  // Set up SD card for writing

  // ! Temporary IMU Output for testing purposes
  // TODO: This is just temporary for testing- able to display values from the IMU, but are not truly readable and able to be interpreted.
  // TODO: Going with 2 decimal places at this time. Determine if we need to change this
  // digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  // delay(1000);                      // wait for a second
  // digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  // delay(1000);     
  unsigned long currentIMUTime = millis(); // Get the current time in milliseconds

  /**Serial communication
   * TODO: Ensure that the received values are the same as the transmitted values in base station
   * https://www.elithecomputerguy.com/2020/12/arduino-send-commands-with-serial-communication/
   * https://www.arduino.cc/reference/tr/language/functions/communication/serial/read/
   * Check if serial active, then look for commands
   * Read the string until there is a new line - trim after a new line
   */
 

if(Serial.available() > 0){
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    char buf[command.length() + 1];
    command.toCharArray(buf, command.length() + 1);

    char *token = strtok(buf, ",");
    int mor0 = atoi(token);

    token = strtok(NULL, ",");
    int ser0 = atoi(token);

    token = strtok(NULL, ",");
    int ser1 = atoi(token);

    token = strtok(NULL, ",");
    int ser2 = atoi(token);

    token = strtok(NULL, ",");
    int ser3 = atoi(token);
    
    basePitchMotor.setSpeedPWMAndDirection(mor0);
    basePitchServo.write(ser0);
    midPitchServo.write(ser1);
    endPitchServo.write(ser2);
    endEffectorGrabServo.write(ser3);
    
  }

  /** This section collects IMU data and writes it to a file. Data collected includes:
   * X axis orientation
   * Y axis orientation
   * Z axis orientation
   * Acceleration
   * currentIMU time - in milliseconds
   * Also prints to serial for debugging purposes- can comment out if needed
   */

  // TODO: Need to add acceleration to the file writing and to the serial output as well
  
  if(millis() - previousSensorUpdate >= sensorUpdateInterval){
    previousSensorUpdate = millis();
	  Serial.println("Current time:");
	  Serial.println(previousSensorUpdate /1000);
	
		digitalWrite(LED_BUILTIN, HIGH);
		imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
		sensors_event_t getIMUEvent;
		bno.getEvent(&getIMUEvent);

		posX = euler.x();
		posY = euler.y();
		posZ = euler.z();
		uint8_t system, gyro, accel, mag = 0;
		bno.getCalibration(&system, &gyro, &accel, &mag);

		// Serial.print("Calibration values:");
		// Serial.print(system, DEC);
		// Serial.print("Gyro=");
		// Serial.print(gyro, DEC);
		// Serial.print("Acceleration");
		// Serial.print(accel, DEC);
		// Serial.print("Magnetometer");
		// Serial.print(mag, DEC);

		// TODO: There is a better way to do this with headers, but this will work for now
		// TODO: Do this with new string methods
  
		
		sensorDataFile = SD.open("sensorData.csv", FILE_WRITE);
		if (sensorDataFile){
		  sensorDataFile.print("posX ,");
		  sensorDataFile.print(posX);
		  sensorDataFile.print("posY ,");
		  sensorDataFile.print(posY);
		  sensorDataFile.print("posZ ,");
		  sensorDataFile.print(posZ);
		  sensorDataFile.print("acceleration ,");
      sensors_event_t accelerometerData;
      bno.getEvent(&accelerometerData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
     // sensorDataFile.print(printEvent(&accelerometerData));
		  sensorDataFile.println(accel, DEC);
    


		  sensorDataFile.close();
		}
		else
		{
		  Serial.println("Unable to write to the sensor data file. Check wiring and pin assignments");
		}

		// Serial.print("Current time between IMU Update:");
		// Serial.print(IMUUpdateInterval);
		// Serial.println("X axis: ");
		// Serial.println(posX);
		// Serial.println("Y axis: ");
		// Serial.println(posY);
		// Serial.println("Z Axis: ");
		// Serial.println(posZ);
		// Serial.println("Acceleration");
		
		//Serial.println(printEvent(&accelerometerData));
		
		Serial.print("$");
		Serial.print(posX + "," + posY + "," + posZ + "$");
		sensors_event_t accelerometerData;
		bno.getEvent(&accelerometerData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
		Serial.print(printEvent(&accelerometerData));
		Serial.print("$");
	  // Serial.println(accel, DEC); 
	  

	  /** This takes data from the enviromental sensor and writes it to a file as well as printing it to the terminal
	   * Data collected includes:
	   * current time in milliseconds
	   * current temperature
	   * current pressure
	   * current altitude ( a derivative of pressure)
	   */

	  if (!bmp.begin_I2C())
	  {
		Serial.println("Sensor is not able to perform the reading. Please check that the sensor is connected correctly (wiring and software)");
		return;
	  }

	  unsigned long currentEnvTime = millis(); // Get the current time in milliseconds- could this possibly be merged into the main function


		envTemp = bmp.temperature;
		envPressure = bmp.pressure / 100;
		envAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);

		/**Writes the following to the SD card
		 * The Current Environment sensor time (timestamp)
		 * Temperature sensor reading/data
		 * Pressure sensor reading/data
		 * Altitude sensor reading/data
		 */
    sensorDataFile = SD.open("sensorData.csv", FILE_WRITE);
		if (sensorDataFile)
		{

		  // TODO: There is a better way to do this with headers, but this will work for now
		  // sensorDataFile.print("currentEnvTime ,");
		  // sensorDataFile.print(currentEnvTime);
		  sensorDataFile.print("envTemp ,");
		  sensorDataFile.print(envTemp);
		  sensorDataFile.print("envPressure ,");
		  sensorDataFile.print(envPressure);
		  sensorDataFile.print("envAltitude ,");
		  sensorDataFile.print(envAltitude);
		  sensorDataFile.close();
		}
		// else{
		//   Serial.print("Sensor data is unable to be written to a file. Please check wiring and pin assignments");

		// }

		// Serial.println("Current time between Environmental sensor update");
		// Serial.println(currentEnvTime);
		// Serial.println(" Celsius");
		// Serial.println(envTemp); // TODO: This is in celsius! Do we want to have this in Fahrenheit?
		// Serial.println("Pressure");
		// Serial.println(envPressure); // TODO: This is in HPA. Do we want that?
		// Serial.println("Altitude:");
		// Serial.println(envAltitude); // TODO: This is in meters. Determine if we want to use this for units, or change to something else
		// Serial.println(" meters");
		
		Serial.print(envTemp + "," + envPressure + "," + envAltitude);
		
		digitalWrite(LED_BUILTIN, LOW);	
  }
}
// void driveMotorA(int speed, bool direction)
// {
//   if (direction)
//   {
//     digitalWrite(bin1, HIGH);
//     digitalWrite(bin2, HIGH);
//   }
// }
// void stopMotor()
// {
//   analogWrite(PWMA, 0);
// }

String printEvent(sensors_event_t* event) {
  double x = -1000000, y = -1000000 , z = -1000000; //dumb values, easy to spot problem
  if (event->type == SENSOR_TYPE_ACCELEROMETER) {
    Serial.print("Accl:");
    x = event->acceleration.x;
    y = event->acceleration.y;
    z = event->acceleration.z;
  }
  return String(x)+String(y)+String(z);  
}
