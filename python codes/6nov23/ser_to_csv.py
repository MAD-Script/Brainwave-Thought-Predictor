import serial
import csv

# Define the COM port and baud rate
com_port = 'COM5'
baud_rate = 115200

# Open the serial port
ser = serial.Serial(com_port, baud_rate)

# Create a CSV file
csv_filename = 'data.csv'

def write_to_csv(data):
    with open(csv_filename, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)

try:
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        first_run = True

        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data = line.split(',')
                if first_run:
                    header = data[0]
                    csv_writer.writerow([header])
                    first_run = False
                csv_data = data[1]
                write_to_csv([csv_data])

except KeyboardInterrupt:
    print("Data collection stopped.")
    ser.close()
except Exception as e:
    print(f"An error occurred: {e}")

