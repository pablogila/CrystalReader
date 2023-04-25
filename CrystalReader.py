"""
CrystalReader Launcher. Read and extract data from different files.
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



job_file = 'CrystalReader_JOBS.txt'



import time
try:
    import cr_common as cr
    # import cr_castep as castep
    # import cr_cif as cif
    # import cr_phonon as phonon
except:
    print("")
    print("  ----------------------------------------------------------")
    print("  ERROR:  Could not import the CrystalReader modules.")
    print("  Read the docs at https://github.com/pablogila/CrystalReader")
    print("  Closing...")
    print("  ----------------------------------------------------------")
    print("")
    exit()
try:
    import pandas as pd
except:
    print("")
    print("  ----------------------------------------------------------")
    print("  ERROR:  Could not import the pandas module")
    print("  Perform 'pip install --user pandas' to install it")
    print("  Closing...")
    print("  ----------------------------------------------------------")
    print("")
    exit()



print("\n")
print("  -----------------------------------------------------------------------")
print("  Welcome to CrystalReader version " + cr.version())
print("  This is free software, and you are welcome to")
print("  redistribute it under GNU General Public License.")
print("  You should have already configured the '" + job_file + "'")
print("  batch file and the corresponding scripts, else check the documentation.")
print("  -----------------------------------------------------------------------")
print("  If you find this code useful, a citation would be awesome :D")
print("  Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader")
print("  -----------------------------------------------------------------------")
print("")
#print("  Conversion factors:")
#print("  cm^-1 to eV =", cr.cm_ev())
#print("  eV to kJ/mol =", cr.ev_kjmol())
#print("")
time_start = time.time()


try:
    cr.jobs(job_file)
except:
    cr.create_job_file(job_file)
    print("")
    print("  ----------------------------------------------------------")
    print("  ERROR:  Could not find the batch job file")
    print("  A '" + job_file + "' file was created with examples")
    print("  ----------------------------------------------------------")
    print("\n")
    exit()


##############################################################
#  EXAMPLES FOR CALLING THE SCRIPTS WITHOUT A BATCH JOB FILE
##############################################################
# First, uncomment the import castep, cif and phonon lines at the top of this file
# Default values to call are listed in the examples. This follows the same structure as the batch job file.
# Other parameters can be modified from within the scripts.
#
# castep.main(data_directory='data', data_castep='cc-2.castep', out='out_castep.csv', out_error='errors_castep.txt')
# cif.main(data_directory='data', data_cif='cc-2-out.cif', out='out_cif.csv', out_error='errors_cif.txt')
# phonon.main(data_directory='data', data_phonon='cc-2_PhonDOS.phonon', out='out_phonon.csv', out_error='errors_phonon.txt')
##############################################################


print("")
print("  All jobs finished in", round(time.time() - time_start, 1), "seconds\n")
print("")

