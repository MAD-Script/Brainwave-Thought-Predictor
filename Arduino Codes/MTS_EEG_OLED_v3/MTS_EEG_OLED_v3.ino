#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "arduinoFFT.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

const int AD8232_PIN = A0; // Analog pin connected to AD8232 OUT pin
const int samples = 128;
const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC

unsigned long sampling_period_us;
unsigned long microseconds;

double vReal[samples];
double vImag[samples];
double vPSDs[samples];

arduinoFFT FFT = arduinoFFT(); /* Create FFT object */

int MaxV = 100;

void setup()
{
  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
  Serial.begin(115200);
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);

  display.display();
  delay(2000);
  display.clearDisplay();

  // Display Text
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  // Display static text

  display.println("A Simple");
  display.println("Brain-Computer");

  display.println("Interface(BCI) to");
  display.println("Translate Brainwaves");
  display.println("to Text");

 
  display.display();
  delay(5000);


}

void loop()
{
  microseconds = micros();
  for (int i = 0; i < samples; i++)
  {
    vReal[i] = analogRead(AD8232_PIN);
    vImag[i] = 0;
    while (micros() - microseconds < sampling_period_us)
    {
      // Wait for the sampling period
    }
    microseconds += sampling_period_us;
  }

  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, samples);
  PrintVector(vReal, (samples >> 1));
  delay(1000);
}


void PrintVector(double *vData, uint16_t bufferSize)
{
  for (uint16_t i = 0; i < bufferSize; i++)
  {
    double abscissa;
    abscissa = ((i * 1.0 * samplingFrequency) / samples);
    Serial.print(abscissa, 6);
    Serial.print(",");
    Serial.println(vData[i], 4);
    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
  }
  Serial.println();
}
