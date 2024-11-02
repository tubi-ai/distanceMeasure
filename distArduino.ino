#define trigPin 9 
#define echoPin 8 
#define ledPin 13 
#define potPin A0  
void setup() {   
  Serial.begin(9600);   
  pinMode(trigPin, OUTPUT);   
  pinMode(echoPin, INPUT);   
  pinMode(ledPin, OUTPUT); 
  }  
  void loop() {   
    // Distance measurement  
    digitalWrite(trigPin, LOW);   
    delayMicroseconds(2);   
    digitalWrite(trigPin, HIGH);   
    delayMicroseconds(10);   
    digitalWrite(trigPin, LOW);    
    long duration = pulseIn(echoPin, HIGH);   
    float distance = duration * 0.034 / 2; // Convert to cm  
    // Reading from potentiometer   
    int potValue = analogRead(potPin);   
    float threshold = map(potValue, 0, 1023, 5, 100); // Mapping between 5-100 cm 
    // Send distance and threshold value   
    Serial.print(distance);   
    Serial.print(",");   
    Serial.println(threshold);    
    // If below threshold value, light the LED
    if (distance < threshold) {     
      digitalWrite(ledPin, HIGH);   } 
      else {     digitalWrite(ledPin, LOW);   }    
      delay(500); 
      }
