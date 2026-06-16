#include <Wire.h>
#include <LiquidCrystal_I2C.h>  
#include <DHT.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);


#define DHTPIN 2     
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);


String candidateName = "IGIHOZO Belise"; 


int scrollIndex = 0;
int nameLength = 0;
unsigned long previousMillis = 0;
const long interval = 2000; 

void setup() {
  Serial.begin(9600);
  
  lcd.init();          
  lcd.backlight();     
  lcd.clear();
  
  dht.begin();
  pinMode(DHTPIN, INPUT_PULLUP);
  
  nameLength = candidateName.length();
  
  
  lcd.setCursor(0, 0);
  if (nameLength <= 16) {
    lcd.print(candidateName);
  } else {
    lcd.print(candidateName.substring(0, 16));
  }
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

  
    float humidity = dht.readHumidity();
    float temperatureC = dht.readTemperature();
   
    if (isnan(humidity) || isnan(temperatureC)) {
      Serial.println("Sensor Error!");
      lcd.setCursor(0, 1);
      lcd.print("Sensor Error!   ");
      return;
    }

   
    lcd.setCursor(0, 1);
    lcd.print("T:");
    lcd.print(temperatureC, 1);
    lcd.print("C H:");
    lcd.print(humidity, 0);
    lcd.print("%   "); 

 
    if (nameLength > 16) {
      String displayText = candidateName + "    "; 
      lcd.setCursor(0, 0);
      lcd.print(displayText.substring(scrollIndex, scrollIndex + 16));
      
      scrollIndex++;
      if (scrollIndex > nameLength) {
        scrollIndex = 0;
      }
    }

   
    Serial.print("TEMP:");
    Serial.print(temperatureC);
    Serial.print(",HUM:");
    Serial.println(humidity);
  }
}