//basic led blinker for teensy 4.0
//sensors and devices to control:
//teensy, bmp390, matek aspd-4525
//3202-ADA miny camera
//Adafruit LSM6DSOX
//NEO-6M
//xbee
//servos
/*
3202-ADA miny camera - pulse white wire for over 100ms to trigger video
                        pulse white wire again to stop video

matek airspeed sensor uses i2c protocol
https://www.pjrc.com/teensy/td_libs_Wire.html
use wire examples

neo 6m use tiny gps examples

xbee examples
*/



const int ledPin = 13;


void setup() {
  // initialize the digital pin as an output.
  pinMode(ledPin, OUTPUT);
}


void loop() {
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(1000);  
}

void bmp390setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Adafruit BMP388 / BMP390 test");

  if (!bmp.begin_I2C()) {   // hardware I2C mode, can pass in address & alt Wire
  //if (! bmp.begin_SPI(BMP_CS)) {  // hardware SPI mode  
  //if (! bmp.begin_SPI(BMP_CS, BMP_SCK, BMP_MISO, BMP_MOSI)) {  // software SPI mode
    Serial.println("Could not find a valid BMP3 sensor, check wiring!");
    while (1);
  }

  // Set up oversampling and filter initialization
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
}