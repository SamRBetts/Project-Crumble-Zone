//Flight software code for Crumple Zone Cansat Team
//by Tyler Kessis


#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP3XX.h>
#include <Adafruit_LSM6DSOX.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
#include <TimeLib.h>
#include <SD.h>

//state variables

bool isBeforeLaunch = true;
bool isAscent = false;
bool isFastDescent = false;
bool isSlowDescent = false;
bool isOnGround = false;

bool isSimEnabled = false;
bool isSimActivated = false;

bool isBeaconActivated = false;

//timer variable
IntervalTimer timer;

//packet variables

// constant team id
uint16_t const TEAM_ID = 2033; 
// utc time
String MISSION_TIME = String("00:00:00"); 
/*increment everytime packet is transmitted since turned on
  reset to 0 when installed on launch pad
  maintain count during processor reset*/
uint16_t PACKET_COUNT = 0;
// 'F' for flight mode and 'S' for simulation mode 
char MODE = 'F';
//operating state of the software
String STATE = String("HI I LIKE THIS STATE!");
//altitude meters relative to ground level with resolution of 0.1m
float ALTITUDE = 0.0;
//ground altitude for altitude calibration (not in packet)
float groundAltitude = 0.0;
//air speed in meters per second with the pitot tube during ascent and descent
float AIR_SPEED = 0.0;
//'P' inicates the heat shield deployed, 'N' otherwise
char HS_DEPLOYED = 'N';
//'C' indicates the parachute deployed (at 100 m), ‘N’ otherwise.
char PC_DEPLOYED = 'N'; 
//temperature in degrees celcius with resolution of 0.1 degrees
float TEMPERATURE = 0.0;
//voltage from voltage regulator resolution of 0.1 V
float VOLTAGE = 0.0;
//air pressure from the bmp sensor in kPa, 0.1 resolution
float PRESSURE = 0.0; 
//time from gps receiver in UTC with resolution of seconds
String GPS_TIME = String("00:00:00"); 
//altitude from gps with resolution of 0.1 meters
double GPS_ALTITUDE = 0.0;
//latitude of GPS receiver in degrees with resolution of 0.0001 degree North
double GPS_LATITUDE = 0.0000;
//latitude of GPS receiver in degrees with resolution of 0.0001 degree West
double GPS_LONGITUDE = 0.0000; 
//number of satellites tracked by GPS reciever
uint32_t GPS_SATS = 0;
//X tilt angle of cansat in degrees with 0.01 resolution
float TILT_X = 0.00;
//Y tilt angle of cansat in degrees with 0.01 resolution
float TILT_Y = 0.00;
//rotation rate of cansat in degrees per second with 0.1 resolution
float ROT_Z = 0.0;
//text of last command received and processed by CanSat.
String CMD_ECHO = String("ITSCOMMANDINTIME");

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

    const uint16_t SEALEVELPRESSURE_HPA = 1013.25;

    Adafruit_BMP3XX bmp;

    PressureSensor() {

    }

    void begin() {
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
      
    }

    void begin() {
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
      
    }

    void begin() {
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
    
    //get pressure and temperature for density calculation
    Adafruit_BMP3XX bmp;

    PitotTube(Adafruit_BMP3XX bmp3) {
      bmp = bmp3;
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
      Serial.println(_status);

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

      

      deltaP = (float) (P_dat - MS4525ZeroCounts)/MS4525Span*MS4525FullScaleRange; //kPa

      //287.05 = air gas constant (J/kg), 273.15 = convert to Kelvin
      float rho = bmp.pressure/(287.05*(bmp.temperature + 273.15));

      float airspeed = sqrt(2*deltaP/rho);

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
      
    }

    void begin() {
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
      
    }

    void begin() {
      if (!SD.begin(chipSelect)) {
        Serial.println("no SD card!");
        return;
      }
      
      if(SD.exists("packet_data.csv")) {
        SD.remove("packet_data.csv");
      }
    }

    void write(String data) {
      // open the file.
      myFile = SD.open("packet_data.csv", FILE_WRITE);

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

class Clock {

  public:
    Clock() {

    }
    
    void begin() {
      Serial.begin(9600);

      setSyncProvider(Teensy3Clock.get());   // the function to get the time from the RTC
      if(timeStatus()!= timeSet) {
        Serial.println("Unable to sync with the RTC");
      }
      else {
        Serial.println("RTC has set the system time");  
      }
    }

    String getUTCtime() {
      // digital clock display of the time

      if (timeStatus() == timeSet) {
        return printDigitsHour(hour()) + printDigits(minute()) + printDigits(second());
      }

      return "XX:XX:XX";
    }

    String printDigitsHour(int digits){
      // utility function for digital clock display: prints leading 0
      String s;
      if(digits < 10) {
        s = "0";
      }
      return s + String(digits);
    }

    String printDigits(int digits){
      // utility function for digital clock display: prints preceding colon and leading 0
      String s;
      s = ":";
      if(digits < 10) {
        s += "0";
      }
      return s + String(digits);
    }

    void clockSetTime(unsigned long t) {
      Teensy3Clock.set(t); // set the RTC
      setTime(t);
    }

};

//class instance variables
//compiler doesn't like these variables above the classes
PressureSensor pres;
GPSSensor gps;
AccelerometerGyroscopeSensor accelGy;
PitotTube pito(pres.bmp);
XBeeCommunication xbee;
SDCard sd;
Clock cl;


void collectData() {
  //tp.MISSION_TIME = "00:00:00" //get rtc working!
  //tp.PACKET_COUNT++;
  
  if(! isSimActivated) {
    ALTITUDE = pres.bmp.readAltitude(pres.SEALEVELPRESSURE_HPA) - groundAltitude;
    PRESSURE = pres.bmp.readPressure() / 1000; // kPa
  }
  AIR_SPEED = pito.getAirspeed();
  TEMPERATURE = pres.bmp.readTemperature();
  //VOLTAGE = 
  GPS_TIME = String(gps.tgps.time.hour()) + String(":") + String(gps.tgps.time.minute()) + String(":") + String(gps.tgps.time.second());
  GPS_ALTITUDE = gps.tgps.altitude.meters();
  GPS_LATITUDE = gps.tgps.location.lat();
  GPS_LONGITUDE = gps.tgps.location.lng();
  GPS_SATS = gps.tgps.satellites.value();
  TILT_X = accelGy.sox.gyroX;
  TILT_Y = accelGy.sox.gyroY;
  ROT_Z = accelGy.sox.gyroZ;
  
  //tp.CMD_ECHO; 
}

String buildStateString() {
  if(isBeforeLaunch) {
    return String("BEFORE_LAUNCH");
  }
  if(isAscent) {
    return String("ASCENT");
  }
  if(isFastDescent) {
    return String("FAST_DESCENT");
  }
  if(isSlowDescent) {
    return String("SLOW_DESCENT");
  }
  return String("ON_GROUND");
}

String buildPacket() {
  String packet = String("<");
  packet = packet + String(TEAM_ID) + String(", ");
  packet = packet + MISSION_TIME + String(", ");
  packet = packet + String(PACKET_COUNT) + String(", ");
  packet = packet + String(MODE) + String(", ");
  packet = packet + buildStateString() + String(", ");
  packet = packet + String(ALTITUDE) + String(", ");
  packet = packet + String(AIR_SPEED) + String(", ");
  packet = packet + String(HS_DEPLOYED) + String(", ");
  packet = packet + String(PC_DEPLOYED) + String(", ");
  packet = packet + String(TEMPERATURE) + String(", ");
  packet = packet + String(VOLTAGE) + String(", ");
  packet = packet + String(PRESSURE) + String(", ");
  packet = packet + GPS_TIME + String(", ");
  packet = packet + String(GPS_ALTITUDE) + String(", ");
  packet = packet + String(GPS_LATITUDE) + String(", ");
  packet = packet + String(GPS_LONGITUDE) + String(", ");
  packet = packet + String(GPS_SATS) + String(", ");
  packet = packet + String(TILT_X) + String(", ");
  packet = packet + String(TILT_Y) + String(", ");
  packet = packet + String(ROT_Z) + String(", ");
  packet = packet + CMD_ECHO;
  packet = packet + String(">");

  return packet;
}

void collectSendStore() {
  collectData();
  MISSION_TIME = cl.getUTCtime();
  String packet = buildPacket();

  //print for testing!
  //Serial.println(packet);

  //xbee.sendPacket(packet);
  sd.write(packet);
}

void executeCommand(String cmd) {
  //toggle telemetry transmission
  if(cmd.endsWith("CX,ON")) {
    //activate payload telemtry transmission
  }
  if(cmd.endsWith("CX,OFF")) {
    //turn off transmissions
  }

  //set clock
  if(cmd.startsWith("CMD,2033,ST,") && cmd.length() == 20) {
    int h = cmd.substring(12,14).toInt();
    int m = cmd.substring(15,17).toInt();
    int s = cmd.substring(18,20).toInt();
    unsigned long t = h*3600 + m*60 + s;
    cl.clockSetTime(t);
  }
  if(cmd.endsWith("|GPS")) {
    cl.clockSetTime(gps.tgps.time.value());
  }


  //enable, activate, disable simulation mode
  if(cmd.endsWith("SIM,ENABLE")) {
    isSimEnabled = true;
  }
  if(cmd.endsWith("SIM,ACTIVATE") && isSimEnabled) {
    isSimActivated = true;
  }
  if(cmd.endsWith("SIM,DISABLE")) {
    isSimEnabled = false;
    isSimActivated = false;
  }

  if(cmd.startsWith("CMD,2033,SIMP,") && isSimActivated) {
    //need to calculate altitude somhow from this
    PRESSURE = (float) cmd.substring(14).toInt() / 1000.0;
    ALTITUDE = 44330*(1 - pow(10*PRESSURE/1013.25, 1/5.255)) - groundAltitude;
  }

  if(cmd.endsWith("CAL")) {
    groundAltitude = pres.bmp.readAltitude(pres.SEALEVELPRESSURE_HPA);
  }

  if(cmd.endsWith("BCN,ON")) {
    //maybe just activate beacon directly with no boolean.
    //i need beacon code first to do this
    isBeaconActivated = true;
  }
  if(cmd.endsWith("BCN,OFF")) {
    isBeaconActivated = false;
  }
}

void setup() {

  Serial.begin(9600);
  Wire.begin();
  pres.begin();
  groundAltitude = pres.bmp.readAltitude(pres.SEALEVELPRESSURE_HPA);
  gps.begin();
  accelGy.begin();
  sd.begin();
  cl.begin();
  //set up servos and other small stuff here


  timer.begin(collectSendStore,1000000); // 1 Hz interval
  

}


void loop() {

  //state machine

  if(isBeforeLaunch) {

    /*check xbee's recieve instrucions to 
      calibrate altitude for real flight or do simulation mode */
      //toggle next state

  }else if(isAscent) {

    //check if max altitude is reached ~ 700m
      //deploy skirt mechanism and seperate nose cone from CanSat
      //toggle next state

  }else if(isFastDescent) {

    //check if altitude is less than 100m
      //actuate solenoid to release parachute from its container
      //toggle next state

  }else if(isSlowDescent) {

    //check if velocity is near zero or if cansat is near starting altitude
      //toggle to next state

  }else if(isOnGround) {

    //recieve audio beacon command from ground station to retrieve cansat

  }

}