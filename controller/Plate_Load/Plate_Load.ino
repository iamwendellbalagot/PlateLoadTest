//#define sensor A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)
//
//void setup() {
//  Serial.begin(9600); // start the serial port
//}
//
//void loop() {
//  
//  // 5v
//  float volts = analogRead(sensor)*0.0048828125;  // value from sensor * (5/1024)
//  float distance = 12.08*pow(volts , -1.058); // worked out from datasheet graph
//  delay(1000); // slow down serial port 
//  
//  Serial.println(distance);   // print the distance
//
//}

#include "HX711.h"
#define sensor1 A0
#define sensor2 A1
#define calibration_factor 7050.0 //This value is obtained using the SparkFun_HX711_Calibration sketch

#define DOUT  3
#define CLK  2

HX711 scale;

void setup() {
  Serial.begin(9600);
  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
}

void loop() {
  float volts1 = analogRead(sensor1)*0.0048828125;
  float volts2 = analogRead(sensor2)*0.0048828125;  
  
  float disp1 = 60.374 * pow(volts1, -1.16);
  float disp2 = 60.374 * pow(volts2, -1.16);
  float loadc = scale.get_units();
  
  Serial.print(disp1);
  Serial.print('\t');
  Serial.print(disp2);
  Serial.print('\t');
  Serial.println(loadc/2.2);
  delay(1000);
}
