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
//        SCL  4  |       A5
//        SDA  3  |       A4
//        Vcc  2  |       5V
//        GND  1  |      GND

// ********************************************************************************************* //
// INCLUDES 
// ********************************************************************************************* //
#include <Wire.h>
#include "RTClib.h"
#include <LowPower.h>

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
#define GPIO_DOS                49
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
#define GPIO_DIEZ_2             42
#define GPIO_VEINTI             43
#define GPIO_CINCO_2            47
#define GPIO_MEDIA              48
#define GPIO_CUARTO             46


// ********************************************************************************************* // 
// GLOBAL VARIABLES
// ********************************************************************************************* //
RTC_DS3231 rtc;
int lastHour;
int lastMinute;
volatile bool increaseHourFlag = false;
volatile bool increaseMinuteFlag = false;


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
   attachInterrupt(digitalPinToInterrupt(GPIO_HOUR_UP), increaseHourInterrupt, FALLING);
   attachInterrupt(digitalPinToInterrupt(GPIO_MINUTE_UP), increaseMinuteInterrupt, FALLING);

   pinMode(GPIO_E, OUTPUT);
   pinMode(GPIO_S, OUTPUT);
   pinMode(GPIO_ON, OUTPUT);
   pinMode(GPIO_LA, OUTPUT);
   pinMode(GPIO_S_2, OUTPUT);
   pinMode(GPIO_UNA, OUTPUT);
   pinMode(GPIO_DOS, OUTPUT);
   pinMode(GPIO_TRES, OUTPUT);
   pinMode(GPIO_CUATRO, OUTPUT);
   pinMode(GPIO_CINCO, OUTPUT);
   pinMode(GPIO_SEIS, OUTPUT);
   pinMode(GPIO_SIETE, OUTPUT);
   pinMode(GPIO_OCHO, OUTPUT);
   pinMode(GPIO_NUEVE, OUTPUT);
   pinMode(GPIO_DIEZ, OUTPUT);
   pinMode(GPIO_ONCE, OUTPUT);
   pinMode(GPIO_DOCE, OUTPUT);
   pinMode(GPIO_Y, OUTPUT);
   pinMode(GPIO_MENOS, OUTPUT);
   pinMode(GPIO_VEINTE, OUTPUT);
   pinMode(GPIO_DIEZ_2, OUTPUT);
   pinMode(GPIO_VEINTI, OUTPUT);
   pinMode(GPIO_CINCO_2, OUTPUT);
   pinMode(GPIO_MEDIA, OUTPUT);
   pinMode(GPIO_CUARTO, OUTPUT);

   // test leds
   switchOnLeds();
   delay(5000);
   switchOffLeds();

}


// ********************************************************************************************* // 
// MAIN
// ********************************************************************************************* //
void loop() {
   //LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  //works!!! but serial.print not...
   //LowPower.idle(SLEEP_8S, ADC_OFF, TIMER5_OFF, TIMER4_OFF, TIMER3_OFF, 
   //    TIMER2_OFF, TIMER1_OFF, TIMER0_OFF, SPI_OFF, USART3_OFF, 
   //    USART2_OFF, USART1_OFF, USART0_OFF, TWI_OFF);
   
   // Get current date and print the suitable leds
   printDate();

   // check increase time
   if (increaseHourFlag == true){
     increaseHour();
     delay(1000);
     increaseHourFlag = false;
   }
   else if (increaseMinuteFlag == true){
     increaseMinute();
     delay(1000);
     increaseMinuteFlag = false;
   }
}


// ********************************************************************************************* // 
// FUNCTIONS
// ********************************************************************************************* //

// increaseHourInterrupt: increases the hour flag
void increaseHourInterrupt(){
  increaseHourFlag = true;
}

// increaseHour: increases the hour for each new interrupt
void increaseHour(){
  Serial.println("Increase_hour");
  DateTime now = rtc.now();
  int newHour;
  if (now.hour() == 23){
    newHour = 0;
  }
  else{
    newHour = now.hour()+1;
  }
  rtc.adjust(DateTime(now.year(), now.month(), now.year(), newHour, now.minute(), now.second()));
}

// increaseMinuteInterrupt: increases the minute flag
void increaseMinuteInterrupt(){
  increaseMinuteFlag = true;
}

// increaseMinute: increases the minutes for each new interrupt
void increaseMinute(){
  Serial.println("Increase_minute");
  DateTime now = rtc.now();
  int newMinute;
  newMinute = (int((now.minute() / 5)) + 1) * 5;
  if (newMinute >= 60){
    newMinute = 0;
  }
  rtc.adjust(DateTime(now.year(), now.month(), now.year(), now.hour(), newMinute, 0));
}

// printDate: Switches on the suitable leds depending on current time
void printDate()
{
   DateTime date = rtc.now();
   // Get current hour & minute
   int currentHour;
   int currentMinute;
   currentHour = date.hour();
   currentMinute = int((date.minute() / 5)) * 5;

   
   Serial.print(date.hour(),DEC);
   Serial.print(':');
   Serial.print(date.minute(),DEC);
   Serial.print(" --> ");
   Serial.print(currentHour);
   Serial.print(':');
   Serial.print(currentMinute);
   Serial.print(" --> ");
   Serial.print(lastHour);
   Serial.print(':');
   Serial.println(lastMinute);

   // Check for a change in time
   if ((currentHour!=lastHour) or (currentMinute!=lastMinute)){
     lastHour = currentHour;  
     lastMinute = currentMinute;

     // Serial print time
     Serial.println("Change Time");
     Serial.print(currentHour);
     Serial.print(':');
     Serial.println(currentMinute);

     // Switch off leds
     switchOffLeds();

     // Adapt to "to" hours
     if (currentMinute==35 or currentMinute==40 or currentMinute==45 or 
       currentMinute==50 or currentMinute==55){
       currentHour+=1;
     }

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
       digitalWrite(GPIO_TRES,HIGH);
     }
     else if (currentHour==4 or currentHour==16) {
       digitalWrite(GPIO_CUATRO,HIGH);
     }
     else if (currentHour==5 or currentHour==17) {
       digitalWrite(GPIO_CINCO,HIGH);
     }
     else if (currentHour==6 or currentHour==18) {
       digitalWrite(GPIO_SEIS,HIGH);
     }
     else if (currentHour==7 or currentHour==19) {
       digitalWrite(GPIO_SIETE,HIGH);
     }
     else if (currentHour==8 or currentHour==20) {
       digitalWrite(GPIO_OCHO,HIGH);
     }
     else if (currentHour==9 or currentHour==21) {
       digitalWrite(GPIO_NUEVE,HIGH);
     }
     else if (currentHour==10 or currentHour==22) {
       digitalWrite(GPIO_DIEZ,HIGH);
     }
     else if (currentHour==11 or currentHour==23) {
       digitalWrite(GPIO_ONCE,HIGH);
     }
     else if (currentHour==12 or currentHour==0 or currentHour==24) {
       digitalWrite(GPIO_DOCE,HIGH);
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
       digitalWrite(GPIO_CINCO_2,HIGH);
     }
     else if (currentMinute==10 or currentMinute==50) {
       digitalWrite(GPIO_DIEZ_2,HIGH);
     }
     else if (currentMinute==15 or currentMinute==45) {
       digitalWrite(GPIO_CUARTO,HIGH);
     }
     else if (currentMinute==20 or currentMinute==40) {
       digitalWrite(GPIO_VEINTE,HIGH);
     }
     else if (currentMinute==25 or currentMinute==35) {
       digitalWrite(GPIO_VEINTI,HIGH);
       digitalWrite(GPIO_CINCO_2,HIGH);
     }
     else if (currentMinute==30) {
       digitalWrite(GPIO_MEDIA,HIGH);
     }
     
   }
}


// switchOffLeds: Switch off all digital outputs
void switchOffLeds(){
  for (int i=20; i<=49; i++){
    digitalWrite(i,LOW);
  }
}

// switchOnLeds: Switch on all digital outputs
void switchOnLeds(){
  for (int i=20; i<=49; i++){
    digitalWrite(i,HIGH);
  }
}
