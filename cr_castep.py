"""
CrystalReader 'castep' script. Read and extract data from '.castep' files.
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
print("  If you find this code useful, a citation would be awesome :D")
print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")



######################################
""" PARAMETERS THAT YOU MAY MODIFY """
######################################


out_castep = 'out_castep.csv'
data_directory = 'data'
data_castep = 'cc-2.castep'
# If you change the header, make sure to change the columns in the 'row = [...]' line below
header_castep = ['filename', 'enthalpy [eV]', 'enthalpy [kJ/mol]', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'cell volume [A^3]', 'density [amu/A^3]', 'density [g/cm^3]']
error_log = 'errors_castep.txt'


#####################################
""" MAIN SCRIPT FOR .CASTEP FILES """
#####################################


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

# Create an empty array to store the data
errors = []
rows = []
rows.append(header_castep)

# Start a timer and counter for the progress bar
time_start = time.time()
loop = 0
# Loop through all the folders in the /data path
for directory in directories:
    # Progress bar, just for fun
    loop += 1
    cr.progressbar(loop, len(directories))

    # Define the path to the .castep file
    file = os.path.join(path, directory, data_castep)
    file_name = cr.naming(directory)

    ### DEBUGGING ###
    #print(file_name)

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

    # Convert enthalpy from eV to kJ/mol
    if enthalpy == None:
        enthalpy_ev = None
    else:
        enthalpy_ev = enthalpy * cr.ev_kjmol()
    
    # save the data row to the rows array
    row = [file_name, enthalpy, enthalpy_ev, a, b, c, alpha, beta, gamma, volume, density, densityg]
    rows.append(row)

    # Check if any of the values are missing
    error = [file_name]
    for i, var in enumerate(row):
        if var is None:
            error.append(header_castep[i])
    if len(error) > 1:
        errors.append(error)

    #### DEBUGGING ###
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

print("")

df = pd.DataFrame(rows)

# Check for errors. any() is called twice, because it works column-wise
if pd.isnull(df).any().any():
    #df = df.fillna('ERROR')
    print("  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("   COMPLETED WITH ERRORS: THE FOLLOWING VALUES ARE MISSING ")
    for k in errors:
        print("  ", k)
    print("   Error log registered in ", error_log)
    print("  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    log = pd.DataFrame(errors)
    log.to_csv(error_log, header=False, index=False)

# Write the DataFrame to a CSV file
df.to_csv(out_castep, header=False, index=False)

time_elapsed = round(time.time() - time_start, 2)
print("  Finished reading ", data_castep, " files in ", time_elapsed, " seconds")
print("  Data saved to ", out_castep)
print("")

