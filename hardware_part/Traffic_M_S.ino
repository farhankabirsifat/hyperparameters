void setup() {
  Serial.begin(9600);

  // Set all pins as OUTPUT
  for (int pin = 2; pin <= 13; pin++) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW); // Turn off all lights initially
  }
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.length() < 3) return;

    char light = cmd.charAt(0); // G / Y / R
    char dir = cmd.charAt(2);   // N / S / E / W

    int g = getPin("G", dir);
    int y = getPin("Y", dir);
    int r = getPin("R", dir);

    // Turn OFF current direction's lights
    digitalWrite(g, LOW);
    digitalWrite(y, LOW);
    digitalWrite(r, LOW);

    // Turn ON only the requested light
    if (light == 'G') digitalWrite(g, HIGH);
    else if (light == 'Y') digitalWrite(y, HIGH);
    else if (light == 'R') digitalWrite(r, HIGH);
  }
}

int getPin(String color, char dir) {
  if (dir == 'N') {
    if (color == "G") return 2;
    if (color == "Y") return 3;
    if (color == "R") return 4;
  } else if (dir == 'S') {
    if (color == "G") return 5;
    if (color == "Y") return 6;
    if (color == "R") return 7;
  } else if (dir == 'E') {
    if (color == "G") return 8;
    if (color == "Y") return 9;
    if (color == "R") return 10;
  } else if (dir == 'W') {
    if (color == "G") return 11;
    if (color == "Y") return 12;
    if (color == "R") return 13;
  }
  return -1;
}
