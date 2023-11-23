
/*
#include <Wire.h>
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"
#include "arduinoFFT.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for SSD1306 display connected using I2C
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


arduinoFFT FFT = arduinoFFT(); /* Create FFT object */


/*
#define CHANNEL A0 // Output of the AD8232
const uint16_t samples = 128; // This value MUST ALWAYS be a power of 2
const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC

unsigned int sampling_period_us;
unsigned long microseconds;

double vReal[samples];
double vImag[samples];
double vPSDs[samples];

void setup() {
  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
  Serial.begin(115200);
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS); // Initialize with the I2C address

  display.display(); // Initialize with the I2C address

  display.clearDisplay(); // Clear the display buffer

  // Initialize the OLED display with text
  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // White text
  display.setCursor(0, 0);     // Start at top-left corner
  display.println("FFT Data:");

  display.display(); // Show initial text

}

void loop() {
  //SAMPLING
  microseconds = micros();
  for (int i = 0; i < samples; i++) {
    vReal[i] = analogRead(CHANNEL) - 512.0;  // Modified for zero balance
    vImag[i] = 0;
    while (micros() - microseconds < sampling_period_us) {
      // Empty loop
    }
    microseconds += sampling_period_us;
  }

  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, samples);
  PrintVector(vReal, (samples >> 1));

  // Clear the display buffer
  display.clearDisplay();

  // Display text on OLED
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);

  for (int i = 0; i < (samples >> 1); i++) {
    display.print("Freq: ");
    display.print((i * 1.0 * samplingFrequency) / samples, 2);
    display.print(" Hz, PSD: ");
    display.println(vPSDs[i], 2);
  }

  // Display the graph on OLED
  display.display();

  delay(1000);
}

void PrintVector(double *vData, uint16_t bufferSize) {
  for (uint16_t i = 0; i < bufferSize; i++) {
    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
  }
}
*/







//
//#include <SPI.h>
//#include <Wire.h>
//#include <Adafruit_GFX.h>
//#include <Adafruit_SSD1306.h>
//#include "arduinoFFT.h"
//
//#define SCREEN_WIDTH 128 // OLED display width, in pixels
//#define SCREEN_HEIGHT 64 // OLED display height, in pixels
//
//// Declaration for SSD1306 display connected using I2C
//#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
//#define SCREEN_ADDRESS 0x3C
//Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
//
//arduinoFFT FFT = arduinoFFT(); /* Create FFT object */
//
//#define CHANNEL A0 // Output of the AD8232
//const uint16_t samples = 64; // Reduced sample size
//const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC
//
//unsigned int sampling_period_us;
//unsigned long microseconds;
//
//double vReal[samples]; // Use double data type
//double vImag[samples]; // Use double data type
//double vPSDs[samples]; // Use double data type
//
//void setup() {
//  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
//  Serial.begin(115200);
//  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS); // Initialize with the I2C address
//
//  display.display(); // Initialize with the I2C address
//
//  display.clearDisplay(); // Clear the display buffer
//
//  // Initialize the OLED display with text
//  display.setTextSize(1);      // Normal 1:1 pixel scale
//  display.setTextColor(WHITE); // White text
//  display.setCursor(0, 0);     // Start at top-left corner
//  display.println("FFT Data:");
//
//  display.display(); // Show initial text
//
//  delay(2000);
//
//}
//
//void loop() {
//  
//  /*SAMPLING*/
//  microseconds = micros();
//  for (int i = 0; i < samples; i++) {
//    // Convert the float sample to double
//    vReal[i] = static_cast<double>(analogRead(CHANNEL) - 512.0); // Modified for zero balance
//    vImag[i] = 0;
//    while (micros() - microseconds < sampling_period_us) {
//      // Empty loop
//    }
//    microseconds += sampling_period_us;
//  }
//
//  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
//  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
//  FFT.ComplexToMagnitude(vReal, vImag, samples);
//  PrintVector(vReal, (samples >> 1));
//
//  // Clear the display buffer
//  display.clearDisplay();
//
//  // Display text on OLED
//  display.setTextSize(1);
//  display.setTextColor(SSD1306_WHITE);
//  display.setCursor(0, 0);
//
//  for (int i = 0; i < (samples >> 1); i++) {
//    display.print("Freq: ");
//    display.print((i * 1.0 * samplingFrequency) / samples, 2);
//    display.print(" Hz, PSD: ");
//    display.println(vPSDs[i], 2);
//  }
//
//  // Display the graph on OLED
//  display.display();
//
//  delay(1000);
//}
//
//void PrintVector(double *vData, uint16_t bufferSize) {
//  for (uint16_t i = 0; i < bufferSize; i++) {
//    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
//  }
//}

/* sdjfksjfhskdjfhskdj new code */

//
//#include <Wire.h>
//#include "Adafruit_GFX.h"
//#include "Adafruit_SSD1306.h"
//#include "arduinoFFT.h"
//
//#define SCREEN_WIDTH 128 // OLED display width, in pixels
//#define SCREEN_HEIGHT 64 // OLED display height, in pixels
//
//// Declaration for SSD1306 display connected using I2C
//#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
//#define SCREEN_ADDRESS 0x3C
//Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
//
//arduinoFFT FFT = arduinoFFT(); /* Create FFT object */
//
//#define CHANNEL A0 // Output of the AD8232
//const uint16_t samples = 64; // Reduced sample size
//const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC
//
//unsigned int sampling_period_us;
//unsigned long microseconds;
//
//double vReal[samples]; // Use double data type
//double vImag[samples]; // Use double data type
//double vPSDs[samples]; // Use double data type
//
//void setup() {
//  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
//  Serial.begin(115200);
//
//  // Initialize the OLED object
//  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
//    Serial.println(F("SSD1306 allocation failed"));
//    for (;;)
//      ; // Don't proceed, loop forever
//  }
//
//  // Clear the buffer.
//  display.clearDisplay();
//
//  // Display Text
//  display.setTextSize(1);
//  display.setTextColor(WHITE);
//  display.setCursor(0, 28);
//  display.println("FFT Data:");
//  display.display();
//}
//
//void loop() {
//  /*SAMPLING*/
//  microseconds = micros();
//  for (uint16_t i = 0; i < samples; i++) {
//    // Convert the float sample to double
//    vReal[i] = static_cast<double>(analogRead(CHANNEL) - 512.0); // Modified for zero balance
//    vImag[i] = 0;
//    while (micros() - microseconds < sampling_period_us) {
//      // Empty loop
//    }
//    microseconds += sampling_period_us;
//  }
//
//  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
//  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
//  FFT.ComplexToMagnitude(vReal, vImag, samples);
//  PrintVector(vReal, (samples >> 1));
//
//  // Clear the display buffer.
//  display.clearDisplay();
//
//  // Display FFT results on OLED
//  display.setTextSize(1);
//  display.setTextColor(WHITE);
//  display.setCursor(0, 28);
//
//  for (uint16_t i = 0; i < (samples >> 1); i++) {
//    display.print("Freq: ");
//    display.print((i * 1.0 * samplingFrequency) / samples, 2);
//    display.print(" Hz, PSD: ");
//    display.println(vPSDs[i], 2);
//  }
//
//  // Update the OLED display.
//  display.display();
//
//  // Delay for a while before the next FFT measurement.
//  delay(1000);
//}
//
//void PrintVector(double *vData, uint16_t bufferSize) {
//  for (uint16_t i = 0; i < bufferSize; i++) {
//    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
//  }
//}
//
//




/* this is yet another code */


//#include <Wire.h>
//#include "Adafruit_GFX.h"
//#include "Adafruit_SSD1306.h"
//#include "arduinoFFT.h"
//
//#define SCREEN_WIDTH 128 // OLED display width, in pixels
//#define SCREEN_HEIGHT 64 // OLED display height, in pixels
//
//// Declaration for SSD1306 display connected using I2C
//#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
//#define SCREEN_ADDRESS 0x3C
//Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
//
//arduinoFFT FFT = arduinoFFT(); /* Create FFT object */
//
//#define CHANNEL A0 // Output of the AD8232
//const uint16_t samples = 64; // Reduced sample size
//const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC
//
//unsigned int sampling_period_us;
//unsigned long microseconds;
//
//double vReal[samples]; // Use double data type
//double vImag[samples]; // Use double data type
//double vPSDs[samples]; // Use double data type
//
//void setup() {
//  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
//  Serial.begin(115200);
//
//  // Initialize the OLED object
//  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
//    Serial.println(F("SSD1306 allocation failed"));
//    for (;;)
//      ; // Don't proceed, loop forever
//  }
//
//  // Clear the buffer.
//  display.clearDisplay();
//
//  // Display Text
//  display.setTextSize(1);
//  display.setTextColor(WHITE);
//  display.setCursor(0, 28);
//  display.println("FFT Data:");
//  display.display();
//}
//
//void loop() {
//  /*SAMPLING*/
//  microseconds = micros();
//  for (uint16_t i = 0; i < samples; i++) {
//    // Convert the float sample to double
//    vReal[i] = static_cast<double>(analogRead(CHANNEL) - 512.0); // Modified for zero balance
//    vImag[i] = 0;
//    while (micros() - microseconds < sampling_period_us) {
//      // Empty loop
//    }
//    microseconds += sampling_period_us;
//  }
//
//  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
//  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
//  FFT.ComplexToMagnitude(vReal, vImag, samples);
//  PrintVector(vReal, (samples >> 1));
//
//  // Clear the display buffer.
//  display.clearDisplay();
//
//  // Display FFT results on OLED
//  display.setTextSize(1);
//  display.setTextColor(WHITE);
//  display.setCursor(0, 28);
//
//  for (uint16_t i = 0; i < (samples >> 1); i++) {
//    display.print("Freq: ");
//    display.print((i * 1.0 * samplingFrequency) / samples, 2);
//    display.print(" Hz, PSD: ");
//    display.println(vPSDs[i], 2);
//  }
//
//  // Update the OLED display.
//  display.display();
//
//  // Print the FFT results to the serial monitor for debugging
//  for (uint16_t i = 0; i < (samples >> 1); i++) {
//    Serial.print("Freq: ");
//    Serial.print((i * 1.0 * samplingFrequency) / samples, 2);
//    Serial.print(" Hz, PSD: ");
//    Serial.println(vPSDs[i], 2);
//  }
//
//  // Delay for a while before the next FFT measurement.
//  delay(1000);
//}
//
//void PrintVector(double *vData, uint16_t bufferSize) {
//  for (uint16_t i = 0; i < bufferSize; i++) {
//    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
//  }
//}



/* Well.... that didnt work */

//#include <Wire.h>
//#include "arduinoFFT.h"
//
//arduinoFFT FFT = arduinoFFT(); /* Create FFT object */
//
//#define CHANNEL A0 // Output of the AD8232
//const uint16_t samples = 64; // Reduced sample size
//const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC
//
//unsigned int sampling_period_us;
//unsigned long microseconds;
//
//double vReal[samples]; // Use double data type
//double vImag[samples]; // Use double data type
//double vPSDs[samples]; // Use double data type
//
//void setup() {
//  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
//  Serial.begin(115200);
//}
//
//void loop() {
//  /*SAMPLING*/
//  microseconds = micros();
//  for (uint16_t i = 0; i < samples; i++) {
//    // Convert the float sample to double
//    vReal[i] = static_cast<double>(analogRead(CHANNEL) - 512.0); // Modified for zero balance
//    vImag[i] = 0;
//    while (micros() - microseconds < sampling_period_us) {
//      // Empty loop
//    }
//    microseconds += sampling_period_us;
//  }
//
//  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
//  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
//  FFT.ComplexToMagnitude(vReal, vImag, samples);
//  PrintVector(vReal, (samples >> 1));
//
//  // Delay for a while before the next FFT measurement.
//  delay(1000);
//}
//
//void PrintVector(double *vData, uint16_t bufferSize) {
//  for (uint16_t i = 0; i < bufferSize; i++) {
//    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
//  }
//
//  // Output FFT results to the serial monitor
//  for (uint16_t i = 0; i < (bufferSize); i++) {
//    Serial.print("Freq: ");
//    Serial.print((i * 1.0 * samplingFrequency) / samples, 2);
//    Serial.print(" Hz, PSD: ");
//    Serial.println(vPSDs[i], 2);
//  }
//}


//did work but had issues

#include <arduinoFFT.h>

#define CHANNEL A0 // Output of the AD8232
const uint16_t samples = 128; // This value MUST ALWAYS be a power of 2
const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC

unsigned int sampling_period_us;
unsigned long microseconds;

double vReal[samples];
double vImag[samples];
double vPSDs[samples];

arduinoFFT FFT = arduinoFFT(); /* Create FFT object */

void setup() {
  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
  Serial.begin(115200);
}

void loop() {
  /*SAMPLING*/
  microseconds = micros();
  for (int i = 0; i < samples; i++) {
    vReal[i] = analogRead(CHANNEL) - 512.0;  // Modified for zero balance
    vImag[i] = 0;
    while (micros() - microseconds < sampling_period_us) {
      // Empty loop
    }
    microseconds += sampling_period_us;
  }

  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, samples);
  PrintVector(vReal, (samples >> 1));

  delay(1000); // Delay before sending the next data point
}

void PrintVector(double *vData, uint16_t bufferSize) {
  for (uint16_t i = 0; i < bufferSize; i++) {
    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
    Serial.print((i * 1.0 * samplingFrequency) / samples, 2); // Frequency
    Serial.print(",");
    Serial.println(vPSDs[i], 4); // PSD
  }
}
