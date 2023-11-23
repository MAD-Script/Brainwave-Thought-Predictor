# import serial
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# # Configure the serial port - adjust the port name as needed
# ser = serial.Serial('COM5', 115200, timeout=1)

# # Initialize empty lists to store data
# frequency_data = []
# psd_data = []

# # Initialize variables for storing data
# current_frequency = None
# current_psd = None

# # Define frequency bands (you can adjust these as needed)
# delta_band = (0.5, 4)  # Delta waves (0.5-4 Hz)
# theta_band = (4, 8)    # Theta waves (4-8 Hz)
# alpha_band = (8, 12)   # Alpha waves (8-12 Hz)
# beta_band = (12, 30)   # Beta waves (12-30 Hz)
# gamma_band = (30, 100) # Gamma waves (30-100 Hz)

# # Function to update data lists
# def update_data():
#     if current_frequency is not None and current_psd is not None:
#         frequency_data.append(current_frequency)
#         psd_data.append(current_psd)

# # Read and process data from the serial port
# def read_serial_data():
#     while True:
#         line = ser.readline().decode().strip()  # Read a line from the serial port
#         if line.startswith("Freq: "):
#             parts = line.split(", PSD: ")
#             if len(parts) == 2:
#                 try:
#                     current_frequency = float(parts[0].split("Freq: ")[1])
#                     current_psd = float(parts[1])
#                     update_data()
#                 except ValueError:
#                     pass

# # Create a live plot using Matplotlib animation
# def animate(i):
#     plt.clf()
#     plt.plot(frequency_data, psd_data, label='PSD')
#     plt.axvspan(*delta_band, color='red', alpha=0.2, label='Delta')
#     plt.axvspan(*theta_band, color='orange', alpha=0.2, label='Theta')
#     plt.axvspan(*alpha_band, color='yellow', alpha=0.2, label='Alpha')
#     plt.axvspan(*beta_band, color='green', alpha=0.2, label='Beta')
#     plt.axvspan(*gamma_band, color='blue', alpha=0.2, label='Gamma')
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Power Spectral Density (PSD)')
#     plt.title('Brainwave Analysis')
#     plt.legend()
#     plt.grid(True)

# # Start reading and plotting data
# ani = FuncAnimation(plt.gcf(), animate, frames=range(0, len(frequency_data)), interval=1000)
# read_serial_data()  # This will continuously read data from the serial port

# # Display the plot
# plt.show()

# # Close the serial port when done
# ser.close()


# import serial
# import csv

# # Configure the serial port - adjust the port name as needed
# ser = serial.Serial('COM5', 115200, timeout=1)

# # Create a CSV file to save the data
# csv_filename = "brainwave_data.csv"
# csv_file = open(csv_filename, mode='w', newline='')
# csv_writer = csv.writer(csv_file)

# # Initialize lists to store data
# psd_values = []

# # Define the number of samples
# num_samples = 128

# # Read and process data from the serial port
# def read_serial_data():
#     frequencies_saved = False  # Flag to indicate if frequencies have been saved
#     while True:
#         line = ser.readline().decode().strip()  # Read a line from the serial port
#         values = line.split(",")
#         if len(values) == 2:
#             try:
#                 if not frequencies_saved:
#                     frequencies = [str(i * 1.0 * 1000 / num_samples) for i in range(num_samples)]
#                     csv_writer.writerow(["Frequency (Hz)"] + frequencies)  # Save frequencies at the top row
#                     frequencies_saved = True
#                 psd = float(values[1])
#                 psd_values.append(psd)
#                 save_to_csv()
#             except ValueError:
#                 pass

# # Save data to the CSV file
# def save_to_csv():
#     if len(psd_values) >= num_samples:
#         csv_writer.writerow(["PSD"] + psd_values)
#         csv_file.flush()  # Ensure data is written immediately
#         psd_values.clear()

# # Start reading and saving data
# try:
#     read_serial_data()
# except KeyboardInterrupt:
#     print("Data collection stopped by user.")

# # Close the serial port and CSV file when done
# ser.close()
# csv_file.close()






import serial
import csv

# Configure the serial port - adjust the port name as needed
ser = serial.Serial('COM5', 115200, timeout=1)

# Create a CSV file to save the data
csv_filename = "brainwave_data.csv"
csv_file = open(csv_filename, mode='w', newline='')
csv_writer = csv.writer(csv_file)

# Initialize a list to store frequencies
frequencies = []

# Define the number of samples
num_samples = 128

# Read and process data from the serial port
def read_serial_data():
    psd_values = [[] for _ in range(num_samples)]  # Initialize a list of empty lists for PSD values
    while True:
        line = ser.readline().decode().strip()  # Read a line from the serial port
        values = line.split(",")
        if len(values) == 2:
            try:
                frequency = float(values[0])
                psd = float(values[1])
                frequencies.append(frequency)
                for i in range(num_samples):
                    psd_values[i].append(psd)
                save_to_csv(frequencies, psd_values)
            except ValueError:
                pass

# Save data to the CSV file
def save_to_csv(frequencies, psd_values):
    if len(frequencies) >= num_samples:
        if not csv_writer:
            # Write the header row with frequencies
            csv_writer.writerow(['Frequency (Hz)'] + frequencies)
        # Write rows with PSD values for each frequency
        for i in range(num_samples):
            csv_writer.writerow(['PSD' + str(i + 1)] + psd_values[i])
        csv_file.flush()  # Ensure data is written immediately
        frequencies.clear()
        for i in range(num_samples):
            psd_values[i].clear()

# Start reading and saving data
try:
    read_serial_data()
except KeyboardInterrupt:
    print("Data collection stopped by user.")

# Close the serial port and CSV file when done
ser.close()
csv_file.close()
