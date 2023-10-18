//basic led blinker for teensy 4.0
//sensors and devices to control:
//teensy, bmp390, matek aspd-4525
//3202-ADA miny camera
//Adafruit LSM6DSOX
//NEO-6M
//xbee
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

