import io
import os
import csv
import time
import serial
import pandas as pd
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk


class DataCollectorApp:
    serial_port = None
    df = None
    file_path = None
    data_rows = 64
    # 2.68 seconds to collect each row of data
    # collecting 64 data per word, in an hour
    pbar_length = 10
    
    start_time = time.time()
    
    def __init__(self):
        # Initialize the application
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        self.window = ctk.CTk()
        self.init_ui()

    def init_ui(self):
        self.serial_port = self.open_serial_port("COM5", 115200)

        self.username = self.get_username()  # Ask for the username
        time.sleep(.5)
        if self.username != None:
            self.configure_window()
            self.create_widgets()

            self.directory = f"data/{self.username}/"
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)

            self.load_words()  # Load words from CSV
            # self.serial_port = self.open_serial_port('COM5', 115200)
            self.wait_for_arduino(self.serial_port)
            self.start_program()

    def configure_window(self):
        # Configure window settings
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        ratio = 0.9
        win_geo_x = screen_width * ratio
        win_geo_y = screen_height * ratio
        self.pbar_length = int(win_geo_x)
        
    
        window_x = int(screen_width / 2 - win_geo_x / 2)
        window_y = int(screen_height / 2 - win_geo_y / 2)

        self.window.geometry(f"{int(win_geo_x)}x{int(win_geo_y)}+{window_x}+{window_y}")
        self.window.title("Data Collector")
        self.window.minsize(int(win_geo_x / 3), int(win_geo_y / 3))
        self.window.bind("<Escape>", lambda event: self.exit_screen())

    def create_widgets(self):
        # Create UI elements
        self.title = ctk.CTkLabel(
            self.window, text="", font=("Arial", 250), anchor="center"
        )
        self.title.pack(expand=True, fill="both")

        self.progress_frame = ttk.Frame(self.window)
        self.window.tk_setPalette(background="blue")
        self.progress_frame.pack(fill="both")

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=self.data_rows+1,
            length=self.pbar_length,
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew")

        self.blank = ttk.Frame(self.progress_frame)
        self.blank.grid(row=0, column=0, sticky="nsew")

    def get_username(self):
        username = ctk.CTkInputDialog(
            text="Enter your name", title="User Name"
        ).get_input()
        if not username:
            self.window.quit()
            return None
        return username

    def load_words(self):
        # Load words from a CSV file
        self.word_list = []
        with open("words.csv", "r") as csv_file:
            word_list = csv.reader(csv_file)
            for row in word_list:
                self.word_list.extend(row)

    def start_program(self):
        self.title.configure(text="Ready to start? ")
        self.title.configure(font=("Arial", 100))
        self.window.bind(
            "<Key>",
            lambda event: self.wait_screen()
            if event.char == "y"
            else self.exit_screen(),
        )

    def wait_screen(self):
        self.title.configure(font=("Arial", 450))
        for i in range(1, 4):
            self.title.configure(text=i)
            self.title.update_idletasks()
            time.sleep(1)
        self.show_next_word()

    def show_next_word(self):
        if self.word_list:
            word = self.word_list.pop(0)
            self.show_word(word)

            self.file_path = os.path.join(self.directory, f"{word}.csv")
            self.df = pd.DataFrame()

            print(f"\nCollecting data for '{word}'...")
            time.sleep(1)
            
            self.start_time = time.time()
            self.progress_step()
        else:
            self.title.configure(text="No more words.")
            self.window.after(1500, self.exit_screen)

    def show_word(self, word):
        print(f"Now Viewing word '{word}'")
        self.progress_bar.tkraise()
        self.progress_bar["value"] = 0
        self.title.configure(text=word)
        self.title.configure(font=("Arial", 350))
        self.title.pack(expand=True, fill="both")
        self.title.update_idletasks()

    def progress_step(self):
        self.progress_bar.tkraise()
        # time.sleep(1)
        if self.progress_bar["value"] < self.data_rows:
            self.serial_data = self.read_data_from_serial(self.serial_port)

            if self.serial_data:
                self.df = self.process_serial_data(self.serial_data, self.df)
                print("\nUpdated DataFrame:")
                print(self.df)

            self.progress_bar.step()
            self.window.after(200, self.progress_step)
        else:
            print("\nData collection stopped.")
            end=time.time()
            print(f"Started at {self.start_time} \nended at {end}\nTime Taken: {end-self.start_time}")
            self.serial_port
            self.save_dataframe_to_csv(self.df, self.file_path)
            self.df = None
            # self.serial_port.close()
            self.progress_bar.stop()
            self.next_screen()

    def next_screen(self):
        self.progress_bar["value"] = 60
        self.progress_bar.lower()
        self.title.configure(text="Ready for next word? ")
        self.title.configure(font=("Arial", 100))
        self.window.bind(
            "<Key>",
            lambda event: self.wait_screen()
            if event.char == "y"
            else self.exit_screen(),
        )

    def exit_screen(self):
        self.progress_bar["value"] = 60
        self.progress_bar.lower()
        self.title.configure(font=("Arial", 100))
        for i in range(1, 4):
            self.title.configure(text=f"Thank you! Closing in {4-i} seconds ")
            self.title.update_idletasks()
            time.sleep(1)
        self.window.after(200, self.window.quit)

    def open_serial_port(self, com_port, baud_rate):
        try:
            ser = serial.Serial(com_port, baud_rate)
            print("Serial Port Opened Successfully")
            # time.sleep(3)  # Wait for some time (adjust as needed)
            return ser
        except serial.SerialException as e:
            print(f"Failed to open the serial port: {e}")
            return None

    def wait_for_arduino(self, ser):
        print("Waiting for Arduino to be ready...")
        while True:
            line = ser.readline().decode("utf-8").strip()
            if line == "Arduino is ready":
                print("Arduino is Ready to Start")
                break
            time.sleep(1)

    def send_command(self, ser, command):
        ser.write(command.encode("utf-8"))

    def read_data_from_serial(self, ser):
        try:
            print("Reading data from the Arduino...\n")
            self.send_command(ser, "read")
            data = ""

            data_ready = False

            while not data_ready:
                line = ser.readline().decode("utf-8").strip()
                # concatenate the data until we receive "DataReady"
                if line == "DataReady":
                    data_ready = True
                else:
                    data += line + "\n"
            return data
        except serial.SerialException as e:
            print(f"Error reading data from the serial port: {e}")
            return None

    def process_serial_data(self, serial_data, df):
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

    def save_dataframe_to_csv(self, df, filename):
        try:
            df.to_csv(filename, index=False)
        except Exception as e:
            print(f"Error saving DataFrame to CSV: {e}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = DataCollectorApp()
    app.run()
