//Flight software code for Crumple Zone Cansat Team
//by Tyler Kessis


#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP3XX.h>
#include <Adafruit_LSM6DSOX.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
#include <SD.h>


//state variables

bool isBeforeLaunch = true;
bool isAscent = false;
bool isFastDescent = false;
bool isSlowDescent = false;
bool isOnGround = false;


//packet variables

uint16_t TEAM_ID = 2033;
String MISSION_TIME;
uint16_t PACKET_COUNT;
char MODE;
String STATE;
float ALTITUDE;
float AIR_SPEED;
char HS_DEPLOYED;
char PC_DEPLOYED; 
float TEMPERATURE;
float VOLTAGE;
float PRESSURE; 
String GPS_TIME; 
float GPS_ALTITUDE;
float GPS_LATITUDE;
float GPS_LONGITUDE; 
uint32_t GPS_SATS;
float TILT_X;
float TILT_Y;
float ROT_Z;
String CMD_ECHO;

String telemetryPacket = TEAM_ID + ", " + MISSION_TIME + ", " + PACKET_COUNT + ", " + MODE + ", " + STATE + ", " + 
                         ALTITUDE + ", " + AIR_SPEED + ", " + HS_DEPLOYED + ", " + PC_DEPLOYED + ", " + TEMPERATURE + ", " + 
                         VOLTAGE + ", " + PRESSURE + ", " + GPS_TIME + ", " + GPS_ALTITUDE + ", " + GPS_LATITUDE + ", " + 
                         GPS_LONGITUDE + ", " + GPS_SATS + ", " + TILT_X + ", " + TILT_Y + ", " + ROT_Z + ", " + CMD_ECHO;


//timer variables

bool isDataCollected = false;
bool isPacketTransfered = false;

const uint32_t startTime = millis();

//SoftWareSerial objects
//put software serials as global variables.
//doesn't work inside classes idk why

SoftwareSerial ssGPS(0, 1); // rx and tx pins respectivley
SoftwareSerial ssXBee(7, 8);

//classes for each device improves code organization for large projects like this

class PressureSensor {

  public:
    #define BMP_SCK 13
    #define BMP_MISO 12
    #define BMP_MOSI 11
    #define BMP_CS 10

    uint16_t SEALEVELPRESSURE_HPA = 1013.25;

    Adafruit_BMP3XX bmp;

    PressureSensor() {

      if (!bmp.begin_I2C()) {  // hardware I2C mode, can pass in address & alt Wire
        //if (! bmp.begin_SPI(BMP_CS)) {  // hardware SPI mode
        //if (! bmp.begin_SPI(BMP_CS, BMP_SCK, BMP_MISO, BMP_MOSI)) {  // software SPI mode
        Serial.println("Could not find a valid BMP3 sensor, check wiring!");
        while (1);
      }

      bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
      bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
      bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
      bmp.setOutputDataRate(BMP3_ODR_50_HZ);
    }
};

class GPSSensor {

  #define GPSBaud 9600

  public:

    TinyGPSPlus tgps;


    GPSSensor() {
      ssGPS.begin(GPSBaud);
    }
};

class AccelerometerGyroscopeSensor {


  public:

    // For SPI mode, we need a CS pin
    #define LSM_CS 10
    // For software-SPI mode we need SCK/MOSI/MISO pins
    #define LSM_SCK 13
    #define LSM_MISO 12
    #define LSM_MOSI 11
    Adafruit_LSM6DSOX sox;

    AccelerometerGyroscopeSensor() {
      if (!sox.begin_I2C()) {
        // if (!sox.begin_SPI(LSM_CS)) {
        // if (!sox.begin_SPI(LSM_CS, LSM_SCK, LSM_MISO, LSM_MOSI)) {
        // Serial.println("Failed to find LSM6DSOX chip");
        while (1) {
          delay(10);
        }
      }

      sox.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
      sox.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
      sox.setAccelDataRate(LSM6DS_RATE_12_5_HZ);
      sox.setGyroDataRate(LSM6DS_RATE_12_5_HZ);
      }
};

class PitotTube {


  public:

    // MS4525D sensor I2C address (uncomment the Interface Type of the device you are using)
    // Interface Type I
    const uint8_t MS4525DAddress = 0x28;
    // Interface Type J
    //const uint8_t MS4525DAddress = 0x36;
    // Interface Type K
    //const uint8_t MS4525DAddress = 0x46;
    // Interface Type 0
    //const uint8_t MS4525DAddress = 0x48;

    // MS4525D sensor full scale range and units
    //const int16_t MS4525FullScaleRange = 1;  // 1 psi
    //const int16_t MS4525FullScaleRange = 0.0689476; // 1 psi in Bar
    const int16_t MS4525FullScaleRange = 6895;  // 1 psi in Pascal
    //const int16_t MS4525FullScaleRange = 2; // 2 psi
    //const int16_t MS4525FullScaleRange = 5; // 5 psi

    // MS4525D Sensor type (A or B) comment out the wrong type assignments
    // Type A (10% to 90%)
    const int16_t MS4525MinScaleCounts = 1638;
    const int16_t MS4525FullScaleCounts = 14746;
    // Type B (5% to 95%)
    //const int16_t MS4525MinScaleCounts = 819;
    //const int16_t MS4525FullScaleCounts = 15563;
    const int16_t MS4525Span = MS4525FullScaleCounts - MS4525MinScaleCounts;

    //MS4525D sensor pressure style, differential or otherwise. Comment out the wrong one.
    //Differential
    const int16_t MS4525ZeroCounts = (MS4525MinScaleCounts + MS4525FullScaleCounts) / 2;
    // Absolute, Gauge
    //const int16_t MS4525ZeroCounts=MS4525MinScaleCounts;

    PitotTube() {
    }
    
    byte fetch_pressure(uint16_t &P_dat, uint16_t &T_dat) {
      byte _status;
      byte Press_H;
      byte Press_L;
      byte Temp_H;
      byte Temp_L;

      Wire.requestFrom(MS4525DAddress, static_cast<uint8_t>(4), static_cast<uint8_t>(true));  //Request 4 bytes, 2 pressure/status and 2 temperature
      Press_H = Wire.read();
      Press_L = Wire.read();
      Temp_H = Wire.read();
      Temp_L = Wire.read();

      _status = (Press_H >> 6) & 0x03;
      Press_H = Press_H & 0x3f;
      P_dat = (((uint16_t)Press_H) << 8) | Press_L;

      Temp_L = (Temp_L >> 5);
      T_dat = (((uint16_t)Temp_H) << 3) | Temp_L;

      return _status;
    }

    float getAirspeed() {
      byte _status;    // A two bit field indicating the status of the I2C read
      uint16_t P_dat;  // 14 bit pressure data
      uint16_t T_dat;  // 11 bit temperature data
      float deltaP;

      _status = fetch_pressure(P_dat, T_dat);

      switch (_status) {
        case 0:
          //Serial.println("Ok ");
          break;
        case 1:
          Serial.println("Busy");
          break;
        case 2:
          Serial.println("Slate");
          break;
        default:
          Serial.println("Error");
          break;
      }

      deltaP = (float) (P_dat - MS4525ZeroCounts)/MS4525Span*MS4525FullScaleRange * 6894.7573; //kPa
      float airspeed = sqrt(2*deltaP/1.2041); //1.2041 = air density

      return airspeed;
    }
};

class XBeeCommunication {
  #define XBeeBaud 9600

  public:
    //Constants:
    //serial pind for xbee

    //Variables:
    bool started = false;  //True: Message is strated
    bool ended = false;    //True: Message is finished
    char incomingByte;     //Variable to store the incoming byte
    String msg;            //recieved message

    XBeeCommunication() {
      ssXBee.begin(XBeeBaud);
    }

    void sendPacket(String s) {
      ssXBee.print(s);
    }

    void recieveInstructions() {
      msg = "";
      //read message from other xbee
      while (ssXBee.available() > 0) {
        //Serial.println("a");
        //Read the incoming byte
        incomingByte = ssXBee.read();
        //Serial.print(incomingByte);
        //Start the message when the '<' symbol is received
        if (incomingByte == '<') {
          //Serial.println("b");
          started = true;
          msg = "";  // Throw away any incomplete packet
        }
        //End the message when the '>' symbol is received
        else if (incomingByte == '>') {
          //Serial.println("c");
          ended = true;
          break;  // Done reading - exit from while loop!
        }
        //Read the message!
        else if (msg.length() < 100) {
          //Serial.println("d");
          msg += incomingByte;  // Add char to array
                                //Serial.println(msg);
        }
      }

      //Serial.println(started);
      //Serial.println(ended);

      if (started && ended) {
        //Serial.println("e");
        //store / return message
        Serial.println(msg);
        msg = "";
        started = false;
        ended = false;
      }
    }
};

class SDCard {

  public:
    File myFile;
    const int chipSelect = BUILTIN_SDCARD;

    SDCard() {
      if (!SD.begin(chipSelect)) {
        Serial.println("initialization failed!");
        return;
      }
      Serial.println("initialization done.");
    }

    void write(String data) {
      // open the file.
      myFile = SD.open("packet_data.txt", FILE_WRITE);

      // if the file opened okay, write to it:
      if (myFile) {
        myFile.println(data);
        // close the file:
        myFile.close();
      } else {
        // if the file didn't open, print an error:
        Serial.println("error opening test.txt");
      }
    }
};


//class instance variables
//compiler doesn't like these variables above the classes
//PressureSensor pres;
//GPSSensor gps;
//AccelerometerGyroscopeSensor accelGy;
PitotTube pito;
//XBeeCommunication xbee;
SDCard sd;

/*
void collectData() {
  ALTITUDE = pres.bmp.readAltitude(pres.SEALEVELPRESSURE_HPA);
  AIR_SPEED = pito.getAirspeed();
  TEMPERATURE = pres.bmp.readTemperature();
  //VOLTAGE = 
  PRESSURE = pres.bmp.readPressure() / 1000; // kPa
  GPS_TIME = gps.tgps.time.value();
  GPS_ALTITUDE = gps.tgps.altitude.meters();
  GPS_LATITUDE = gps.tgps.location.lat();
  GPS_LONGITUDE = gps.tgps.location.lng();
  GPS_SATS = gps.tgps.satellites.value();
  TILT_X = accelGy.sox.gyroX;
  TILT_Y = accelGy.sox.gyroY;
  ROT_Z = accelGy.sox.gyroZ;
  //CMD_ECHO;
  
}
*/

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Serial.println("HI");
  //set up servos and other small stuff here

}


void loop() {

  //Serial.println("How are u");
  delay(200);

  /*
  //data collection and transmission

  uint32_t currentTime = millis();

  //collect data at 1 Hz
  if((currentTime - startTime) % 1000 == 0 && !isDataCollected) {
    collectData();

    Serial.println("data collected maybe");

    //fix to make it run once and not multiple times during the one ms duration
    isDataCollected = true;
  }else if((currentTime - startTime) % 1000 != 0 && isDataCollected) {
    isDataCollected = false;
  }
  
  //send data to ground station at 1 Hz
  //store data to SD card
  if((currentTime - startTime) % 1000 == 0 && !isPacketTransfered) {
    xbee.sendPacket(telemetryPacket);
    sd.write(telemetryPacket);

    Serial.println(telemetryPacket);

    isPacketTransfered = true;
  }else if((currentTime - startTime) % 1000 != 0 && isPacketTransfered) {
    isPacketTransfered = false;
  }


  //state machine

  if(isBeforeLaunch) {

    // check xbee's recieve instructions method to do real flight launch or simulation through sent packet data.
      //toggle next state

  }else if(isAscent) {

    //check if max altitude is reached
      //then do stuff i forget the exact details, deploy skirt, remove nosecone?
      //toggle next state

  }else if(isFastDescent) {

    //check if specific altitude is reached (100 meters i think)
      //deploy parachute with solenoid, idk how that code would work ask eric!

  }else if(isSlowDescent) {

    //check if velocity is near zero or if cansat is near starting altitude
      //toggle to next state

  }else if(isOnGround) {

    //mission is done send happy signals to ground station

  }

  */
}