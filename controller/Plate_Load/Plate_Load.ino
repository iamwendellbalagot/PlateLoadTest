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

int SIZE = 100;

HX711 scale;

void setup() {
  Serial.begin(9600);
  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
 //Assuming there is no weight on the scale at start up, reset the scale to 0
}

void loop() {
  
  float disp1_val[SIZE];
  float disp2_val[SIZE];
  float loadc = scale.get_units() / 2.2;

  for (int i =0; i<SIZE; i++){
    float volts1 = analogRead(sensor1)*0.0048828125;
    float volts2 = analogRead(sensor2)*0.0048828125;  
    
    float disp1 = 60.374 * pow(volts1, -1.16);
    float disp2 = 60.374 * pow(volts2, -1.16);
    

    disp1_val[i] = disp1;
    disp2_val[i] = disp2;
  }

  float d1= 0;
  float d2= 0;

  for (int i =0; i<SIZE; i++){
    d1 = d1 + disp1_val[i];
    d2 = d2 + disp2_val[i];
  }

  d1 = (d1/SIZE);
  d2 = (d2/SIZE);
  loadc = loadc - 0.35;
  if (loadc <0){
    loadc = 0.0;
  }
  
  
  Serial.print(d1);
  Serial.print('\t');
  Serial.print(d2);
  Serial.print('\t');
  Serial.println(loadc);
  delay(1000);
}
