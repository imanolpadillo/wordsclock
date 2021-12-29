// ********************************************************************************************* //
// ********************************************************************************************* //
// **************************************** WORDSCLOCK ***************************************** //
// ********************************************************************************************* //
// ********************************************************************************************* //
// AUTOR:   Imanol Padillo
// DATE:    29/12/2021
// VERSION: 1.0

// Board: Arduino Mega
// Processor: Atmega 2560 (Mega 2560)
// Port: /dev/cu.wchusbserial1420
// External module: RTC DS3213
//      DS3213    |    Arduino Mega
// __________________________________
//        SCL     |       A5
//        SDA     |       A4
//        Vcc     |       5V
//        GND     |      GND

// ********************************************************************************************* //
// INCLUDES 
// ********************************************************************************************* //
#include <Wire.h>
#include "RTClib.h"

// ********************************************************************************************* // 
// CONSTANTS
// ********************************************************************************************* //
#define GPIO_HOUR_UP            2
#define GPIO_MINUTE_UP          3
#define GPIO_E                  22
#define GPIO_S                  23
#define GPIO_ON                 24
#define GPIO_LA                 25
#define GPIO_S_2                26
#define GPIO_UNA                27
#define GPIO_DOS                28
#define GPIO_TRES               29
#define GPIO_CUATRO             30
#define GPIO_CINCO              31
#define GPIO_SEIS               32
#define GPIO_SIETE              33
#define GPIO_OCHO               34
#define GPIO_NUEVE              35
#define GPIO_DIEZ               36
#define GPIO_ONCE               37
#define GPIO_DOCE               38
#define GPIO_Y                  39
#define GPIO_MENOS              40
#define GPIO_VEINTE             41
#define GPIO_DIEZ               42
#define GPIO_VEINTI             43
#define GPIO_CINCO              44
#define GPIO_MEDIA              45
#define GPIO_CUARTO             46


// ********************************************************************************************* // 
// GLOBAL VARIABLES
// ********************************************************************************************* //
RTC_DS3231 rtc;
int lastHour;
int lastMinute;


// ********************************************************************************************* // 
// SETUP
// ********************************************************************************************* //
void setup() {
   Serial.begin(9600);
   delay(1000); 
   if (!rtc.begin()) {
      Serial.println(F("Couldn't find RTC"));
      while (1);
   }
   // In case of lost of power supply, set date to compilation date
   if (rtc.lostPower()) {
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
      // Set specific date, for example; 21st of January 2016 at 03:00:00
      // rtc.adjust(DateTime(2016, 1, 21, 3, 0, 0));
   }
   // Switch off leds
   switchOffLeds();
   // Init interrupts
   pinMode(GPIO_HOUR_UP, INPUT);
   pinMode(GPIO_MINUTE_UP, INPUT);
   attachInterrupt(digitalPinToInterrupt(GPIO_HOUR_UP), increaseHour, FALLING);
   attachInterrupt(digitalPinToInterrupt(GPIO_MINUTE_UP), increaseMinute, FALLING);
}


// ********************************************************************************************* // 
// MAIN
// ********************************************************************************************* //
void loop() {
   // Get current date and print the suitable leds
   DateTime now = rtc.now();
   printDate(now);
   delay(30000);
}


// ********************************************************************************************* // 
// FUNCTIONS
// ********************************************************************************************* /
// increaseHour: increases the hour for each new interrupt
void increaseHour(){
  DateTime now = rtc.now();
  int newHour;
  if (now.hour() == 23){
    newHour = 0;
  }
  else{
    newHour = newHour+1;
  }
  rtc.adjust(DateTime(now.year(), now.month(), now.year(), newHour, now.minute(), now.second()));
}

// increaseMinute: increases the minutes for each new interrupt
void increaseMinute(){
  DateTime now = rtc.now();
  int newMinute;
  newMinute = ((now.minute() % 5) + 1) * 5;
  if (newMinute >= 60){
    newMinute = 0;
  }
  rtc.adjust(DateTime(now.year(), now.month(), now.year(), now.hour(), newMinute, now.second()));
}

// printDate: Switches on the suitable leds depending on current time
void printDate(DateTime date)
{
   // Get current hour & minute
   int currentHour;
   int currentMinute;
   currentHour = date.hour();
   currentMinute = (date.minute() % 5) * 5;

   // Check for a change in time
   if ((currentHour!=lastHour) or (currentMinute!=lastMinute)){
     lastHour = currentHour;  
     lastMinute = currentMinute;

     // Serial print time
     Serial.print(currentHour);
     Serial.print(':');
     Serial.println(currentMinute);

     // Switch off leds
     switchOffLeds();

     // Print 'ES LA' or 'SON LAS'
     if (currentHour==1 or currentHour==13) {
       digitalWrite(GPIO_E,HIGH);
       digitalWrite(GPIO_S,HIGH);
       digitalWrite(GPIO_LA,HIGH);
     }
     else{
       digitalWrite(GPIO_S,HIGH);
       digitalWrite(GPIO_ON,HIGH);
       digitalWrite(GPIO_LA,HIGH);
       digitalWrite(GPIO_S_2,HIGH);
     }

     // Print hour
     if (currentHour==1 or currentHour==13) {
       digitalWrite(GPIO_UNA,HIGH);
     }
     else if (currentHour==2 or currentHour==14) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==3 or currentHour==15) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==4 or currentHour==16) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==5 or currentHour==17) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==6 or currentHour==18) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==7 or currentHour==19) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==8 or currentHour==20) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==9 or currentHour==21) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==10 or currentHour==22) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==11 or currentHour==23) {
       digitalWrite(GPIO_DOS,HIGH);
     }
     else if (currentHour==12 or currentHour==0) {
       digitalWrite(GPIO_DOS,HIGH);
     }

     // Print '-', 'Y' or 'MENOS'
     if (currentMinute==5 or currentMinute==10 or currentMinute==15 or 
       currentMinute==20 or currentMinute==25 or currentMinute==30) {
       digitalWrite(GPIO_Y,HIGH);
     }
     else if (currentMinute==35 or currentMinute==40 or currentMinute==45 or 
       currentMinute==50 or currentMinute==55){
       digitalWrite(GPIO_MENOS,HIGH);
     }

     // Print minutes
     if (currentMinute==5 or currentMinute==55) {
       digitalWrite(GPIO_CINCO,HIGH);
     }
     else if (currentMinute==10 or currentMinute==50) {
       digitalWrite(GPIO_DIEZ,HIGH);
     }
     else if (currentMinute==15 or currentMinute==45) {
       digitalWrite(GPIO_CUARTO,HIGH);
     }
     else if (currentMinute==20 or currentMinute==40) {
       digitalWrite(GPIO_VEINTE,HIGH);
     }
     else if (currentMinute==25 or currentMinute==35) {
       digitalWrite(GPIO_VEINTI,HIGH);
       digitalWrite(GPIO_CINCO,HIGH);
     }
     
   }
}


// switchOffLeds: Switch off all digital outputs
void switchOffLeds(){
  for (int i=22; i<46; i++){
    digitalWrite(i,LOW);
  }
}
