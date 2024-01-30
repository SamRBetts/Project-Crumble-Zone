int solPin = 9;
int solPB = 3;
int buzPin = 8;
int buzPB = 2;

void setup(){
  pinMode(solPin, OUTPUT);
  pinMode(solPB, INPUT_PULLUP);
  pinMode(buzPin, OUTPUT);
  pinMode(buzPB, INPUT_PULLUP);
}

void loop(){
  if(digitalRead(solPB)==LOW){
    digitalWrite(solPin, HIGH);
    //delay(1000);
    //digitalWrite(solPin, LOW);
  }
  if(digitalRead(buzPB)==LOW){
    digitalWrite(buzPin, HIGH);
    delay(1000);
    digitalWrite(buzPin, LOW);
    
  }
}