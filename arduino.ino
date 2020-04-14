#include <dht11.h>
#include <BoltDeviceCredentials.h>
#include <BoltIoT-Arduino-Helper.h>
#define DHT11PIN 7

#include <Servo.h> 
#ifndef API_KEY
#define API_KEY   "boltcloudAPI"
#endif
#ifndef DEVICE_ID
#define DEVICE_ID "boltdeviceid"
#endif

int servoPin = 3; 

Servo Servo1;
dht11 DHT11;


String getAnalogData(String *data){
  String retval="";
  retval=retval+analogRead(A1);
  return retval;
  //Serial.read();
}


String getLDR(String *data){
  String LDR="";
  LDR=LDR+analogRead(A5);
  return LDR;
}

String getRain(String *data){
  String r="";
  r=r+analogRead(A3);
  return r;
}

String getTemp(String *data){
  String value = "";
int chk = DHT11.read(DHT11PIN);
  value = value+ (int)DHT11.temperature;
  
  return value;
  }

 String getHum(String *data){
  String value = "";
int chk = DHT11.read(DHT11PIN);
 value = value+ (int)DHT11.humidity;
  
  return value;
  }


void setup () {
 
  Serial.begin (9600);
  Servo1.attach(servoPin);
  pinMode(A1,INPUT);
  pinMode(A5,INPUT);
  pinMode(A3,INPUT);

  Serial.setTimeout(500);
  boltiot.begin(Serial);
  boltiot.setCommandString("Level",getAnalogData);
  
  boltiot.setCommandString("LDR",getLDR);
  
  
  boltiot.setCommandString("Rain",getRain);

  boltiot.setCommandString("getHum",getHum);
  boltiot.setCommandString("getTemp",getTemp); 
  
  
  
  }
 
void loop() {
  
  boltiot.handleCommand();
}
