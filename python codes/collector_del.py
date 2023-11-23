import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import time
import csv
import serial
import os
import pandas as pd
import threading

class DataCollectorApp:
    def __init__(self):
        # Initialize the application
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        self.window = ctk.CTk()
        self.init_ui()

    def init_ui(self):
        # Initialize the user interface
        self.configure_window()
        self.create_widgets()
        self.username = self.get_username()  # Ask for the username
        self.load_words()  # Load words from CSV
        self.start_program()

    def configure_window(self):
        # Configure window settings
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        win_geo_x = screen_width * 0.9
        win_geo_y = screen_height * 0.9

        window_x = int(screen_width / 2 - win_geo_x / 2)
        window_y = int(screen_height / 2 - win_geo_y / 2)

        self.window.geometry(f"{int(win_geo_x)}x{int(win_geo_y)}+{window_x}+{window_y}")
        self.window.title("Data Collector")
        self.window.minsize(int(win_geo_x / 3), int(win_geo_y / 3))
        self.window.overrideredirect(True)
        self.window.bind("<Escape>", lambda event: self.window.quit())

    def create_widgets(self):
        # Create UI elements
        self.title = ctk.CTkLabel(
            self.window, text="", font=("Arial", 250), anchor="center"
        )
        self.title.pack(expand=True, fill="both")

        self.progress_frame = ttk.Frame(self.window)
        self.progress_frame.pack(fill="both")

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=60,
            length=self.window.winfo_width(),
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew")

        self.blank = ttk.Frame(self.progress_frame)
        self.blank.grid(row=0, column=0, sticky="nsew")

    def get_username(self):
        username = ctk.CTkInputDialog(text="Enter your name", title="User Name").get_input()
        if not username:
            self.window.quit()
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
        self.title.configure(font=("Arial", 250))
        for i in range(1, 4):
            self.title.configure(text=i)
            self.title.update_idletasks()
            time.sleep(1)
        self.show_next_word()

    def show_next_word(self):
        if self.word_list:
            word = self.word_list.pop(0)
            self.show_word(word)
        else:
            self.title.configure(text="No more words.")
            self.window.after(2000, self.exit_screen)

    def show_word(self, word):
        self.progress_bar.tkraise()
        self.progress_bar["value"] = 0
        self.title.configure(text=word)
        self.title.configure(font=("Arial", 100))
        self.title.pack(expand=True, fill="both")
        threading.Thread(target=self.record_data, args=(word,)).start()  # Start recording data in a separate thread
        self.progress_step()

    def record_data(self, word):
        directory = f"data/{self.username}/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, f"{word}.csv")
        frequencies = []

        with serial.Serial('COM5', 115200) as ser:  # Replace 'COMX' with your Arduino's serial port
            prev_time = time.time()
            flag = False
            while True:
                data = ser.readline().decode().strip()
                if not data:
                    continue

                # Split data into frequency and value
                freq, value = map(float, data.split(','))
                if not flag:
                    frequencies.append(freq)
                    flag = True
                frequencies.append(value)
                
                # Check if 60 seconds have passed
                if time.time() - prev_time >= 6:
                    # Write frequencies to a CSV file
                    with open(file_path, mode='w', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(frequencies)
                    frequencies = []
                    prev_time = time.time()

                # Check if the user wants to exit
                response = input("Next word (y/N): ")
                if response.lower() != 'y':
                    break

    def progress_step(self):
        self.progress_bar.tkraise()
        if self.progress_bar["value"] < 59:
            self.progress_bar.step()
            self.window.after(100, self.progress_step)
        else:
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
        self.title.configure(text="Thank you! Closing in 3 seconds ")
        self.title.configure(font=("Arial", 100))
        self.window.after(3000, self.window.quit)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DataCollectorApp()
    app.run()
