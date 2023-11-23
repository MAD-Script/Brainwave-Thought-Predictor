import csv

# Specify the path to the input and output CSV files
input_csv_file = "english-word-list-total.csv"
output_csv_file = "sorted-english-words.csv"

try:
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        
        # Create a dictionary to hold words by their length
        word_dict = {}
        
        # Iterate through each row in the CSV
        for row in csv_reader:
            if len(row) >= 2:
                word = row[1].strip()
                length = len(word)
                
                # Check if the length is already in the dictionary
                if length in word_dict:
                    word_dict[length].append(word)
                else:
                    word_dict[length] = [word]
        
        # Sort the words by their length and write them to the output CSV
        with open(output_csv_file, mode='w', encoding='utf-8', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            
            for length, words in sorted(word_dict.items()):
                words.sort()  # Sort the words within each length category
                csv_writer.writerow([length] + words)
        
        print(f"Words sorted and saved to {output_csv_file}.")
        
except FileNotFoundError:
    print(f"The file '{input_csv_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
