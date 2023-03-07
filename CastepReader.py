""""

This program will read specific data from several .castep files.
There is a folder called /data, and inside that folder, there are many nested folders, each containing a file named 'cc-2.castep'.
The nested folders have names like '---pnam-p-1-000-000-270-000---350', and this program extracts the numbers 'xxx-xxx-xxx-xxx' and uses them as reference for the extracted data.
This program will read the data from the cc-2.castep file in each folder, and output a 'castep.out.csv' file with the data I want, in the root folder.
I want to write the following columns of data in the .csv file, in this order:
- name of the parent folder
- enthalpy of the final iteration, in eV
- enthalpy of the final iteration, in J
- cell parameter a, in Angstroms
- cell parameter b, in Angstroms
- cell parameter c, in Angstroms
- cell parameter alpha, in degrees
- cell parameter beta, in degrees
- cell parameter gamma, in degrees
- volume of the cell, in Angstroms^3
- density of the cell, in amu/Angstroms^3
- density of the cell, in g/cm^3

"""


import re
import os
import csv
import time


""" This function will extract the numbers from the name of the parent folder. """
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


""" This function will extract the value of a given variable from a raw string. """
def extract(string, name):
    pattern = re.compile(name + r'\s*=\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None


""" This function will exclusively extract the density in g/cm^3, because that line in particular is a pain in the ass. """
def extract_damm_densityg(string):
    pattern = re.compile(r'=\s*([\d\.]+)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None


""" This function will search for a specific string value in a given file, and return the corresponding line """
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



time_start = time.time()



ev = 1.602176634E-19 / 1000 # eV to kJ

row = []

# Get the absolute path to the directory containing the Python script
dir_path = os.path.dirname(os.path.realpath(__file__))
# Specify the path to the directory containing the folders relative to the script's directory
path = os.path.join(dir_path, 'data') # This is the path to the folder containing the folders with the .castep files
# Get the names of all the directories in the given path
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

print(" ")
print("Starting to read files...")
print(" ")

# Here we open the file to write the data
with open('out_castep.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write a header row for the CSV file
    writer.writerow(['file', 'enthalpy', 'enthalpy*ev', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'cell', 'density', 'density_g'])

    # Let's loop through all the folders in the path
    for directory in directories:

        file = os.path.join(path, directory, 'cc-2.castep')

        file_name = naming(directory)

        enthalpy_str = searcher(file, 'LBFGS: Final Enthalpy     =')
        cell_str = searcher(file, 'Current cell volume =')
        density_str = searcher(file, 'density =')
        densityg_str = searcher(file, '=') # This line in particular is weird so be careful
        a_str = searcher(file, 'a =')
        b_str = searcher(file, 'b =')
        c_str = searcher(file, 'c =')

        enthalpy = extract(enthalpy_str, 'LBFGS: Final Enthalpy')
        cell = extract(cell_str, 'Current cell volume')
        density = extract(density_str, 'density')
        densityg = extract_damm_densityg(densityg_str)
        a = extract(a_str, 'a')
        b = extract(b_str, 'b')
        c = extract(c_str, 'c')
        alpha = extract(a_str, 'alpha')
        beta = extract(b_str, 'beta')
        gamma = extract(c_str, 'gamma')

        print(file_name)
        #print("enthalpy = ",enthalpy)
        #print("cell = ",cell)
        #print("density = ",density)
        #print("densityg = ",densityg)
        #print("a = ",a)
        #print("b = ",b)
        #print("c = ",c)
        #print("alpha = ",alpha)
        #print("beta = ",beta)
        #print("gamma = ",gamma)
        #print("")

        # create a dataframe with the data
        row = [file_name, enthalpy, enthalpy*ev, a, b, c, alpha, beta, gamma, cell, density, densityg]
        writer.writerow(row)

print("Done!")


time_elapsed = (time.time() - time_start)
print("Completed in ", time_elapsed, " seconds")