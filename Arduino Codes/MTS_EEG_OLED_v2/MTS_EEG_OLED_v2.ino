// #include <arduinoFFT.h>

// #define CHANNEL A0 // Output of the AD8232
// const uint16_t samples = 128; // This value MUST ALWAYS be a power of 2
// const double samplingFrequency = 100; // Hz, must be less than 10000 due to ADC

// unsigned int sampling_period_us;
// unsigned long microseconds;

// double vReal[samples];
// double vImag[samples];
// double vPSDs[samples];

// arduinoFFT FFT = arduinoFFT(); /* Create FFT object */

// void setup() {
//   sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
//   Serial.begin(115200);
// }

// void loop() {
//   /*SAMPLING*/
//   microseconds = micros();
//   for (int i = 0; i < samples; i++) {
//     vReal[i] = analogRead(CHANNEL) - 512.0;  // Modified for zero balance
//     vImag[i] = 0;
//     while (micros() - microseconds < sampling_period_us) {
//       // Empty loop
//     }
//     microseconds += sampling_period_us;
//   }

//   FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
//   FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
//   FFT.ComplexToMagnitude(vReal, vImag, samples);
//   PrintVector(vReal, (samples >> 1));

//   delay(1000); // Delay before sending the next data point
// }

// void PrintVector(double *vData, uint16_t bufferSize) {
//   for (uint16_t i = 0; i < bufferSize; i++) {
//     vPSDs[i] = log10(vData[i] * vData[i] / 0.78125); // Save PSD values
//     char formattedFrequency[10];
//     sprintf(formattedFrequency, "%.4f", (i * 1.0 * samplingFrequency) / samples); // Format the frequency
//     Serial.print(formattedFrequency); // Frequency
//     Serial.print(",");
//     Serial.println(vPSDs[i], 4); // PSD
//   }
// }


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
    double freq = (i * 1.0 * samplingFrequency) / samples;
    if(freq < 10){
      Serial.print(0);
    }
    Serial.print(freq); // Frequency
    Serial.print(",");
    Serial.println(vPSDs[i], 4); // PSD
  }
}
