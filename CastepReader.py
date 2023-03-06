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

# Import the read_castep_file function from castep_parse
from castep_parse import read_castep_file

# Load a .castep file into a CastepFile object
cf = read_castep_file('cc-2.castep')

# Extract the data you want
final_enthalpy = cf.final_enthalpy # in eV
cell_parameters = cf.cell_parameters # in Angstroms
a, b, c = cell_parameters['a'], cell_parameters['b'], cell_parameters['c']
alpha, beta, gamma = cell_parameters['alpha'], cell_parameters['beta'], cell_parameters['gamma']
volume = cf.volume # in Angstroms^3
density = cf.density # in g/cm^3

# Print the data
print(f'Final enthalpy: {final_enthalpy} eV')
print(f'Cell parameters: a={a}, b={b}, c={c}, alpha={alpha}, beta={beta}, gamma={gamma}')
print(f'Volume: {volume} Angstroms^3')
print(f'Density: {density} g/cm^3')


