""""

This program will read specific data from several .castep files.
The .castep files are inside a folder called /PBEsol-MP-2x2x2, and inside that folder, there are 50 new folders, each containing a file named 'cc-2.castep' file.
This program will read the data from the cc-2.castep file in each folder, and output a 'castep.out.csv' file with the data I want, in the root folder.
I want to write the following columns of data in the .csv file, in this order:
- name of the parent folder
- enthalpy of the final iteration, in eV
- empty column
- cell parameter a, in Angstroms
- cell parameter b, in Angstroms
- cell parameter c, in Angstroms
- cell parameter alpha, in degrees
- cell parameter beta, in degrees
- cell parameter gamma, in degrees
- volume of the cell, in Angstroms^3
- density of the cell, in amu/Angstroms^3
- density of the cell, in g/cm^3

"""

import os
import csv
import numpy as np

# Define the path to the folder containing the .castep files
path = '/PBEsol-MP-2x2x2'

# Define the path to the output file
output = 'castep.out.csv'

# Define the list of folders
folders = os.listdir(path)

# Define the list of files
files = []

# Define the list of data
data = []

# Define the list of data to be written to the output file
output_data = []

# Define the list of column names
column_names = ['Folder', 'Enthalpy (eV)', 'Enthalpy (kJ/mol)', 'a (Angstroms)', 'b (Angstroms)', 'c (Angstroms)', 'alpha (degrees)', 'beta (degrees)', 'gamma (degrees)', 'Volume (Angstroms^3)', 'Density (amu/Angstroms^3)', 'Density (g/cm^3)']

# Define the list of units
units = ['-', 'eV', 'kJ/mol', 'Angstroms', 'Angstroms', 'Angstroms', 'degrees', 'degrees', 'degrees', 'Angstroms^3', 'amu/Angstroms^3', 'g/cm^3