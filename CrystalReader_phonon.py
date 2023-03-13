"""

CrystalReader version 'phonon'. Read and extract data from '.phonon' files.
Copyright (C) 2023  Pablo Gila-Herranz
Check the latest version at https://github.com/pablogila/CrystalReader
Feel free to contact me at pablo.gila.herranz@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

version = "vCRphonon.2023.03.13.1300"

print("")
print("  Running CrystalReader in 'phonon' mode, version " + version)
print("  If you find this code useful, a citation would be greatly appreciated :D")
print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")
print("  This is free software, and you are welcome to redistribute it under GNU General Public License")
print("")


import re
import os
import csv
import time


# This function will extract the numbers from the name of the parent folder
def naming(string):
    # Define a regular expression pattern to match the desired value
    pattern = r"pnam-p-1-(\d{3})-(\d{3})-(\d{3})-(\d{3})"
    # Use the re.search() function to find the first occurrence of the pattern in the string
    match = re.search(pattern, string)
    # Check if a match was found
    if match:
        # Extract the matched groups and join them with hyphens
        return "-".join(match.groups())
    else:
        # If no match was found, return None
        return None


# This function will extract the string value of a given variable from a raw string
def extract_column(string, column):
    columns = string.split()
    pattern = r'(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'
    if column < len(columns):
        match = re.match(pattern, columns[column])
        if match:
            return float(match.group(1))
    return None


# This function will search for a specific string value in a given file, and return the lines following the match
def searcher_rows(filename, search_value, number_rows):
    with open(filename, 'r') as file:
        # Move the file pointer to the end of the file
        file.seek(0, 2)
        # Get the position of the file pointer
        position = file.tell()
        lines = []
        while position >= 0 and len(lines) < number_rows+1:
            file.seek(position)
            next_char = file.read(1)
            if next_char == '\n':
                line = file.readline().strip()
                if line.startswith(search_value):
                    lines.append(line)
                    for i in range(number_rows):
                        next_line = file.readline().strip()
                        if next_line:
                            lines.append(next_line)
                    break
            position -= 1
    return lines[::1]


# This function will print a progress bar in the console, just for fun
def progressbar(current, total):
    bar_length = 50
    percentage = int((current/total)*100)
    progress = int((bar_length*current)/total)
    loadbar = "  [{:{len}}]{}%".format(progress*'■',percentage,len=bar_length)
    print(loadbar, end='\r')


# This function will print a progress bar in the console, as well as the ETA, just for fun
def progressbar_ETA(current, total, start):
    bar_length = 50
    percentage = int((current/total)*100)
    progress = int((bar_length*current)/total)
    loadbar = "  [{:{len}}]{:4.0f}%".format(progress*'■',percentage,len=bar_length)
    elapsed = time.time() - start
    eta = elapsed * (total/current - 1)
    if current > total/5 and eta >= 0:
        loadbar += "  |  ETA: {:5.0f}s".format(eta)
    else:
        loadbar += "  |  ETA: >{:4.0f}s  ".format(eta)
    print(loadbar, end='\r')


# Structure of the data
data_directory = 'data'
data_phonon = 'cc-2_Efield.phonon'
data_phonon_lines = 144
data_phonon_out = 'out_phonon.csv'
data_phonon_header = ['filename', 'E_1', 'E_2', 'E_3', 'E>0.05?', 'E_73', 'E_74', 'E_75', 'E_76', 'Zero_E_Gamma_Point=(E_4++144)/2 /cm^-1', 'Zero_E_Gamma_Point / eV']
# Threshold for the energy to be considered greater than zero
too_big = 0.05 

# Conversion factor from cm^-1 to eV
cm_ev = 1.0 / 8065.54429
print("  cm^-1 to eV conversion factor: ", cm_ev, "\n")

print("  Reading files...")

# Start a timer to measure the execution time. Just for fun.
time_start = time.time()

# Get the absolute path to the directory containing the Python script
dir_path = os.path.dirname(os.path.realpath(__file__))
# Specify the path to the directory containing the folders with the .castep files, relative to the script's directory
path = os.path.join(dir_path, data_directory)
# Get the names of all the directories in the given path, and store them in a list
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

# Open the output file to write the data
with open(data_phonon_out, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write a header row for the CSV file
    writer.writerow(data_phonon_header)

    # Start the counter for the progress bar
    loop = 0
    # Loop through all the folders in the /data path
    for directory in directories:
        # Progress bar, just for fun
        loop += 1
        progressbar_ETA(loop, len(directories), time_start)

        # Define the path to the .castep file
        file_phonon = os.path.join(path, directory, data_phonon)
        file_name = naming(directory)

        # Read the file and look for the desired line, return the corresponding lines after the match
        # The phonon_str[0] is the header, the phonon_str[1] is the first line of data, etc.
        phonon_str = searcher_rows(file_phonon, 'q-pt=', data_phonon_lines)

        #Ir_1 = extract_column(phonon_str[1], 2)
        #Ir_2 = extract_column(phonon_str[2], 2)
        #Ir_3 = extract_column(phonon_str[3], 2)
        E_1 = extract_column(phonon_str[1], 1)
        E_2 = extract_column(phonon_str[2], 1)
        E_3 = extract_column(phonon_str[3], 1)
        E_73 = extract_column(phonon_str[73], 1)
        E_74 = extract_column(phonon_str[74], 1)
        E_75 = extract_column(phonon_str[75], 1)
        E_76 = extract_column(phonon_str[76], 1)

        if (abs(E_1) > too_big) or (abs(E_2) > too_big) or (abs(E_3) > too_big):
            question = 'YES'
        else:
            question = '-'
        
        ZEGP = 0
        for k in range(4, data_phonon_lines + 1):
            ZEGP += extract_column(phonon_str[k], 1)
        ZEGP = ZEGP/2
        
        # write the data row to the file
        row = [file_name, E_1, E_2, E_3, question, E_73, E_74, E_75, E_76, ZEGP, ZEGP * cm_ev]
        writer.writerow(row)

time_elapsed = round(time.time() - time_start, 3)
print("")
print("  Finished reading the ", data_phonon, " files in ", time_elapsed, " seconds")
print("  Data extracted and saved to ", data_phonon_out)
print("")
