"""
CrystalReader 'cif' script. Read and extract data from '.cif' files.
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
print("  Running CrystalReader in 'cif' mode...")
print("  If you find this code useful, a citation would be awesome :D")
print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")



######################################
""" PARAMETERS THAT YOU MAY MODIFY """
######################################


out = 'out_cif.csv'
data_directory = 'data'
data_cif = 'cc-2-out.cif'
data_cifE = 'cc-2_Efield-out.cif'
# If you change the header, make sure to change the columns in the 'row = [...]' line below
header = ['filename', 'SSG_H_M', 'SSG_H_M-Efield']
out_error = 'errors_cif.txt'
# Seconds for a loop to be considered as an error
cry = 5
# Omit, or not, all values from corrupted files
safemode = True



##################################
""" MAIN SCRIPT FOR .CIF FILES """
##################################


import os
import time
import cr_common as cr
import pandas as pd


# Get the absolute path to the directory containing the Python script
dir_path = os.path.dirname(os.path.realpath(__file__))
# Specify the path to the directory containing the folders with the .castep files, relative to the script's directory
path = os.path.join(dir_path, data_directory)
# Get the names of all the directories in the given path, and store them in a list
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

# Empty arrays to store the data
errors = []
rows = []
rows.append(header)

# Start a timer and counter, for the progress bar and warning messages
time_start = time.time()
bar = time_start
loop = 0

# Loop through all the folders in the /data path
for directory in directories:

    # Progress bar, just for fun
    loop += 1
    cr.progressbar(loop, len(directories), bar)
    
    # Define the path to the .cif files
    file_cif = os.path.join(path, directory, data_cif)
    file_cifE = os.path.join(path, directory, data_cifE)
    file_name = cr.naming(directory)

    # Read the file and look for the desired lines
    cif_str = cr.searcher(file_cif, cry, '_symmetry_space_group_name_H_M')
    cifE_str = cr.searcher(file_cifE, cry, '_symmetry_space_group_name_H_M')

    # Extract the values from the strings
    cif = cr.extract_str(cif_str, '_symmetry_space_group_name_H_M')
    cifE = cr.extract_str(cifE_str, '_symmetry_space_group_name_H_M')

    row = [file_name, cif, cifE]

    # ERRORS: Check if any of the values are missing
    error = [file_name]
    for i, var in enumerate(row):
        if var is None:
            errors.append(error)
            bar = True
            if safemode == True:
                row = [file_name]
            break

    rows.append(row)


print("")

# Save the data to a CSV file
df = pd.DataFrame(rows)
df.to_csv(out, header=False, index=False)

# Display and save errors and warnings
cr.errorlog(out_error, errors)

# Final message  
time_elapsed = round(time.time() - time_start, 1)
print("  Finished reading the ", data_cif, " and ", data_cifE, " files in ", time_elapsed, " seconds")
print("  Data extracted and saved to ", out)
print("")


