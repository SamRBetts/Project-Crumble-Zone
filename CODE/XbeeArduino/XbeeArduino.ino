/* 	~ 
  read and transmit data from xbee for cansat project
  
  tyler kessis                 
*/

//Constants:
//serial pind for xbee
static const int RXPin = 7, TXPin = 8;
#define xbeePort Serial2

//Variables:
//SoftwareSerial ss(RXPin, TXPin);
bool started= false;//True: Message is strated
bool ended 	= false;//True: Message is finished 
char incomingByte; //Variable to store the incoming byte
String msg;		//recieved message

void setup() {

	//Start the serial communication
	Serial.begin(9600);
  xbeePort.begin(9600); //make sure this matches xbee baud
}

void loop() {

  //put these commands into their own functions later

  //send message to other xbee
  //String message = "hi\n";

  //xbeePortprint(message);
  //Serial.println(message);

  msg = "";  
  //read message from other xbee
  while (xbeePort.available()>0){
    //Serial.println("a");
  	//Read the incoming byte
    incomingByte = xbeePort.read();
    Serial.println(incomingByte);
    //Start the message when the '<' symbol is received
    if(incomingByte == '<')
    {
      //Serial.println("b");
     started = true;
     msg = ""; // Throw away any incomplete packet
   }
   //End the message when the '>' symbol is received
   else if(incomingByte == '>')
   {
     //Serial.println("c");
     ended = true;
     break; // Done reading - exit from while loop!
   }
   //Read the message!
   else if(msg.length() < 100)
   {
      //Serial.println("d");
      msg += incomingByte; // Add char to array
      //Serial.println(msg);
   }
  } 
 
  //Serial.println(started);
  //Serial.println(ended);

  if(started && ended)
  {
    //Serial.println("e");
    //store / return message
    Serial.println(msg);
    msg = "";
    started = false;
    ended = false;
  }
  
  

  delay(1000);
}