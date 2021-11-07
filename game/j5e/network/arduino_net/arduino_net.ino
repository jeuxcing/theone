

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

uint8_t i = 0;
unsigned long time = 0;
unsigned long led_time = 0;

void loop() {
  unsigned long t = millis();
  if (t - time > 1000) {
    time = t;
    Serial.write(i++);
    Serial.flush();
  }

  if (t - led_time > 1500)
    digitalWrite(LED_BUILTIN, LOW);

  bool data = false;
  while (Serial.available() > 0) {
    data = true;
    Serial.read();
  }
    
  if (data) {
    digitalWrite(LED_BUILTIN, HIGH);
    led_time = millis();
  }
}
