#include <arduinoFFT.h>

#define CHANNEL A0 // Output of the AD8232
const uint16_t samples = 128; // This value MUST ALWAYS be a power of 2
const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC

unsigned int sampling_period_us;
unsigned long microseconds;

bool shouldRead = false;

double vReal[samples];
double vImag[samples];
double vPSDs[samples];

arduinoFFT FFT = arduinoFFT(); /* Create FFT object */

void setup() {
  initialize();
}

void loop() {
  checkForCommand(); // Check for incoming commands from Python
  if (shouldRead) {
    sampleData();
    performFFT();
    printData();
//    delay(500); // Delay before sending the next data point
    shouldRead = false;
  }
}

void initialize() {
  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
  Serial.begin(115200);
  delay(500); // Add a delay to ensure Python code is ready to receive data
  Serial.println("Arduino is ready");
}

void sampleData() {
  microseconds = micros();
  for (int i = 0; i < samples; i++) {
    vReal[i] = analogRead(CHANNEL) - 512.0;  // Modified for zero balance
    vImag[i] = 0;
    while (micros() - microseconds < sampling_period_us) {
      // Empty loop
    }
    microseconds += sampling_period_us;
  }
}

void performFFT() {
  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, samples);
}

void printData() {
  for (uint16_t i = 0; i < (samples >> 1); i++) {
    vPSDs[i] = log10(vReal[i] * vReal[i] / 0.78125); // Save PSD values
    Serial.print((i * 1.0 * samplingFrequency) / samples, 2); // Frequency
    Serial.print(",");
    Serial.println(vPSDs[i], 4); // PSD
  }
  // Signal Python that data is ready
  Serial.println("DataReady");
}

void checkForCommand() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "read") {
//      Serial.println("ok");
      shouldRead = true;
    }
  }
}
