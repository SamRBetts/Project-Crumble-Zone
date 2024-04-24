//Flight software code for Crumple Zone Cansat Team
//by Tyler Kessis

//include dependent libraries
  #include <Adafruit_LSM6DSOX.h>
  #include <Adafruit_LIS3MDL.h>
  #include <Adafruit_Sensor.h>
  #include <Adafruit_BMP3XX.h>
  #include <SoftwareSerial.h>
  #include <DFRobot_INA219.h>
  #include <NMEAGPS.h>
  #include <TimeLib.h>
  #include <Servo.h>
  #include <Wire.h>
  #include <SPI.h>
  #include <SD.h>
  #include <Streamers.h>
  #include <GPSport.h>

//sea level pressure
  //use this website to get sea level pressure 1 mbar = 1 hpa
  // https://weather.us/observations
  #define SEALEVELPRESSURE_HPA 1013.25

//state variables

  bool isBeforeLaunch = true;
  bool isAscent;
  bool isFastDescent;
  bool isSlowDescent;
  bool isOnGround;

//payload telemetry transmission state
bool isTelemetryTransmissionOn;

//simulation states
bool isSimEnabled;
bool isSimActivated;

//audio beacon state
bool isBeaconActivated;

//solenoid pin
#define solPin 2

//audio beacon pin
#define buzPin 3

//servo
#define servoPin 6
#define detatchDuration 4320 //in milliseconds. change if needed
uint32_t servoStartTime;
bool isServoMovingForwards;
bool isServoMovingBackwards;
Servo servo;

//wattmeter
  DFRobot_INA219_IIC ina219(&Wire, INA219_I2C_ADDRESS4);
  // Revise the following two paramters according to actula reading of the INA219 and the multimeter
  // for linearly calibration
  float ina219Reading_mA = 15;
  float extMeterReading_mA = 15;

//timer variable
IntervalTimer timer1;
IntervalTimer timer2;

//gps
  NMEAGPS  gps; // This parses the GPS characters
  gps_fix  gfix; // This holds on to the latest values

//gps / xbee hardware serial
  #define gpsPort Serial1
  #define xbeePort Serial2

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
  float GPS_ALTITUDE = 0.0;
  //latitude of GPS receiver in degrees with resolution of 0.0001 degree North
  float GPS_LATITUDE = 0.0000;
  //latitude of GPS receiver in degrees with resolution of 0.0001 degree West
  float GPS_LONGITUDE = 0.0000; 
  //number of satellites tracked by GPS reciever
  uint8_t GPS_SATS = 0;
  //X tilt angle of cansat in degrees with 0.01 resolution
  float TILT_X = 0.00;
  //Y tilt angle of cansat in degrees with 0.01 resolution
  float TILT_Y = 0.00;
  //rotation rate of cansat in degrees per second with 0.1 resolution
  float ROT_Z = 0.0;
  //text of last command received and processed by CanSat.
  String CMD_ECHO = String("NULL");

//packet string
String packet;

//other variables for state machine
  float accelZ;
  float maxAltitude;
  float rotX;
  float rotY;
  //ground altitude for altitude calibration (not in packet)
  float groundAltitude = 0.0;
  float simGroundAltitude = 44330.0*(1.0 - pow(939.48/SEALEVELPRESSURE_HPA, 1.0/5.255));


//classes for each device improves code organization for large projects like this

class PressureSensor {

  public:
    #define BMP_SCK 13
    #define BMP_MISO 12
    #define BMP_MOSI 11
    #define BMP_CS 10

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

class AccelGyroMag {


  public:

    // For SPI mode, we need a CS pin
    #define LSM_CS 10
    // For software-SPI mode we need SCK/MOSI/MISO pins
    #define LSM_SCK 13
    #define LSM_MISO 12
    #define LSM_MOSI 11
    
    #define LIS3MDL_CLK 13
    #define LIS3MDL_MISO 12
    #define LIS3MDL_MOSI 11
    #define LIS3MDL_CS 10
    Adafruit_LSM6DSOX sox;
    Adafruit_LIS3MDL lis3mdl;

    AccelGyroMag() {
      
    }

    void begin() {
      if (!sox.begin_I2C()) {
        Serial.println("Failed to find LSM6DSOX chip");
        while (1) { delay(10); }
      }

      if (! lis3mdl.begin_I2C()) {          // hardware I2C mode, can pass in address & alt Wire
        Serial.println("Failed to find LIS3MDL chip");
        while (1) { delay(10); }
      }

      sox.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
      sox.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
      sox.setAccelDataRate(LSM6DS_RATE_12_5_HZ);
      sox.setGyroDataRate(LSM6DS_RATE_12_5_HZ);

      lis3mdl.setPerformanceMode(LIS3MDL_MEDIUMMODE);
      lis3mdl.setOperationMode(LIS3MDL_CONTINUOUSMODE);
      lis3mdl.setDataRate(LIS3MDL_DATARATE_155_HZ);
      lis3mdl.setRange(LIS3MDL_RANGE_4_GAUSS);
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

      deltaP = (float) (P_dat - MS4525ZeroCounts)/MS4525Span*MS4525FullScaleRange; //kPa
      if(deltaP < 0.0) {
        deltaP = 0.0;
      }

      //0.28705 = air gas constant (kJ/kg), 273.15 = convert to Kelvin
      float rho = PRESSURE/(0.28705*(TEMPERATURE + 273.15));

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
      xbeePort.begin(XBeeBaud);
    }

    void transmitPacket(String s) {
      xbeePort.print(s);
    }

    String recieveInstructions() {
      msg = "";
      //read message from other xbee
      while (xbeePort.available() > 0) {
        //Serial.println("a");
        //Read the incoming byte
        incomingByte = xbeePort.read();
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
        //Serial.println(msg);
        started = false;
        ended = false;
        return msg;
      }

      return "N";
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
        myFile = SD.open("packet_data.csv", FILE_WRITE);
        if(myFile) {
          myFile.println("TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE, AIR_SPEED, HS_DEPLOYED, PC_DEPLOYED, TEMPERATURE, VOLTAGE, PRESSURE, GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS, TILT_X, TILT_Y, ROT_Z, CMD_ECHO");
          myFile.close();
        } else {
        // if the file didn't open, print an error:
        Serial.println("error opening test.txt");
        }

      }
    }

    void cacheCurrentPacket(String data) {
      
      //new file every time function is called
      if(SD.exists("current_packet.txt")) {
        SD.remove("current_packet.txt");
      } else {
        Serial.println("file does not exist, creating new file");
      }
      
      // open the file.
      myFile = SD.open("current_packet.txt", FILE_WRITE);

      // if the file opened okay, write to it:
      if (myFile) {
        myFile.print(data);
        // close the file:
        myFile.close();
      } else {
        // if the file didn't open, print an error:
        Serial.println("error opening test.txt");
      }
    }

    void storePacket(String data) {
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

    void restoreVariables() {
      // open the file.
      myFile = SD.open("current_packet.txt");

      if (myFile) {
        uint8_t columnNum = 0;
        String packetVar = "";

        while (myFile.available()) {
          char c = myFile.read();
          //Serial.println("HI");
          if(c != ',') {
            packetVar += String(c);
          } else {
            myFile.read(); //removes space after each comma
            switch(columnNum) {
              //skip TEAM_ID since it's constant
              case 1:
                MISSION_TIME = packetVar;
                break;
              case 2:
                PACKET_COUNT = packetVar.toInt();
                break;
              case 3:
                MODE = packetVar.charAt(0);
                break;
              case 4:
                STATE = packetVar;
                break;
              case 5:
                ALTITUDE = packetVar.toFloat();
                break;
              case 6:
                AIR_SPEED = packetVar.toFloat();
                break;
              case 7:
                HS_DEPLOYED = packetVar.charAt(0);
                break;
              case 8:
                PC_DEPLOYED = packetVar.charAt(0);
                break;
              case 9:
                TEMPERATURE = packetVar.toFloat();
                break;
              case 10:
                VOLTAGE = packetVar.toFloat();
                break;
              case 11:
                PRESSURE = packetVar.toFloat();
                break;
              case 12:
                GPS_TIME = packetVar;
                break;
              case 13:
                GPS_ALTITUDE = packetVar.toFloat();
                break;
              case 14:
                GPS_LATITUDE = packetVar.toFloat();
                break;
              case 15:
                GPS_LONGITUDE = packetVar.toFloat();
                break;
              case 16:
                GPS_SATS = packetVar.toInt();
                break;
              case 17:
                TILT_X = packetVar.toFloat();
                break;
              case 18:
                TILT_Y = packetVar.toFloat();
                break;
              case 19:
                ROT_Z = packetVar.toFloat();
                break;
              case 20:
                CMD_ECHO = packetVar;
                break;
           }
            columnNum++;
            packetVar = "";
          }
        }
        myFile.close();
      }  
      // if the file isn't open, pop up an error:
      else {
        Serial.println("error opening datalog.txt");
      }
    }
};

class Clock {

  public:
    Clock() {

    }
    
    void begin() {
      setSyncProvider(Teensy3Clock.get);   // the function to get the time from the RTC
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
      Teensy3Clock.set(t);
      setTime(t);
    }
};

//class instance variables
//compiler doesn't like these variables above the classes
PressureSensor pres;
AccelGyroMag accelGy;
PitotTube pito;
XBeeCommunication xbee;
SDCard sd;
Clock cl;

void collectData() {

  //tp.PACKET_COUNT++;

  
  pres.bmp.performReading();
  if(! isSimActivated) {
    ALTITUDE = pres.bmp.readAltitude(SEALEVELPRESSURE_HPA) - groundAltitude;
    PRESSURE = pres.bmp.readPressure() / 1000.0; // kPa
  }

  accelGy.lis3mdl.read();
  sensors_event_t mag; 
  accelGy.lis3mdl.getEvent(&mag);

  //Serial.println(mag.magnetic.z);
  
  TILT_X = atan2(-(mag.magnetic.z + 18.07),mag.magnetic.x - 18.23) * RAD_TO_DEG;
  TILT_Y = atan2(-(mag.magnetic.z + 18.07),mag.magnetic.y + 20.58) * RAD_TO_DEG;

  //i dont think this works but it was worth a try
  //TILT_X =  mag.magnetic.roll
  //TILT_Y = mag.magnetic.pitch;

  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  accelGy.sox.getEvent(&accel, &gyro, &temp);
  accelZ = accel.acceleration.z;
  rotX = gyro.gyro.x*RAD_TO_DEG;
  rotY = gyro.gyro.y*RAD_TO_DEG;
  ROT_Z = gyro.gyro.z*RAD_TO_DEG;

  TEMPERATURE = (pres.bmp.readTemperature() + temp.temperature) / 2.0;

  AIR_SPEED = pito.getAirspeed();

  VOLTAGE = ina219.getBusVoltage_V();

/*
  while (gps.available( gpsPort )) {
    gfix = gps.read();
    trace_all( DEBUG_PORT, gps, gfix );

    if(gfix.valid.time) {
      uint8_t h = gfix.dateTime.hours;
      uint8_t m = gfix.dateTime.minutes;
      uint8_t s = gfix.dateTime.seconds;
      GPS_TIME = (h < 10 ? "0" : "") + String(h) + ":" + (m < 10 ? "0" : "") + String(m) + ":" + (s < 10 ? "0" : "") + String(s);
    } 

    if(gfix.valid.location) {
      GPS_LATITUDE = gfix.latitude();
      GPS_LONGITUDE = gfix.longitude();
    }

    if(gfix.valid.altitude) {
      Serial.println(gfix.altitude());
      GPS_ALTITUDE = gfix.altitude();
    }
    
    if(gfix.valid.satellites) {
      Serial.println(gfix.satellites);
      GPS_SATS = gfix.satellites;
    }
  }
  */
  
  //trace_all( DEBUG_PORT, gps, gfix );

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
  return  String("<")
        + String(TEAM_ID) + String(", ")
        + MISSION_TIME + String(", ")
        + String(PACKET_COUNT) + String(", ")
        + String(MODE) + String(", ")
        + buildStateString() + String(", ")
        + String(ALTITUDE,1) + String(", ")
        + String(AIR_SPEED,1) + String(", ")
        + String(HS_DEPLOYED) + String(", ")
        + String(PC_DEPLOYED) + String(", ")
        + String(TEMPERATURE,1) + String(", ")
        + String(VOLTAGE,1) + String(", ")
        + String(PRESSURE,1) + String(", ")
        + GPS_TIME + String(", ")
        + String(GPS_ALTITUDE,1) + String(", ")
        + String(GPS_LATITUDE,4) + String(", ")
        + String(GPS_LONGITUDE,4) + String(", ")
        + String(GPS_SATS) + String(", ")
        + String(TILT_X,2) + String(", ")
        + String(TILT_Y,2) + String(", ")
        + String(ROT_Z,1) + String(", ")
        + CMD_ECHO + String(">");
}

void executeCommand(String cmd) {
  
  if(cmd.substring(9).equals("CX,ON")) {
    isTelemetryTransmissionOn = true;
    PACKET_COUNT = 0;
  }
  if(cmd.substring(9).equals("CX,OFF")) {
    isTelemetryTransmissionOn = false;
  }

  //set clock
  if(cmd.substring(0,12).equals("CMD,2033,ST,") && cmd.length() == 20) {
    int h = cmd.substring(12,14).toInt();
    int m = cmd.substring(15,17).toInt();
    int s = cmd.substring(18,20).toInt();
    unsigned long t = h*3600 + m*60 + s;
    cl.clockSetTime(t);
  }
  
  if(cmd.substring(12).equals("GPS")) {
    int h = gfix.dateTime.hours;
    int m = gfix.dateTime.minutes;
    int s = gfix.dateTime.seconds;
    unsigned long t = h*3600 + m*60 + s;
    cl.clockSetTime(t);
  }
  
  //enable, activate, disable simulation mode
  if(cmd.substring(9).equals("SIM,ENABLE")) {
    isSimEnabled = true;
  }
  if(cmd.substring(9).equals("SIM,ACTIVATE") && isSimEnabled) {
    isSimActivated = true;
    MODE = 'S';
    //prevents ascent state from occuring until pressure data is sent
    ALTITUDE = -1.0;
  }
  if(cmd.substring(9).equals("SIM,DISABLE")) {
    isSimEnabled = false;
    isSimActivated = false;
    MODE = 'F';
  }

  //receive simulated pressure data
  if(cmd.substring(0,14).equals("CMD,2033,SIMP,") && isSimActivated) {
    
    PRESSURE = (float) cmd.substring(14).toInt() / 1000.0;
    //maybe this calculation works idk ahahaha
    ALTITUDE = 44330.0*(1.0 - pow(10.0*PRESSURE/SEALEVELPRESSURE_HPA, 1.0/5.255)) - simGroundAltitude;
  }

  //calibrate altitude to ground level
  if(cmd.substring(9).equals("CAL")) {

    groundAltitude = pres.bmp.readAltitude(SEALEVELPRESSURE_HPA);
  }

  //turn on / off audio beacon
  if(cmd.substring(9).equals("BCN,ON")) {

    digitalWrite(buzPin, HIGH);
  }

  if(cmd.substring(9).equals("BCN,OFF")) {

    digitalWrite(buzPin, LOW);
  }
  if(cmd.substring(9).equals("PR,ON")) {

    digitalWrite(solPin, HIGH);
  }

  if(cmd.substring(9).equals("PR,OFF")) {

    digitalWrite(solPin, LOW);
  }

  //reset packet count to zero
  if(cmd.substring(9).equals("RSTPKT")) {  

    PACKET_COUNT = 0;
  }

  //Nose cone detatch test command
  if(cmd.substring(9).equals("DTCH")) {  
    detatchTest();
  }

  String cmdNoComma;
  for(uint8_t i = 9; i < cmd.length(); i++) {
    char c = cmd.charAt(i);
    if(c != ',') {
      cmdNoComma += String(c);
    }
  }
  CMD_ECHO = cmdNoComma;
}

void detatchTest() {
  isServoMovingForwards = true;
  servoStartTime = millis();
  servo.write(180); // rotate forward
}

void collectAndSave() {
  collectData();
  MISSION_TIME = cl.getUTCtime();
  packet = buildPacket();

}

void sendStoreReceive() {
  //packet = buildPacket();
  //print for testing!
  //if(gfix.valid.location) {
  Serial.println(packet);
  //}

  if(isTelemetryTransmissionOn) {
    xbee.transmitPacket(packet);
    PACKET_COUNT++;
  }
  
  String cmd = xbee.recieveInstructions();
  if(! cmd.equals("N")) {
    Serial.println(cmd);
    executeCommand(cmd);
  }
  sd.cacheCurrentPacket(packet.substring(1, packet.length() - 1));
  sd.storePacket(packet.substring(1, packet.length() - 1));
}

void setup() {

  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);

  Serial.begin(9600);
  Wire.begin();

  delay(50);

  cl.begin();

  sd.begin();
  
  Serial.println("Restoring packet variables:");
  sd.restoreVariables();
  //cl.clockSetTime(MISSION_TIME.substring(0,2).toInt() * 3600 + MISSION_TIME.substring(3,5).toInt() * 60 + MISSION_TIME.substring(6).toInt());
  Serial.println(buildPacket());
  
  pres.begin();
  gpsPort.begin(9600); //Serial1
  accelGy.begin();
  xbee.begin();

  pinMode(solPin, OUTPUT);
  pinMode(buzPin, OUTPUT);
  
  if(ina219.begin() != true) {
    Serial.println("INA219 begin failed");
  } else {
    ina219.linearCalibrate(ina219Reading_mA, extMeterReading_mA);
  }
  
  servo.attach(servoPin);
  //isServoMovingForwards = true;
  //servoStartTime = millis();
  //servo.write(180); // rotate forward

  timer1.begin(collectAndSave,  100000); //  10 Hz interval
  timer2.begin(sendStoreReceive,1000000); // 1 Hz interval

  
}

void loop() {

  //state machine
  if(isBeforeLaunch) {

    //check xbee's recieve instructions to 
    //calibrate altitude for real flight or do simulation mode 

    //if accelerating upwards, switch to isAscent state
    
    if(! isSimActivated) { 
      //use rocket acceleration to activate next state
      if(accelZ >  39.2) {
        isBeforeLaunch = false;
        isAscent = true;
      }
    } else {
      //In simulation mode, use precalculated altitude to initiate state
      if(ALTITUDE > 10) {
        isBeforeLaunch = false;
        isAscent = true;
      }
    }
  }else if(isAscent) {
    
    //if max altitude greater than current altitude switch to fastDescent state
    if(maxAltitude <= ALTITUDE) {
      maxAltitude = ALTITUDE;
    } else {
      isAscent = false;
      isFastDescent = true;

      //turn on audio beacon
      if(! isSimActivated) {
        digitalWrite(buzPin, HIGH);
      }
      
      //Skirt (Heatshield) passivley deploys
      HS_DEPLOYED = 'P';
    }
  }else if(isFastDescent) {

    //if altitude at 100m switch to slowDescent state
    if(ALTITUDE <= 100.0) {
      isFastDescent = false;
      isSlowDescent = true;

      //release parachute housing lid to deploy parachute
      digitalWrite(solPin, HIGH);
      PC_DEPLOYED = 'C';

      //release skirt and nosecone
      //servo timer start
      isServoMovingForwards = true;
      servoStartTime = millis();
      servo.write(180); // rotate forward
    }
  }else if(isSlowDescent) {

    if(! isSimActivated) {
      //if vehicle is not moving switch to on ground state
      //i dont like this ill change it later
      if(rotX <= 0.5 && rotX >= -0.5 && rotY <= 0.5 && rotY >= -0.5 && ROT_Z <= 0.5 && ROT_Z >= -0.5) {
        isSlowDescent = false;
        isOnGround = true;
      }
    } else {
      /*
        simulation pressure data goes from 8m (just above ground) to 3m (landing) 
        with standard sea level pressure and ground level calibration from first pressure value
        so check altitude < 5m
        basically hardcoded but o well
      */
      if(ALTITUDE < 5.0) {
        isSlowDescent = false;
        isOnGround = true;
      }
    }
  }else if(isOnGround) {

    //wait for commands from ground station

  }

  if(isServoMovingForwards) {
    if(millis() - servoStartTime > detatchDuration) {
      servoStartTime = millis();
      servo.write(0); //rotate backwards
      isServoMovingForwards = false;
      isServoMovingBackwards = true;
    }
  }

  if(isServoMovingBackwards) {
    if(millis() - servoStartTime > detatchDuration) {
      servoStartTime = millis();
      servo.write(90); //stop
      isServoMovingBackwards = false;
    }
  }

  //gps loop

  while (gps.available( gpsPort )) {
    gfix = gps.read();
    //trace_all( DEBUG_PORT, gps, gfix );

    if(gfix.valid.time) {
      uint8_t h = gfix.dateTime.hours;
      uint8_t m = gfix.dateTime.minutes;
      uint8_t s = gfix.dateTime.seconds;
      GPS_TIME = (h < 10 ? "0" : "") + String(h) + ":" + (m < 10 ? "0" : "") + String(m) + ":" + (s < 10 ? "0" : "") + String(s);
    } 

    if(gfix.valid.location) {
      GPS_LATITUDE = gfix.latitude();
      GPS_LONGITUDE = gfix.longitude();
    }

    if(gfix.valid.altitude) {
      //Serial.println(gfix.altitude());
      GPS_ALTITUDE = gfix.altitude();
    }
    
    if(gfix.valid.satellites) {
      //Serial.println(gfix.satellites);
      GPS_SATS = gfix.satellites;
    }
  }
}