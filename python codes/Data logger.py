import tkinter as tk
import csv
import serial
import time
import os
import pandas as pd

# Function to check if a file exists
def file_exists(username, word):
    file_path = f"{username}/{word}.csv"
    return os.path.exists(file_path)

# Function to create and save the CSV file
def create_and_save_csv(username, word, frequencies, values):
    file_path = f"{username}/{word}.csv"
    # Create a DataFrame with frequencies as the header and values as data
    df = pd.DataFrame({'Frequencies': frequencies, 'Values': values})
    df.to_csv(file_path, index=False)

# Function to display words in a GUI window
def display_word(word):
    window = tk.Tk()
    window.geometry("400x200")
    label = tk.Label(window, text=word, font=("Helvetica", 36))
    label.pack()

    def next_word():
        window.destroy()

    button = tk.Button(window, text="Next Word (y)", command=next_word)
    button.pack()

    window.mainloop()

# Function to read and process Arduino data
def read_and_process_data(username, word):
    file_path = f"{username}/{word}.csv"
    frequencies = []

    with serial.Serial('COM5', 9600) as ser:  # Replace 'COMX' with your Arduino's serial port
        start_time = time.time()
    
        while True:
            data = ser.readline().decode().strip()
            if not data:
                continue

            # Split data into frequency and value
            freq, value = map(float, data.split(','))
            # frequencies.append(freq)
            if not flag:
                frequencies.append(freq)
                print(freq)
                flag = True
            frequencies.append(value)
            
            # Display the word if 60 seconds have passed
            if time.time() - start_time >= 60:
                display_word(word)
                frequencies = []
                start_time = time.time()

            # Check if the user wants to exit
            response = input("Next word (y/N): ")
            if response.lower() != 'y':
                break

    # Write frequencies to a CSV file
    with open(file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(frequencies)

# Main function
def main():
    username = input("Enter your username: ")  # Get username from user
    words_df = pd.read_csv("words.csv")
    words = words_df["Word"].tolist()  # Read words from 'words.csv'

    for word in words:
        if not file_exists(username, word):
            
            display_word(word)
            read_and_process_data(username, word)

if __name__ == "__main__":
    main()
