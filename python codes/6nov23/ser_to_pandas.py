import serial
import io
import pandas as pd
import time


def open_serial_port(com_port, baud_rate):
    try:
        ser = serial.Serial(com_port, baud_rate)
        time.sleep(3)  # Wait for some time (adjust as needed)
        return ser
    except serial.SerialException as e:
        print(f"Failed to open the serial port: {e}")
        return None

def read_data_from_serial(ser):
    try:
        serial_data = ser.read_all().decode('utf-8').strip().replace('\r\n', '\n')
        time.sleep(1)
        if not serial_data:
            time.sleep(2.5)
        return serial_data
    except serial.SerialException as e:
        print(f"Error reading data from the serial port: {e}")
        return None

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
    ser = open_serial_port(com_port = 'COM5', baud_rate = 115200)
    if ser is None:
        return

    df = pd.DataFrame()

    try:
        while True:
            serial_data = read_data_from_serial(ser)
            if serial_data:
                df = process_serial_data(serial_data, df)
                print("\nUpdated DataFrame:")
                print(df)
                time.sleep(2)
    except KeyboardInterrupt:
        print("\nData collection stopped.")
        ser.close()
        save_dataframe_to_csv(df, 'output.csv')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
