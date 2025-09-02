// Arduino: GSR + Buzzer (commanded by Python)
const int GSR = A0;
const int BUZZER = 9;

int sensorValue = 0;
int gsr_average = 0;

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);
}

void loop() {
  // Average 10 samples
  long sum = 0;
  for (int i = 0; i < 10; i++) {
    sensorValue = analogRead(GSR);
    sum += sensorValue;
    delay(5);
  }
  gsr_average = sum / 10;

  // Calculate human resistance (from datasheet formula)
  int human_resistance = ((1024 + 2 * gsr_average) * 10000) / (516 - gsr_average);

  // Send BOTH values to Python (comma-separated)
  Serial.print(gsr_average);
  Serial.print(",");
  Serial.println(human_resistance);

  // Receive command from Python to control buzzer
  while (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '1') {
      digitalWrite(BUZZER, HIGH);   // ON
    } else if (cmd == '0') {
      digitalWrite(BUZZER, LOW);    // OFF
    }
  }

  delay(100);
}

