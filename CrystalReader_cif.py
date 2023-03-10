"""

CrystalReader version 'cif'. Read and extract data from '.cif' files.
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

version = "vCRcif.2023.03.10.1900"

print("")
print("  Running CrystalReader in 'cif' mode, version " + version)
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
def extract_str(string, name):
    pattern = re.compile(name + r"\s*(=)?\s*['\"](.*?)(?=['\"]|$)")
    match = pattern.search(string)
    if match:
        return match.group(2).strip()
    else:
        return None


# This function will search for a specific string value in a given file, and return the corresponding line
def searcher(filename, search_value):
    with open(filename, 'r') as file:
        # Move the file pointer to the end of the file
        file.seek(0, 2)
        # Get the position of the file pointer
        position = file.tell()
        while position >= 0:
            file.seek(position)
            next_char = file.read(1)
            if next_char == '\n':
                line = file.readline().strip()
                if line.startswith(search_value):
                    return line
            position -= 1
    return None


# This function will print a progress bar in the console, just for fun
def progressbar(current, total):
    bar_length = 50
    percentage = int((current/total)*100)
    progress = int((bar_length*current)/total)
    loadbar = "  [{:{len}}]{}%".format(progress*'■',percentage,len=bar_length)
    print(loadbar, end='\r')


# Structure of the data
data_directory = 'data'
data_cif = 'cc-2-out.cif'
data_cifE = 'cc-2_Efield-out.cif'
data_cif_out = 'out_cif.csv'
data_cif_header = ['filename', 'SSG_H_M', 'SSG_H_M-Efield']

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
with open(data_cif_out, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write a header row for the CSV file
    writer.writerow(data_cif_header)

    # Start the counter for the progress bar
    i = 0
    # Loop through all the folders in the /data path
    for directory in directories:
        # Progress bar, just for fun
        i+=1
        progressbar(i, len(directories))

        # Define the path to the .castep file
        file_cif = os.path.join(path, directory, data_cif)
        file_cifE = os.path.join(path, directory, data_cifE)
        file_name = naming(directory)

        # Read the file and look for the desired lines
        cif_str = searcher(file_cif, '_symmetry_space_group_name_H_M')
        cifE_str = searcher(file_cifE, '_symmetry_space_group_name_H_M')

        # Extract the values from the strings
        cif = extract_str(cif_str, '_symmetry_space_group_name_H_M')
        cifE = extract_str(cifE_str, '_symmetry_space_group_name_H_M')

        # write the data row to the file
        row = [file_name, cif, cifE]
        writer.writerow(row)

        # Print the data on screen, for debugging purposes
        #print(file_name)
        #print("cif = ", cif)
        #print("cifE = ", cifE)
        #print("")

time_elapsed = round(time.time() - time_start, 3)
print("  Finished reading the ", data_cif, " and ", data_cifE, " files in ", time_elapsed, " seconds")
print("  Data extracted and saved to ", data_cif_out)
print("")
