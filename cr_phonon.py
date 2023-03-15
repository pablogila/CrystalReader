"""
CrystalReader 'phonon' script. Read and extract data from '.phonon' files.
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
print("  Running CrystalReader in 'phonon' mode...")
print("  If you find this code useful, a citation would be greatly appreciated :D")
print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")



######################################
""" PARAMETERS THAT YOU CAN MODIFY """
######################################


out_phonon = 'out_phonon.csv'
data_directory = 'data'
data_phonon = 'cc-2_Efield.phonon'
data_lines_phonon = 144
# Threshold for the energy to be considered greater than zero
threshold = 0.5
# If you change the header, make sure to change the columns in the 'row = [...]' line below
header_phonon = ['filename', 'E_1', 'E_2', 'E_3', 'E>'+str(threshold)+'?', 'E_73', 'E_74', 'E_75', 'E_76', 'Zero_E_Gamma_Point=(E_4++144)/2 / cm^-1', 'Zero_E_Gamma_Point / eV']



#####################################
""" MAIN SCRIPT FOR .PHONON FILES """
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
with open(out_phonon, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write a header row for the CSV file
    writer.writerow(header_phonon)

    # Start a timer and counter for the progress bar
    time_start = time.time()
    loop = 0
    # Loop through all the folders in the /data path
    for directory in directories:
        # Progress bar, just for fun
        loop += 1
        cr.progressbar_ETA(loop, len(directories), time_start)

        # Define the path to the .castep file
        file_phonon = os.path.join(path, directory, data_phonon)
        file_name = cr.naming(directory)

        # Read the file and look for the desired line, return the corresponding lines after the match
        # The phonon_str[0] is the header, the phonon_str[1] is the first line of data, etc.
        phonon_str = cr.searcher_rows(file_phonon, 'q-pt=', data_lines_phonon)

        #Ir_1 = cr.extract_column(phonon_str[1], 2)
        #Ir_2 = cr.extract_column(phonon_str[2], 2)
        #Ir_3 = cr.extract_column(phonon_str[3], 2)
        E_1 = cr.extract_column(phonon_str[1], 1)
        E_2 = cr.extract_column(phonon_str[2], 1)
        E_3 = cr.extract_column(phonon_str[3], 1)
        E_73 = cr.extract_column(phonon_str[73], 1)
        E_74 = cr.extract_column(phonon_str[74], 1)
        E_75 = cr.extract_column(phonon_str[75], 1)
        E_76 = cr.extract_column(phonon_str[76], 1)

        # Check if the first energies are greater than the threshold
        if (abs(E_1) > threshold) or (abs(E_2) > threshold) or (abs(E_3) > threshold):
            question = 'YES'
        else:
            question = 'no'
        
        ZEGP = 0
        for k in range(4, data_lines_phonon + 1):
            ZEGP += cr.extract_column(phonon_str[k], 1)
        ZEGP = ZEGP/2
        
        # write the data row to the file
        row = [file_name, E_1, E_2, E_3, question, E_73, E_74, E_75, E_76, ZEGP, ZEGP * cr.cm_ev()]
        writer.writerow(row)

time_elapsed = round(time.time() - time_start, 2)
print("")
print("  Finished reading the ", data_phonon, " files in ", time_elapsed, " seconds")
print("  Data extracted and saved to ", out_phonon)
print("")
