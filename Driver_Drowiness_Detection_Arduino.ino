const int GSR = A0;   // GSR sensor connected to analog pin A0
int sensorValue = 0;
int gsr_average = 0;

void setup() {
  Serial.begin(9600);  // Start serial monitor
}

void loop() {
  long sum = 0;

  // Take 10 samples and average
  for (int i = 0; i < 10; i++) {
    sensorValue = analogRead(GSR);
    sum += sensorValue;
    delay(5);
  }

  gsr_average = sum / 10;

  // Print average GSR value
  Serial.print("gsr_average = ");
  Serial.println(gsr_average);

  // Calculate human resistance based on GSR datasheet formula
  int human_resistance = ((1024 + 2 * gsr_average) * 10000) / (516 - gsr_average);

  Serial.print("human_resistance = ");
  Serial.println(human_resistance);

  delay(2000);  // Wait before next reading
}



