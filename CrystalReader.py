"""

CrystalReader Common Functions. Read and extract data from different simulation files.
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

version = "vCRcif.2023.03.14.1200"

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



#####################################################
""" COMMON FUNCTIONS TO ALL CRYSTALREADER SCRIPTS """
#####################################################


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


# This function will extract the float value of a given variable from a raw string
def extract_float(string, name):
    pattern = re.compile(name + r'\s*=?\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None
    

# This function will extract the string value of a given variable from a raw string
def extract_str(string, name):
    pattern = re.compile(name + r"\s*(=)?\s*['\"](.*?)(?=['\"]|$)")
    match = pattern.search(string)
    if match:
        return match.group(2).strip()
    else:
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


# This function will search for a specific string value in a given file, and return the following lines after the match
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
        loadbar += "  |  ETA: {:5.0f}s  ".format(eta)
    else:
        loadbar += "  |  ETA: >{:4.0f}s  ".format(eta)
    print(loadbar, end='\r')


# This program asks the user which python script to use, and then runs it
# The possible options are: CrystalReader_cif.py, CrystalReader_castep.py, CrystalReader_phonon.py
print("")
print("  Which crystal structure would you like to read?")
print("  1. cif")
print("  2. castep")
print("  3. phonon")
print("")
choice = input("  Enter the number of your choice: ")
if choice == "1":
    import CrystalReader_cif
elif choice == "2":
    import CrystalReader_castep
elif choice == "3":
    import CrystalReader_phonon
else:
    print("")
    print("  Invalid input. Please try again.")


