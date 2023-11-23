import os
import serial
import time

def initialize_serial(com_port, baud_rate=115200, timeout=1):
    return serial.Serial(com_port, baud_rate, timeout=timeout)

def send_command(ser, command):
    ser.write(command.encode('utf-8'))

def read_data_from_serial(ser):
    try:
        print("Reading data from the Arduino...\n")
        send_command(ser, 'read')
        time.sleep(1.4)
        data = ""
        
        data_ready = False

        while not data_ready:
            line = ser.readline().decode('utf-8').strip()
            # concatenate the data until we receive "DataReady"
            if line == "DataReady":
                data_ready = True
            else:
                data += line
        return data
    except serial.SerialException as e:
        print(f"Error reading data from the serial port: {e}")
        return None

def wait_for_arduino(ser):
    print("Waiting for Arduino to be ready...")
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "Arduino is ready":
            break
        time.sleep(1)

def main():
    ser = initialize_serial('COM5')
    try:
        wait_for_arduino(ser)
        while True:
            ard_data = read_data_from_serial(ser)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()

if __name__ == "__main__":
    main()