//From bildr article: http://bildr.org/2012/08/rotary-encoder-arduino/


//
//
//  ° CLK    
//              ° SW
//  ° GND
//              ° GND
//  ° DT


//Potar 1
int potA1 = 2; // DT 
int potA2 = 3; //CLK
int lastEncoded1 = 0;
long encoderValue1 = 0;


//Potar 2
int potB1 = 4; //DT
int potB2 = 5; //CLK
int lastEncoded2 = 0;
long encoderValue2 = 0;



bool valueChanged = false;

void setup() {
  Serial.begin (9600);

  // Initialiser les pin
  pinMode(potA1, INPUT);
  pinMode(potA2, INPUT);

  digitalWrite(potA1, HIGH); 
  digitalWrite(potA2, HIGH); 

  pinMode(potB1, INPUT);
  pinMode(potB2, INPUT);

  digitalWrite(potB1, HIGH); 
  digitalWrite(potB2, HIGH); 
  
}

void loop(){
  //Do stuff here
  if(valueChanged){
      Serial.print("Potar 1:");
      Serial.println(encoderValue1);
      
      Serial.print("Potar 2:");
      Serial.println(encoderValue2);
      Serial.println();

      valueChanged = false;
  }
  delay(1); //just here to slow down the output, and show it will work even during a delay

  //Vérifier la mise à jour de la rotation
  valueChanged = updateEncoder(potA1,potA2, &encoderValue1, &lastEncoded1);
  valueChanged += updateEncoder(potB1,potB2, &encoderValue2, &lastEncoded2);

}

bool updateEncoder(int pin1, int pin2, long *encoderValue, int *lastEncoded){
  int MSB = digitalRead(pin1);
  int LSB = digitalRead(pin2); 
  bool updatedValue = false;

  int encoded = (MSB << 1) |LSB; 
  int sum = (*lastEncoded << 2) | encoded;
  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
    (*encoderValue) +=1;
    updatedValue=true;
  }
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000){
    (*encoderValue) -=1;
    updatedValue=true;
  }
  (*lastEncoded) = encoded; 

  return updatedValue;
}
