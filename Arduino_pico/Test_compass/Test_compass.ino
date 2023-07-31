#include <VescUart.h>
#include <Arduino.h>
#include <Wire.h>
// libraries
#include "bmm150.h"
#include "bmm150_defs.h"


BMM150 bmm = BMM150();

int headingDegrees = 0;
int error = 90;
int p = 0;
int n = 0;
int inByte = '0';

VescUart UART1;
VescUart UART2;

void setup() {
  // put your setup code here, to run once:
  Serial1.setTX(0);
  Serial1.setRX(1);
  Serial1.begin(115200);

  Serial2.setTX(4);
  Serial2.setRX(5);
  Serial2.begin(115200);

   Serial.begin(115200);

    if (bmm.initialize() == BMM150_E_ID_NOT_CONFORM) {
        Serial.println("Chip ID can not read!");
        while (1);
    } else {
        Serial.println("Initialize done!");
    }

      //while (!Serial) {;}
  while (!Serial1) {;}
  while (!Serial2) {;}

  /** Define which ports to use as UART */
  UART1.setSerialPort(&Serial1);
  UART2.setSerialPort(&Serial2);

}

void loop() {
  // put your main code here, to run repeatedly:
   if (Serial.available() > 0){
    int theta = Serial.parseInt();
    p = theta + error;
    n = theta - error;
      calcular();
      compass();
    //  UART1.setDuty(0.1);
    //  UART2.setDuty(0.1);
      
      if(headingDegrees < n){
        UART1.setDuty(0.04);
        UART2.setDuty(0.04);
      }
    
      else if(headingDegrees > p){
        UART1.setDuty(-0.04);
        UART2.setDuty(-0.04);
      }
    
      else if(n <= headingDegrees <= p){
        UART1.setDuty(0.1);
        UART2.setDuty(-0.1);
      }
    
      Serial.print("Heading: ");
      Serial.print(headingDegrees);
      Serial.print(" Input: ");
      Serial.print(theta);
      Serial.print(" p: ");
      Serial.print(p);
      Serial.print(" n: ");
      Serial.print(n);
   }
}

void compass(){
    bmm150_mag_data value;
    bmm.read_mag_data();

    value.x = bmm.raw_mag_data.raw_datax;
    value.y = bmm.raw_mag_data.raw_datay;
    value.z = bmm.raw_mag_data.raw_dataz;

    float xyHeading = atan2(value.x, value.y);
    float zxHeading = atan2(value.z, value.x);
    float heading = xyHeading;

    if (heading < 0) {
        heading += 2 * PI;
    }
    if (heading > 2 * PI) {
        heading -= 2 * PI;
    }
    headingDegrees = heading * 180 / M_PI;
}
void calcular(){
  if(p > 360){
    p = (p + 360) % 360;
  }
  if(n < 0){
    n = (n + 360) % 360;
  }
}
