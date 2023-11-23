import tkinter as tk
import csv
import serial
import os

# Function to check if a file exists
def file_exists(username, word):
    file_path = f"{username}/{word}.csv"
    return os.path.exists(file_path)

# Function to display words in a GUI window
def display_word(word):
    window = tk.Tk()
    window.geometry("400x200")
    label = tk.Label(window, text=word, font=("Helvetica", 36))
    label.pack()

    def next_word():
        window.destroy()

    # destroy() is called after 60 seconds
    window.after(60000, next_word())
    

# Function to read and process Arduino data
def read_arduino_data(username, word):
    file_path = f"{username}/{word}.csv"
    frequencies = []

    with serial.Serial('COM5', 9600) as ser:  # Replace 'COMX' with your Arduino's serial port
        while True:
            data = ser.readline().decode().strip()
            if not data:
                continue

            # Split data into frequency and value
            freq, value = map(float, data.split(','))
            frequencies.append(freq)

            # Display the word if 60 seconds have passed
            if sum(frequencies) >= 60:
                display_word(word)
                frequencies = []

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
    username = "Adrian Dip Mohanta"  # Replace with your username
    words = ["I", "a", "am", "an", "as", "at", "be", "by"]  # Add more words if needed

    for word in words:
        if file_exists(username, word):
            continue

        display_word(word)
        read_arduino_data(username, word)

if __name__ == "__main__":
    main()
