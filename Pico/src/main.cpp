#include <Arduino.h>

/**These are inputs fro the BMP388 (Environment sensor) and BNO (orientation/IMU)
 *  https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
 * https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx?view=all#spi-logic-pins-3022081
 * It is necessary to add the libraries to Platform IO in order to be able to build correctly
 *
 *
 *
 * */

#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"
#include <Adafruit_BNO055.h>
#include "SparkFun_TB6612.h"
#include <utility/imumaths.h>
#include <Servo.h>
// #include <SparkFun_TB6612.h>

// TODO: Double check these
// #define BMP_SCK 13
// #define BMP_MISO 12
// #define BMP_MOSI 11
// #define BMP_CS 10
#define PWMB 11
#define BIN1 9
#define BIN2 10
#define STBY 41
/**Notes for tb6612 driver
 * https://electropeak.com/learn/interfacing-tb6612fng-dual-motor-driver-module-with-arduino/#google_vignette
 */

// ! This is really hard to visualize without looking at real HW

Adafruit_BNO055 bno = Adafruit_BNO055(55);
#define SEALEVELPRESSURE_HPA (1013.25) // TODO: Does this value need to be tuned

Adafruit_BMP3XX bmp;

unsigned long IMUCheckTimeElapsed = 0UL;
unsigned long IMUUpdateInterval = 100UL;

unsigned long EnvCheckTimeElapsed = 0UL;
unsigned long EnvUpdateInterval = 100UL;

// Declare vars for environmental sensor in preparation of writing to file
double envTemp = 0.0;
double envPressure = 0.0;
double envAltitude = 0.0;

// Declare vars for IMU sensor in preperation for writing values to a file
double posX = 0.0;
double posY = 0.0;
double posZ = 0.0;

double accelX = 0.0;
double accelY = 0.0;
double accelZ = 0.0;

const int basePitchOffset = 1;
const int baseRotateOffset = 1;

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

void setup()
{
  // put your setup code here, to run once:

  Serial.begin(9600); // Begin broadcasting/receiving over serial on a baud rate of 9600
  while (!Serial)
    ; // Execute while not running in serial mode

  // Set up pins for digital input and output- for help refer to the "Resources" folder for the schematic
  // Using pins 1-6 for servo output.
  //! Pin 3 is GROUND- Do not assign something to this

  pinMode(0, OUTPUT); // High Torque Servo Miuzei
  pinMode(1, OUTPUT); // Grab — MGT Servo
  pinMode(2, OUTPUT); // Rotation MGT-Servo
  // pinMode(3, OUTPUT); // PWMA Driver - Is this an input?
  pinMode(8, OUTPUT); // PWMB Driver- Are these actually inputs- difficult to tell from the diagram

  pinMode(11, INPUT); // These are the GPIO pins - 11 and 12
  pinMode(12, OUTPUT);

  // TODO: Double check the pin assignment on this
  pinMode(4, INPUT);  // SDA-BMP388- SDA = serial input to processor- confirm
  pinMode(5, OUTPUT); // SCL-BMP388

  pinMode(4, OUTPUT); // SCL-BNO055
  pinMode(5, INPUT);  // SDA-BNO055- SDA = serial input to processor- confirm

  pinMode(40, OUTPUT); // Output to Libre

  pinMode(PWMA, OUTPUT);
  pinMode(bin1, OUTPUT);
  pinMode(bin2, OUTPUT);

  // Set pin on the pico which the SD card is on, so we can save a file
  const int sdOutputPin = 17; // Actual pin on the pico is 22

  /**Servo initialization
   * https://docs.arduino.cc/libraries/servo/
   * baseRotationServo - 1st servo, controls rotation of the arm base
   * basePitchServo - 2nd servo from the bottom, used to control pitch of the arm
   * midPitchServo - 3rd servo from the bottom, controls the pitch of the portion of the arm with the end effector
   * wristPitchServo - 4th servo from the bottom, controls the pitch of the wrist
   * clawServo - 5th servo from the bottom, controls the closing and opening action of the claw
   * base is GM3 motor/ servo
   * axis 1 is 25 kg
   * all other axis are basic servos
   */

  Servo midPitchServo;
  Servo wristPitchServo;
  Servo clawServo;

  // This should create a file if it does not exist

  if (!SD.begin(17))
  {
    Serial.println("initialization failed!");
    while (1);
  }
  Serial.println("initialization done.");

  // Check that we are receiving input from the BMP 388, print error message if not
  if (!bmp.begin_I2C())
  {
    Serial.println("No BMP388 sensor is detected. Please check wiring, pin assignment in both hardware and software,etc. ");
    while (1); // Throw
  }
  if (!bno.begin())
  {
    Serial.print("No BNO055 sensor is detected. Please check wiring, pin assignment in both hardware and software,etc.");
    while (1);
  }
  // Throw if the SD card cant be written to
  if (!SD.begin(sdOutputPin))
  {
    Serial.println("SD card initialization failed. Please check the wiring and ensure that pins are initialized correctly in software.");
    return;
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
  // Set up SD card for writing
  sensorDataFile = SD.open("sensorData.txt", FILE_WRITE);

  // ! Temporary IMU Output for testing purposes
  // TODO: This is just temporary for testing- able to display values from the IMU, but are not truly readable and able to be interpreted.
  // TODO: Going with 2 decimal places at this time. Determine if we need to change this

  unsigned long currentIMUTime = millis(); // Get the current time in milliseconds

  /**Serial communication
   * TODO: Ensure that the received values are the same as the transmitted values in base station
   * https://www.elithecomputerguy.com/2020/12/arduino-send-commands-with-serial-communication/
   * https://www.arduino.cc/reference/tr/language/functions/communication/serial/read/
   * Check if serial active, then look for commands
   * Read the string until there is a new line - trim after a new line
   */
  char receivedTempChar;
  static byte ndx = 0;
  if (Serial.available() > 0)
  {
    receivedTempChar = Serial.read();
    if (receivedTempChar != endMarker)
    {
      receivedValues[ndx] = receivedTempChar;
      ndx++;
      if (ndx >= numberOfChars)
      {
        ndx = numberOfChars - 1;
      }
      else
      {
        // TODO: Confirm this works 
        receivedValues[ndx] = '\0';
        ndx = 0;
        char receivedValues = 'value';
        int motorPosition = receivedValues;
        Serial.print(motorPosition);
        driveMotorA(motorPosition, false);
      }
    }
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
  if (currentIMUTime - IMUCheckTimeElapsed >= IMUUpdateInterval)
  {
    imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
    sensors_event_t getIMUEvent;
    bno.getEvent(&getIMUEvent);

    posX = (getIMUEvent.orientation.x);
    posY = (getIMUEvent.orientation.y);
    posZ = (getIMUEvent.orientation.z);
    uint8_t system, gyro, accel, mag = 0;
    bno.getCalibration(&system, &gyro, &accel, &mag);
    Serial.print("Calibration values:");
    Serial.print(system, DEC);
    // Serial.print("Gyro=");
    // Serial.print(gyro, DEC);
    Serial.print("Acceleration");
    Serial.print(accel, DEC);
    accelX =(getIMUEvent.acceleration.x);
    accelY = (getIMUEvent.acceleration.y);
    accelZ = (getIMUEvent.acceleration.z);
    // Serial.print("Magnetometer");
    // Serial.print(mag, DEC);

    // TODO: There is a better way to do this with headers, but this will work for now
    // TODO: Do this with new string methods
    sensorDataFile = SD.open("sensorData.csv");
    if (sensorDataFile)
    {
      sensorDataFile.print(", currentIMUTime ,");
      sensorDataFile.print(currentIMUTime);
      sensorDataFile.print("  posX ,");
      sensorDataFile.print(posX);
      sensorDataFile.print("  posY ,");
      sensorDataFile.print(posY);
      sensorDataFile.print("  posZ ,");
      sensorDataFile.print(posZ);
      sensorDataFile.print(" acceleration X,");
      sensorDataFile.print(accelX);
      sensorDataFile.print(" acceleration Y,");
      sensorDataFile.print(accelY);
      sensorDataFile.print(" acceleration Z,");
      sensorDataFile.print(accelZ);
      sensorDataFile.print("\n");

      sensorDataFile.close();
    }
    else
    {
      Serial.println("Unable to write to the sensor data file. Check wiring and pin assignments");
    }

    Serial.print("Current time between IMU Update:");
    Serial.print(IMUUpdateInterval);
    Serial.print("X axis: ");
    Serial.print(posX);
    Serial.print("Y axis: ");
    Serial.print(posY);
    Serial.print("Z Axis: ");
    Serial.print(posZ);
    Serial.print("Accel X");
    Serial.print(accelX);
    Serial.print("Accel Y");
    Serial.print(accelY);
    Serial.print("Accel Z");
    Serial.print(accelZ);
    

    

    IMUCheckTimeElapsed = currentIMUTime; // Update the previous IMU value with the current value of the time elapsed so it can trigger the conditional
  }

  /** This takes data from the enviromental sensor and writes it to a file as well as printing it to the terminal
   * Data collected includes:
   * current time in milliseconds
   * current temperature
   * current pressure
   * current altitude ( a derivative of pressure)
   */

  if (!bmp.performReading())
  {
    Serial.println("Sensor is not able to perform the reading. Please check that the sensor is connected correctly (wiring and software)");
    return;
  }

  unsigned long currentEnvTime = millis(); // Get the current time in milliseconds- could this possibly be merged into the main function

  if (currentEnvTime - EnvCheckTimeElapsed >= EnvUpdateInterval)
  {
    envTemp = bmp.temperature;
    envPressure = bmp.pressure / 100;
    envAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);

    /**Writes the following to the SD card
     * The Current Environment sensor time (timestamp)
     * Temperature sensor reading/data
     * Pressure sensor reading/data
     * Altitude sensor reading/data
     */
    sensorDataFile = SD.open("sensorData.csv");
    if (sensorDataFile)
    {

      // TODO: There is a better way to do this with headers, but this will work for now
      sensorDataFile.print(", currentEnvTime ,");
      sensorDataFile.print(currentEnvTime);
      sensorDataFile.print(", envTemp ,");
      sensorDataFile.print(envTemp);
      sensorDataFile.print(", envPressure ,");
      sensorDataFile.print(envPressure);
      sensorDataFile.print(", envAltitude ,");
      sensorDataFile.print(envAltitude);
      sensorDataFile.print("\n");
      sensorDataFile.close();
      
    }
    // else{
    //   Serial.print("Sensor data is unable to be written to a file. Please check wiring and pin assignments");

    // }

    Serial.print("Current time between Environmental sensor update");
    Serial.print(currentEnvTime);
    Serial.print(" Celsius");
    Serial.print(envTemp); // TODO: This is in celsius! Do we want to have this in Fahrenheit?
    Serial.print("Pressure");
    Serial.print(envPressure); // TODO: This is in HPA. Do we want that?
    Serial.print("Altitude:");
    Serial.print(envAltitude); // TODO: This is in meters. Determine if we want to use this for units, or change to something else
    Serial.print(" meters");
  }
}
void driveMotorA(int speed, bool direction){
  if (direction){
    digitalWrite(bin1, HIGH);
    digitalWrite(bin2, HIGH);
  }
}
void stopMotor(){
  analogWrite(PWMA, 0);
}