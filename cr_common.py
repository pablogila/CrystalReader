"""
CrystalReader Common Functions. Read and extract data from different files.
Copyright (C) 2023  Pablo Gila-Herranz
If you find this code useful, a citation would be awesome :D
Pablo Gila-Herranz, “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader

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



def version():
    return "vCR.2023.09.20.2330"



import re
import time
import os
import pandas as pd
import cr_castep as castep
import cr_cif as cif
import cr_phonon as phonon



# This function will extract the name of the file from a raw string, in the xxx-xxx-xxx-xxx format
def naming(string):
    # Define a regular expression pattern to match the desired value
    pattern = r"(?:\w*-?)+(\d{3})-(\d{3})-(\d{3})-(\d{3})"
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
    if string == None:
        return None
    pattern = re.compile(name + r'\s*=?\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None
    

# This function will extract the string value of a given variable from a raw string
def extract_str(string, name):
    if string == None:
        return None
    pattern = re.compile(name + r"\s*=\s*(\S.*)?$")
    match = pattern.search(string)
    if match:
        return match.group(1).strip()
    else:
        return None


# Similar to extract_str(). If the value is between commas it is returned without said commas
def extract_str_commas(string, name):
    if string == None:
        return None
    pattern = re.compile(name + r"\s*(=)?\s*['\"](.*?)(?=['\"]|$)")
    match = pattern.search(string)
    if match:
        return match.group(2).strip()
    else:
        return None


# This function will extract the desired column of a given string
def extract_column(string, column):
    if string is None:
        return None
    columns = string.split()
    pattern = r'(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'
    if column < len(columns):
        match = re.match(pattern, columns[column])
        if match:
            return float(match.group(1))
    return None


# This function will search for a specific string value in a given file, return the matching line, and optionally also return a specific number of lines following the match
def searcher(filename, search_value, time_limit=False, number_rows=0):
    with open(filename, 'r') as file:
        # Move the file pointer to the end of the file
        file.seek(0, 2)
        # Get the position of the file pointer
        position = file.tell()
        lines = []
        time_start = time.time() # record the start time
        while position >= 0 and len(lines) < number_rows+1:
            # Check if the elapsed time exceeds the specified time limit
            if time_limit and time.time() - time_start > time_limit:
                return None
            file.seek(position)
            next_char = file.read(1)
            if next_char == '\n':
                line = file.readline().strip()
                if line.startswith(search_value):
                    if number_rows == 0:
                        return line
                    lines.append(line)
                    for i in range(number_rows):
                        next_line = file.readline().strip()
                        if next_line:
                            lines.append(next_line)
                    break
            position -= 1
    return None if not lines else lines[::1]


# This function will print a progress bar in the console, as well as the ETA, just for fun
def progressbar(current, total, start=False):
    bar_length = 50
    percentage = int((current/total)*100)
    progress = int((bar_length*current)/total)
    if start == False:
        loadbar = "  [{:{len}}]{:4.0f}%".format(progress*'■',percentage,len=bar_length)
        print(loadbar, end='\r')
    elif start == True:
        loadbar = "  [{:{len}}]{:4.0f}%    Errors detected...".format(progress*'■',percentage,len=bar_length)
        print(loadbar, end='\r')
    else:
        loadbar = "  [{:{len}}]{:4.0f}%".format(progress*'■',percentage,len=bar_length)
        elapsed = time.time() - start
        eta = elapsed * (total/current - 1)
        if current > total/5 and eta >= 0:
            loadbar += "    ETA: {:5.0f}s  ".format(eta)
        else:
            loadbar += "    ETA: >{:4.0f}s  ".format(eta)
        print(loadbar, end='\r')


# This function will read the input file and execute the batch jobs
def jobs(job_file):
    current_directory = os.getcwd()
    job_file_path = os.path.join(current_directory, job_file)
    if os.path.isfile(job_file_path):
        is_file_empty = True
        with open(job_file, 'r') as f:
            lines = f.readlines()
        for line in lines[0:]:
            line = line.split(',')
            line = [x.strip() for x in line]
            if line[0].startswith('#') or line[0] == '':
                continue
            if (line[0] == 'cif' or line[0] == 'CIF' or line[0] == 'castep' or line[0] == 'CASTEP' or line[0] == 'phonon' or line[0] == 'PHONON') and (len(line) >= 3):
                is_file_empty = False
                if len(line) <= 3:
                    errors = 'errors_' + line[1] + '_' + line[2] + '.txt'
                    out = 'out_' + line[1] + '_' + line[2] + '.csv'
                else:
                    out = line[3]
                    if len(line) <= 4:
                        errors = 'errors_' + line[1] + '_' + line[2] + '.txt'
                    else:
                        errors = line[4]
                data_folder = line[1]
                data_path = os.path.join(current_directory, data_folder)
                if os.path.isdir(data_path):
                    if line[0] == 'cif' or line[0] == 'CIF':
                        cif.main(line[1], line[2], out, errors)
                    if line[0] == 'castep' or line[0] == 'CASTEP':
                        castep.main(line[1], line[2], out, errors)
                    if line[0] == 'phonon' or line[0] == 'PHONON':
                        phonon.main(line[1], line[2], out, errors)
                else:
                    error_datafolder_missing(line)
                    continue
            else:
                error_job_unknown(line)
                continue
        if is_file_empty:
            error_jobfile_empty(job_file)
            exit()
    else:
        error_jobfile_missing(job_file)
        exit()


# Take the list of missing files as errors and slow loops as warnings, write them to a log file and display in the console
def errorlog(error_log, errors):
    if len(errors) > 0:
        log = pd.DataFrame(errors)
        log.to_csv(error_log, header=False, index=False)
        print("  ------------------------------------------------------------")
        print("  COMPLETED WITH ERRORS:")
        for k in errors:
            print("  "+str(k))
        print("  Error log registered at ", error_log)
        print("  ------------------------------------------------------------")


def error_datafolder_missing(line):
    print("")
    print("  ------------------------------------------------------------")
    print("  ERROR:  DataFolder not found. Check this line:")
    print(' ',line)
    print("  Skipping to the next job...")
    print("  ------------------------------------------------------------")
    print("")


def error_job_unknown(line):
    print("")
    print("  ------------------------------------------------------------")
    print("  ERROR:  Unknown job. Check this line:")
    print(' ',line)
    print("  Skipping to the next job...")
    print("  ------------------------------------------------------------")
    print("")


def error_jobfile_empty(job_file):
    print("")
    print("  ------------------------------------------------------------")
    print("  WARNING:  '" + job_file + "' batch job file was found,")
    print("  but it is empty. Please fill it and try again.")
    print("  ------------------------------------------------------------")
    print("\n")


def error_jobfile_missing(job_file):
    with open(job_file, 'w') as f:
        f.write("# ----------------------------------------------------------------------------------------------\n")
        f.write("# CrystalReader Batch Job File\n")
        f.write("# Copyright (C) 2023  Pablo Gila-Herranz\n")
        f.write("# If you find this code useful, a citation would be awesome :D\n")
        f.write("# Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader\n")
        f.write("# This is free software, and you are welcome to redistribute it under GNU General Public License\n")
        f.write("#\n")
        f.write("# Write here all the CrystalReader jobs that you want to execute, following this format:\n")
        f.write("# Format(=castep/cif/phonon), DataFolder, DataFiles\n")
        f.write("# Additionally, you can also specify the desired names for the output file and the error log:\n")
        f.write("# Format, DataFolder, DataFiles, Output, ErrorLog\n")
        f.write("# If you specify subpaths, make sure that said folders ('data' and 'out' here) already exist:\n")
        f.write("# Format, data\DataFolder, DataFiles, out\Output, out\ErrorLog\n")
        f.write("#\n")
        f.write("# Example:\n")
        f.write("# phonon, data_rscan, rscan.phonon, out.csv, errors.txt\n")
        f.write("# ----------------------------------------------------------------------------------------------\n")
    print("")
    print("  ------------------------------------------------------------")
    print("  First time running CrystalReader, huh?")
    print("  The batch job file was not found, so an empty one called")
    print("  '" + job_file + "' was created with examples")
    print("  ------------------------------------------------------------")
    print("\n")



############################
###  CONVERSION FACTORS  ###
############################


def print_conversion_factors():
    print("cm^-1 to eV:   ", cm_ev())
    print("eV to cm^-1:   ", ev_cm())
    print("eV to kJ/mol:  ", ev_kjmol())


# Conversion factor from eV to kJ/mol, Supposing that the energy is in eV/cell
def ev_kjmol():
    return ((1.602176634E-19 / 1000) * 6.02214076E+23)


# Conversion factor from cm^-1 to eV
def cm_ev():
    return (1.0 / 8065.54429)


def ev_cm():
    return (8065.54429)

