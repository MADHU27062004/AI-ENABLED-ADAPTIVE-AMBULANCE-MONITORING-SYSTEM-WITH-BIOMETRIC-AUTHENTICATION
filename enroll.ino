#include <Adafruit_Fingerprint.h>

HardwareSerial mySerial(2);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

int enrollID = -1;

void setup() {
  Serial.begin(9600);
  mySerial.begin(57600, SERIAL_8N1, 16, 17);
  finger.begin(57600);

  if (finger.verifyPassword()) {
    Serial.println("Fingerprint sensor ready!");
  } else {
    Serial.println("Fingerprint sensor not found");
    while (1);
  }

  Serial.println("Type ID number (1–127) in Serial Monitor and press Enter:");
}

void loop() {
  // Read ID from Serial Monitor
  if (Serial.available()) {
    enrollID = Serial.parseInt();
    if (enrollID > 0 && enrollID < 128) {
      Serial.print("Enrolling ID: ");
      Serial.println(enrollID);
      enrollFingerprint(enrollID);
      Serial.println("Type next ID to enroll:");
    } else {
      Serial.println("Invalid ID. Use 1–127");
    }
    while (Serial.available()) Serial.read(); // clear buffer
  }
}

/* ---------- ENROLL FUNCTION ---------- */
void enrollFingerprint(int id) {
  int p = -1;
  Serial.println("Place finger on sensor");

  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
  }

  p = finger.image2Tz(1);
  if (p != FINGERPRINT_OK) {
    Serial.println("Image convert failed");
    return;
  }

  Serial.println("Remove finger");
  delay(2000);

  p = 0;
  Serial.println("Place same finger again");

  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
  }

  p = finger.image2Tz(2);
  if (p != FINGERPRINT_OK) {
    Serial.println("Second image failed");
    return;
  }

  p = finger.createModel();
  if (p != FINGERPRINT_OK) {
    Serial.println("Finger mismatch");
    return;
  }

  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    Serial.println("Fingerprint Enrolled Successfully!");
  } else {
    Serial.println("Store failed");
  }
}
