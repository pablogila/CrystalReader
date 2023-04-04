"""
CrystalReader Common Functions. Read and extract data from different files.
Copyright (C) 2023  Pablo Gila-Herranz

If you find this code useful, a citation would be awesome :D
Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader
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


import re
import time
import pandas as pd



def version():
    return "vCR.2023.04.04.1800"



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
    pattern = re.compile(name + r"\s*(=)?\s*['\"](.*?)(?=['\"]|$)")
    match = pattern.search(string)
    if match:
        return match.group(2).strip()
    else:
        return None


# This function will extract the string value of a given variable from a raw string
def extract_column(string, column):
    if string == None:
        return None
    columns = string.split()
    pattern = r'(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'
    if column < len(columns):
        match = re.match(pattern, columns[column])
        if match:
            return float(match.group(1))
    return None


# This function will search for a specific string value in a given file, and return the corresponding line
def searcher(filename, time_limit, search_value):
    with open(filename, 'r') as file:
        # Move the file pointer to the end of the file
        file.seek(0, 2)
        # Get the position of the file pointer
        position = file.tell()
        time_start = time.time() # record the start time
        while position >= 0:
            # Check if the elapsed time exceeds the specified time limit
            if time_limit and time.time() - time_start > time_limit:
                return None
            file.seek(position)
            next_char = file.read(1)
            if next_char == '\n':
                line = file.readline().strip()
                if line.startswith(search_value):
                    return line
            position -= 1
    return None


# This function will search for a specific string value in a given file, and return the following lines after the match
def searcher_rows(filename, time_limit, search_value, number_rows):
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
                    lines.append(line)
                    for i in range(number_rows):
                        next_line = file.readline().strip()
                        if next_line:
                            lines.append(next_line)
                    break
            position -= 1
    return lines[::1]


# This function will print a progress bar in the console, as well as the ETA, just for fun
def progressbar(current, total, start):
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


# Take the list of missing files as errors and slow loops as warnings, write them to a log file and display in the console
def errorlog(error_log, errors):
    if len(errors) > 0:
        errors.insert(0, "COMPLETED WITH ERRORS: The following files seem corrupted:")
        log = pd.DataFrame(errors)
        log.to_csv(error_log, header=False, index=False)
        print("  ----------------------------------------------------------")
        for k in errors:
            print("  "+str(k))
        print("  Error log registered in ", error_log)
        print("  ----------------------------------------------------------")


# Conversion factor from eV to kJ/mol, Supposing that the energy is in eV/cell
def ev_kjmol():
    return ((1.602176634E-19 / 1000) * 6.02214076E+23)


# Conversion factor from cm^-1 to eV
def cm_ev():
    return (1.0 / 8065.54429)



#######################
###  OLD FUNCTIONS  ###
### left for legacy ###
#######################


# Take the list of missing files as errors and slow loops as warnings, write them to a log file and display in the console
def errorlog_OLD(error_log, errors, warnings):
    # Remove warnings that resulted in errors, saving in warn[] only the loops that took too long yet seemed to work
    error_files = [error[0] for error in errors]
    warning_files = [warning[0] for warning in warnings]
    warn = []
    for i, warning in enumerate(warning_files):
        if warning not in error_files:
            warn.append(warnings[i])
    # Write the errors and warnings to a log file, and print them to the console
    if len(errors) > 0:
        errors.insert(0, "COMPLETED WITH ERRORS:  The following values are missing:")
    if len(warn) > 0:
        warn.insert(0, "WARNING:  The following files were suspiciously slow to read:")
        for warning in warn:
            errors.append(warning)
    if len(errors) > 0:
        log = pd.DataFrame(errors)
        log.to_csv(error_log, header=False, index=False)
        print("  ---------------------------------------------------------")
        for k in errors:
            print("  "+str(k))
        print("  Error log registered in ", error_log)
        print("  DON'T TRUST FILES WITH ERRORS OR WARNINGS, CHECK MANUALLY")
        print("  ---------------------------------------------------------")

