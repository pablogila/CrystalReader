"""
CrystalReader version 'castep'. Read and extract data from '.castep' files.
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

print("")
print("  Running CrystalReader in 'castep' mode...")
print("  If you find this code useful, a citation would be greatly appreciated :D")
print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")



######################################
""" PARAMETERS THAT YOU MAY MODIFY """
######################################


out_castep = 'out_castep.csv'
data_directory = 'data'
data_castep = 'cc-2.castep'
# If you change the header, make sure to change the columns in the 'row = [...]' line below
header_castep = ['filename', 'enthalpy / eV', 'enthalpy / kJ/mol', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'cell volume / A^3', 'density / amu/A^3', 'density / g/cm^3']



#####################################
""" MAIN SCRIPT FOR .CASTEP FILES """
#####################################


import os
import csv
import time
import cr_common as cr


# Get the absolute path to the directory containing the Python script
dir_path = os.path.dirname(os.path.realpath(__file__))
# Specify the path to the directory containing the folders with the .castep files, relative to the script's directory
path = os.path.join(dir_path, data_directory)
# Get the names of all the directories in the given path, and store them in a list
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

# Open the output file to write the data
with open(out_castep, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write a header row for the CSV file
    writer.writerow(header_castep)

    # Start a timer and counter for the progress bar
    time_start = time.time()
    loop = 0
    # Loop through all the folders in the /data path
    for directory in directories:
        # Progress bar, just for fun
        loop += 1
        cr.progressbar_ETA(loop, len(directories), time_start)

        # Define the path to the .castep file
        file = os.path.join(path, directory, data_castep)
        file_name = cr.naming(directory)

        # Read the file and look for the desired lines
        enthalpy_str = cr.searcher(file, 'LBFGS: Final Enthalpy     =')
        volume_str = cr.searcher(file, 'Current cell volume =')
        density_str = cr.searcher(file, 'density =')
        densityg_str = cr.searcher(file, '=')
        a_str = cr.searcher(file, 'a =')
        b_str = cr.searcher(file, 'b =')
        c_str = cr.searcher(file, 'c =')

        # Extract the values from the strings
        enthalpy = cr.extract_float(enthalpy_str, 'LBFGS: Final Enthalpy')
        volume = cr.extract_float(volume_str, 'Current cell volume')
        density = cr.extract_float(density_str, 'density')
        densityg = cr.extract_float(densityg_str, '')
        a = cr.extract_float(a_str, 'a')
        b = cr.extract_float(b_str, 'b')
        c = cr.extract_float(c_str, 'c')
        alpha = cr.extract_float(a_str, 'alpha')
        beta = cr.extract_float(b_str, 'beta')
        gamma = cr.extract_float(c_str, 'gamma')

        # write the data row to the file
        row = [file_name, enthalpy, enthalpy*cr.ev_kjmol(), a, b, c, alpha, beta, gamma, volume, density, densityg]
        writer.writerow(row)

        # Print the data on screen, for debugging purposes
        #print(file_name)
        #print("enthalpy = ", enthalpy)
        #print("enthalpy*cr.ev_kjmol() = ", enthalpy*cr.ev_kjmol())
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

time_elapsed = round(time.time() - time_start, 2)
print("")
print("  Finished reading the ", data_castep, " files in ", time_elapsed, " seconds")
print("  Data extracted and saved to ", out_castep)
print("")
