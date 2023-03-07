print("")
print("CastepReader v2023.03.07.1600")
print("From CrystalReader by Pablo Gila-Herranz")
print("https://github.com/pablogila/CrystalReader")
print("Released under GNU General Public License v3.0")
print("If you find this code useful, a citation would be appreciated :D")
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


# This function will extract the value of a given variable from a raw string
def extract(string, name):
    pattern = re.compile(name + r'\s*=\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None


# This function will search for a specific string value in a given file, and return the corresponding line
def searcher(filename, search_value):
    with open(filename, 'r') as file:
        file.seek(0, 2)  # move the file pointer to the end of the file
        position = file.tell()  # get the position of the file pointer
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
    bar_length = 30
    percentage = int((current/total)*100)
    progress = int((bar_length*current)/total)
    loadbar = "[{:{len}}]{}%".format(progress*'■',percentage,len=bar_length)
    print(loadbar, end='\r')


# Start a timer to measure the execution time. Just for fun.
time_start = time.time()
# Start the counter for the progress bar
i = 0
# Define the conversion factor from eV to kJ/mol
ev = 1.602176634E-19 / 1000 # THIS NEEDS TO BE FIXED ----------------------------------------------
# Directory containing the folders with the .castep files
data_directory = 'data'

print("Reading files...")

# Get the absolute path to the directory containing the Python script
dir_path = os.path.dirname(os.path.realpath(__file__))
# Specify the path to the directory containing the folders with the .castep files, relative to the script's directory
path = os.path.join(dir_path, data_directory)
# Get the names of all the directories in the given path, and store them in a list
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

# Open the output file to write the data
with open('out_castep.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write a header row for the CSV file
    writer.writerow(['filename', 'enthalpy / eV', 'enthalpy / kJ/mol', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'cell volume / A^3', 'density / amu/A^3', 'density / g/cm^3'])

    # Loop through all the folders in the /data path
    for directory in directories:

        # Progress bar, just for fun
        i+=1
        progressbar(i, len(directories))

        # Define the path to the .castep file
        file = os.path.join(path, directory, 'cc-2.castep')
        file_name = naming(directory)

        # Read the file and look for the desired lines
        enthalpy_str = searcher(file, 'LBFGS: Final Enthalpy     =')
        volume_str = searcher(file, 'Current cell volume =')
        density_str = searcher(file, 'density =')
        densityg_str = searcher(file, '=')
        a_str = searcher(file, 'a =')
        b_str = searcher(file, 'b =')
        c_str = searcher(file, 'c =')

        # Extract the values from the strings
        enthalpy = extract(enthalpy_str, 'LBFGS: Final Enthalpy')
        volume = extract(volume_str, 'Current cell volume')
        density = extract(density_str, 'density')
        densityg = extract(densityg_str, '')
        a = extract(a_str, 'a')
        b = extract(b_str, 'b')
        c = extract(c_str, 'c')
        alpha = extract(a_str, 'alpha')
        beta = extract(b_str, 'beta')
        gamma = extract(c_str, 'gamma')

        # write the data row to the file
        row = [file_name, enthalpy, enthalpy*ev, a, b, c, alpha, beta, gamma, volume, density, densityg]
        writer.writerow(row)

        # Print the data on screen, for debugging purposes
        #print(file_name)
        #print("enthalpy = ", enthalpy)
        #print("enthalpy*ev = ", enthalpy*ev)
        #print("a = ", a)
        #print("b = ", b)
        #print("c = ", c)
        #print("alpha = ", alpha)
        #print("beta = ", beta)
        #print("gamma = ", gamma)
        #print("volume = ", volume)
        #print("density = ", density)
        #print("densityg = ", densityg)
        #print("")


time_elapsed = (time.time() - time_start)
print("")
print("Finished reading the '.castep' files in ", time_elapsed, " seconds")
print("Data extracted and saved to 'out_castep.csv'")
print("")
