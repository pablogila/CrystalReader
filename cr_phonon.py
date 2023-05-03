"""
CrystalReader 'phonon' script. Read and extract data from '.phonon' files.
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
# Threshold for the energy to be considered greater than zero
threshold = 0.1
# Number of phonon lines to read plus one
data_lines_phonon = 144
# !!! IF YOU CHANGE THE HEADER, make sure to change the columns in the 'row = [...]' line, as well to comment the unnecesary 'searcher' and 'extract' lines. Full header is shown in the next comment for further reference:
# header = ['filename', Ir_1, Ir_2, Ir_3, 'E_1', 'E_2', 'E_3', 'E>'+str(threshold)+'?', 'E_73', 'E_74', 'E_75', 'E_76', 'Zero_E_Gamma_Point=(E_4++144)/2 [cm^-1]', 'Zero_E_Gamma_Point [eV]']
header = ['filename', 'E_1', 'E_2', 'E_3', 'E>'+str(threshold)+'?', 'E_73', 'E_74', 'E_75', 'E_76', 'Zero_E_Gamma_Point=(E_4++'+str(data_lines_phonon)+')/2 [cm^-1]', 'Zero_E_Gamma_Point [eV]']
# Run the main script for *.phonon files at execution. Set to False to import the functions as a module.
run_at_import = False
# Rename the file_name in the xxx-xxx-xxx-xxx format; set to False to keep the original name
rename_files = False
# Seconds for a loop to be considered as an error (a.k.a. seconds for me to cry). Remove this threshold by setting 'cry = False'
cry = 30
# Omit, or not, all values from corrupted files
safemode = False
# Main program for reading phonon files. Change the default arguments to run the script from the command line
def main(data_directory='data', data_phonon='cc-2_Efield.phonon', out='out_phonon.csv', out_error='errors_phonon.txt'):
##################################################################

    print("")
    if run_at_import == False:
        print("  Running CrystalReader in 'phonon' mode...")
    if run_at_import == True:
        print("  Running CrystalReader", cr.version(), "in 'phonon' mode...")
        print("  If you find this code useful, a citation would be awesome :D")
        print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")
    print("")
    print("  data directory:      ", data_directory)
    print("  data files:          ", data_phonon)
    print("  output file:         ", out)
    print("  error log:           ", out_error)
    print("  abortion time:       ", cry)
    print("  safemode:            ", safemode)
    print("  phonon lines:        ", data_lines_phonon)
    print("  threshold for E>0:   ", threshold)
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

        # Define the path to the .phonon file
        file_phonon = os.path.join(path, directory, data_phonon)

        # Rename, or not, the file_name in the xxx-xxx-xxx-xxx format
        if rename_files == True:
            file_name = cr.naming(directory)
        else:
            file_name = directory

        # Read the file and look for the desired line, return the corresponding lines after the match
        # The phonon_str[0] is the header, the phonon_str[1] is the first line of data, etc.
        phonon_str = cr.searcher(file_phonon, 'q-pt=', cry, data_lines_phonon)

        try:
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

        except:
            # ERROR:
            error = [file_name]
            errors.append(error)
            bar = True
            row = [file_name]
            rows.append(row)
            continue

        # Check if the first energies are greater than the threshold
        if (abs(E_1) > threshold) or (abs(E_2) > threshold) or (abs(E_3) > threshold):
            question = 'YES'
        else:
            question = 'no'

        ZEGP = 0
        for k in range(4, data_lines_phonon + 1):
            ZEGP += cr.extract_column(phonon_str[k], 1)
        ZEGP = ZEGP/2

        ##################################################################
        #       IF YOU MODIFIED THE HEADER, MODIFY THE COLUMNS TOO
        ##################################################################
        # Values to save. Full row in the following comment for further reference:
        # row = [file_name, Ir_1, Ir_2, Ir_3, E_1, E_2, E_3, question, E_73, E_74, E_75, E_76, ZEGP, ZEGP * cr.cm_ev()]
        row = [file_name, E_1, E_2, E_3, question, E_73, E_74, E_75, E_76, ZEGP, ZEGP * cr.cm_ev()]
        ##################################################################

        # ERRORS: Check if any of the values are missing. For 'phonon' files in particular it should be handled in the 'except' part, and should not be neccesary. However, we leave it here just in case.
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

    time_elapsed = round(time.time() - time_start, 1)
    print("")
    print("  Finished reading the ", data_directory + "/.../" + data_phonon, " files in " + str(time_elapsed) + "s")
    print("  Data extracted and saved to ", out)
    print("")


if run_at_import:
    main()

