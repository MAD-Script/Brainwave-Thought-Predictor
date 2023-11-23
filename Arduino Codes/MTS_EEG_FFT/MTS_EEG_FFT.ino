/*
  MTS 
  July 26, 2020
  FFT sets up apprx 1Hz 
  Display is 320 x 480 TFT
  Display is PSD on logarthmic scale
  
  FFT copied from Arduino FFT_03

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
  Written by Limor Fried/Ladyada for Adafruit Industries.
  MIT license, all text above must be included in any redistribution
 ***************************************************

*/
#include <SPI.h>
#include "arduinoFFT.h"

#if defined __SAMD51__
   #define STMPE_CS 6
   #define SD_CS    5
#endif



arduinoFFT FFT = arduinoFFT(); /* Create FFT object */

#define CHANNEL A0
const uint16_t samples = 128; //This value MUST ALWAYS be a power of 2
const double samplingFrequency = 100; //Hz, must be less than 10000 due to ADC

unsigned int sampling_period_us;
unsigned long microseconds;

/*
These are the input and output vectors
Input vectors receive computed results from FFT
*/
double vReal[samples];
double vImag[samples];
double vPSDs[samples];

#define SCL_INDEX 0x00
#define SCL_TIME 0x01
#define SCL_FREQUENCY 0x02
#define SCL_PLOT 0x03
int MaxV = 100; //Maximum PSD value * 10

uint16_t yz;  // Uses to calculate yval on TFT
uint16_t Color; // Color for TFT

// Prototypes
void drawGraph();
void PrintVector(double , uint16_t , uint8_t );


void setup(){
  sampling_period_us = round(1000000*(1.0/samplingFrequency));
  Serial.begin(115200);
//  while(!Serial); // Comment out if battery powered

}

void loop(){
  /*SAMPLING*/
  microseconds = micros();
  for(int i=0; i<samples; i++){
//      vReal[i] = analogRead(CHANNEL);
      vReal[i] = analogRead(CHANNEL)-512.0;  //modified for zero balance
//      Serial.println(vReal[i]);
      vImag[i] = 0;
      while(micros() - microseconds < sampling_period_us){
        //empty loop
      }
      microseconds += sampling_period_us;
  }
// while (1);
  /* Print the results of the sampling according to time */
  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);	/* Weigh data */
  FFT.Compute(vReal, vImag, samples, FFT_FORWARD); /* Compute FFT */
  FFT.ComplexToMagnitude(vReal, vImag, samples); /* Compute magnitudes */
  PrintVector(vReal, (samples >> 1), SCL_FREQUENCY);
//  double x = FFT.MajorPeak(vReal, samples, samplingFrequency);
//  Serial.println(x, 6); //Print out what frequency is the most dominant.

//
//  for (int i = 0; i<(samples >> 1); i++){
//    Serial.println(vPSDs[i],2);
//
//  }
  //while(1); /* Run Once */
   delay(1000); /* Repeat after delay */
}


void PrintVector(double *vData, uint16_t bufferSize, uint8_t scaleType)
{
  for (uint16_t i = 0; i < bufferSize; i++){
    double abscissa;
    abscissa = ((i * 1.0 * samplingFrequency) / samples);
    Serial.print(abscissa, 6);
    Serial.print(",");
    Serial.println(vData[i], 4);
    vPSDs[i] = log10(vData[i]*vData[i]/0.78125);  //save PSD values
  }
  Serial.println();
}
