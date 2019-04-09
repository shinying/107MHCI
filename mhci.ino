#include <Adafruit_NeoPixel.h>

#define PIN     6
#define ledPin  13

Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

int i = 0;
int j = 0;
uint32_t colors[4] = {strip.Color(255, 0, 0), strip.Color(0, 255, 0),
                strip.Color(255, 255, 0), strip.Color(0, 0, 255)};
void loop() {
  if (Serial.available()) {
    int p = Serial.read();
    if (p == 1) {
      colorWipe(colors[i], 5);
      colorWipe(strip.Color(0, 0, 0), 0);
      ++i;
      if (i > 3) i = 0;
    }
    else if (p == 2) {
      colorWipe(colors[i], 0);
      delay(20);
      colorWipe(strip.Color(0, 0, 0), 0);
      ++i;
      if (i > 3) i = 0;
    }
    else if (p == 3) {
      colorWipe(strip.Color(255, 255, 255), 0);
      colorWipe(strip.Color(0, 0, 0), 0);
    }
    else if (p == 4) {
      if (j == 3) {
        colorWipe(colors[i], 5);
        ++i;
        if (i > 3) i = 0;
        j = 0;
      } else {
        colorWipe(strip.Color(150, 150, 150), 5);
        ++j;
      }
      colorWipe(strip.Color(0, 0, 0), 0);
    }
  }
  
}

void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=strip.numPixels()/2; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.setPixelColor(strip.numPixels()-i-1, c);
      strip.show();
      delay(wait);
  }
}
