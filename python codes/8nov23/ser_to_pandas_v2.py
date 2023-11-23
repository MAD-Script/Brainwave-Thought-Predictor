import serial
import io
import pandas as pd
import time

def initialize_serial(com_port, baud_rate=115200, timeout=1):
    return serial.Serial(com_port, baud_rate, timeout=timeout)

def send_command(ser, command):
    ser.write(command.encode('utf-8'))

def read_data_from_serial(ser):
    try:
        print("Reading data from the Arduino...\n")
        send_command(ser, 'read')
        data = ""
        
        data_ready = False

        while not data_ready:
            line = ser.readline().decode('utf-8').strip()
            # concatenate the data until we receive "DataReady"
            if line == "DataReady":
                data_ready = True
            else:
                data += line + "\n"
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

def process_serial_data(serial_data, df):
    try:
        temp_df = pd.read_csv(io.StringIO(serial_data), header=None)
        temp_df = temp_df.T
        temp_df.columns = temp_df.iloc[0]
        temp_df = temp_df[1:]
        temp_df = temp_df.reset_index(drop=True)
        # Add a unique index to temp_df
        temp_df.index = range(len(df), len(df) + len(temp_df))
        df = pd.concat([df, temp_df], ignore_index=True)
        return df
    except pd.errors.EmptyDataError:
        print("No data to process.")
        return df
    except pd.errors.ParserError as e:
        print(f"Error processing data: {e}")
        return df
    
def save_dataframe_to_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        print(f"Error saving DataFrame to CSV: {e}")

def main():
    ser = initialize_serial(com_port = 'COM5', baud_rate = 115200)
    if ser is None:
        return

    wait_for_arduino(ser)

    df = pd.DataFrame()

    try:
        while True:
            serial_data = read_data_from_serial(ser)
            if serial_data:
                df = process_serial_data(serial_data, df)
                print("\nUpdated DataFrame:")
                print(df)
    except KeyboardInterrupt:
        print("\nData collection stopped.")
        ser.close()
        save_dataframe_to_csv(df, 'output.csv')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()