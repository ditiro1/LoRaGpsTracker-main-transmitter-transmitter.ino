/*************************************************************************************************
 *  Created By: NewEra TEL324 STUDENTS 
 *  Created On: 23 SEP, 2024
 *  ANIMAL_TRACKING_SYSTEM 
 *  LoRa-Blink-RECIEVER
 ***********************************************************************************************
 *  Install the following libraries :
 *  1. AltSoftSerial - https://github.com/PaulStoffregen/AltSoftSerial
 *  2. TinyGPSPlus - Version 1.0.3
 ***********************************************************************************************/

#include <SoftwareSerial.h>

#define RX 5
#define TX 4
SoftwareSerial LoRaSerial(RX, TX); // RX, TX

void setup() {
  Serial.begin(115200); // USB Serial
  delay(1000);
  
  LoRaSerial.begin(115200); // LoRa Software Serial 
}

void loop() {
  // Check if data is available on Software Serial
  while (LoRaSerial.available()) {
    String data = LoRaSerial.readString();
    //String response = LoRaSerial.readStringUntil('\n');
    Serial.println(data); // Send data to USB Serial
  }
}
