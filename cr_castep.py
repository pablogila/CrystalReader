"""
CrystalReader 'castep' script. Read and extract data from '.castep' files.
Copyright (C) 2023  Pablo Gila-Herranz
If you find this code useful, a citation would be awesome :D
Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader

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


import os
import time
import cr_common as cr
import pandas as pd



##################################################################
#                PARAMETERS THAT YOU MAY MODIFY
##################################################################
# Run the main script for *.castep files at execution. Set to False to import the functions as a module.
run_at_import = False
# Main program for reading castep files. 
def main(data_directory='data', data_castep='cc-2.castep', out='out_castep.csv', out_error='errors_castep.txt'):
    # Seconds for a loop to be considered as an error. Remove this threshold by setting 'cry = False'
    cry = 5
    # Omit, or not, all values from corrupted files
    safemode = True
    # IF YOU CHANGE THE HEADER, make sure to change the columns in the 'row = [...]' line, as well to comment the unnecesary 'searcher' and 'extract' lines. Full header is shown in the next comment for further reference:
    # header = ['filename', 'enthalpy [eV]', 'enthalpy [kJ/mol]', 'total energy corrected [eV]', 'space group', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'cell volume [A^3]', 'density [amu/A^3]', 'density [g/cm^3]']
    header = ['filename', 'total energy corrected [eV]', 'space group', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'cell volume [A^3]', 'density [amu/A^3]', 'density [g/cm^3]']
##################################################################

    print("")
    print("  Running CrystalReader", cr.version(), "in 'castep' mode...")
    print("")
    print("  data directory:      ", data_directory)
    print("  data files:          ", data_castep)
    print("  output file:         ", out)
    print("  error log:           ", out_error)
    print("  abortion time:       ", cry)
    print("  safemode:            ", safemode)
    print("")

    # To avoid errors if we comment the enthalpy lines
    enthalpy = None

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
        
        # Define the path to the .castep file
        file_castep = os.path.join(path, directory, data_castep)
        file_name = cr.naming(directory)

        # Read the file and look for the desired lines
        #enthalpy_str = cr.searcher(file_castep, 'LBFGS: Final Enthalpy     =', cry)
        energy_str = cr.searcher(file_castep, 'Total energy corrected for finite basis set =', cry)
        space_group_str = cr.searcher(file_castep, 'Space group of crystal =', cry).replace(',','.')
        volume_str = cr.searcher(file_castep, 'Current cell volume =', cry)
        density_str = cr.searcher(file_castep, 'density =', cry, 1)
        a_str = cr.searcher(file_castep, 'a =', cry)
        b_str = cr.searcher(file_castep, 'b =', cry)
        c_str = cr.searcher(file_castep, 'c =', cry)

        # Extract the values from the strings
        #enthalpy = cr.extract_float(enthalpy_str, 'LBFGS: Final Enthalpy')
        energy = cr.extract_float(energy_str, 'Total energy corrected for finite basis set')
        space_group = cr.extract_str(space_group_str, 'Space group of crystal')
        volume = cr.extract_float(volume_str, 'Current cell volume')
        density = cr.extract_float(density_str[0], 'density')
        density_g = cr.extract_float(density_str[1], '')
        a = cr.extract_float(a_str, 'a')
        b = cr.extract_float(b_str, 'b')
        c = cr.extract_float(c_str, 'c')
        alpha = cr.extract_float(a_str, 'alpha')
        beta = cr.extract_float(b_str, 'beta')
        gamma = cr.extract_float(c_str, 'gamma')

        # Convert enthalpy from eV to kJ/mol
        if enthalpy != None:
            enthalpy_ev = enthalpy * cr.ev_kjmol()
        else:
            enthalpy_ev = None

        ##################################################################
        #       IF YOU MODIFIED THE HEADER, MODIFY THE COLUMNS TOO
        ##################################################################
        # Values to save. Full row in the following comment for further reference:
        # row = [file_name, enthalpy, enthalpy_ev, energy, space_group, a, b, c, alpha, beta, gamma, volume, density, density_g]
        row = [file_name, energy, space_group, a, b, c, alpha, beta, gamma, volume, density, density_g]
        ##################################################################

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
    print("")
    print("  Finished reading ", data_directory + "/.../" + data_castep, " files in " + str(time_elapsed) + " seconds")
    print("  Data extracted and saved to ", out)
    print("")


if run_at_import:
    main()

