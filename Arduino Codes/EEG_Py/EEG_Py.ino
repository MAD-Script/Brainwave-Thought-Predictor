#include <Wire.h>
#include "arduinoFFT.h"

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
bool shouldRead = false;

void setup() {
  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
  Serial.begin(115200);
  delay(500);  // Add a delay to ensure Python code is ready to receive data
  Serial.println("Arduino is ready");
}

void loop() {
  checkForCommand(); // Check for incoming commands from Python

  if (shouldRead) {
    analogReadToSamples(AD8232_PIN, samples, vReal, vImag, sampling_period_us);
    FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
    FFT.ComplexToMagnitude(vReal, vImag, samples);
    sendSerialData(vReal, samples >> 1);

    // Signal Python that data is ready
    Serial.println("DataReady");

    shouldRead = false;
  }
}

void analogReadToSamples(int pin, int numSamples, double* real, double* imag, unsigned long period) {
  unsigned long startMicros = micros();
  for (int i = 0; i < numSamples; i++) {
    real[i] = analogRead(pin);
    imag[i] = 0;
    while (micros() - startMicros < period) {
      // Wait for the sampling period
    }
    startMicros += period;
  }
}

void sendSerialData(double* vData, uint16_t bufferSize) {
  for (uint16_t i = 0; i < bufferSize; i++) {
    double abscissa = (i * 1.0 * samplingFrequency) / samples;
    Serial.print(abscissa, 5);
    Serial.print(",");
    Serial.println(vData[i], 4);
    vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
  }
  Serial.println();
}

void checkForCommand() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "read") {
      shouldRead = true;
    }
  }
}
