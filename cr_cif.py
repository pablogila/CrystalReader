"""
CrystalReader 'cif' script. Read and extract data from '.cif' files.
Copyright (C) 2023  Pablo Gila-Herranz
Check the latest version at https://github.com/pablogila/CrystalReader
Feel free to contact me at pablo.gila.herranz@gmail.com

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
# Run the main script for *.cif files at execution. Set to False to import the functions as a module.
run_at_import = False
# Main program for reading cif files. 
def main(data_directory='data', data_cif='cc-2-out.cif', out='out_cif.csv', out_error='errors_cif.txt'):
    # Seconds for a loop to be considered as an error. Remove this threshold by setting 'cry = False'
    cry = 5
    # Omit, or not, all values from corrupted files
    safemode = True
    # IF YOU CHANGE THE HEADER, make sure to change the columns in the 'row = [...]' line, as well to comment the unnecesary 'searcher' and 'extract' lines. Full header is shown in the next comment for further reference:
    # header = ['filename', 'SSG_H_M', 'SSG_H_M-Efield']
    header = ['filename', 'SSG_H_M']
    #data_cifE = 'cc-2_Efield-out.cif'
##################################################################

    print("")
    print("  Running CrystalReader", cr.version(), "in 'cif' mode...")
    print("  If you find this code useful, a citation would be awesome :D")
    print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")
    print("")
    print("  data directory:      ", data_directory)
    print("  data files:          ", data_cif)
    print("  output file:         ", out)
    print("  error log:           ", out_error)
    print("  abortion time:       ", cry)
    print("  safemode:            ", safemode)
    print("")

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
        file_name = cr.naming(directory)
        #file_cifE = os.path.join(path, directory, data_cifE)

        # Read the file and look for the desired lines
        cif_str = cr.searcher(file_cif, '_symmetry_space_group_name_H_M', cry)
        #cifE_str = cr.searcher(file_cifE, '_symmetry_space_group_name_H_M', cry)

        # Extract the values from the strings
        cif = cr.extract_str_commas(cif_str, '_symmetry_space_group_name_H_M')
        #cifE = cr.extract_str_commas(cifE_str, '_symmetry_space_group_name_H_M')

        ##################################################################
        #       IF YOU MODIFIED THE HEADER, MODIFY THE COLUMNS TOO
        ##################################################################
        # Values to save. Full row in the following comment for further reference:
        # row = [file_name, cif, cifE]
        row = [file_name, cif]
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
    print("  Finished reading ", data_directory + "/.../" + data_cif, " files in " + str(time_elapsed) + "s")
    print("  Data extracted and saved to ", out)
    print("")


if run_at_import:
    main()

