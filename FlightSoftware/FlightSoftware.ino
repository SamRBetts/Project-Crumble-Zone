//basic led blinker for teensy 4.0

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

