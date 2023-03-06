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


import re


def extract(string, name):
    pattern = re.compile(name + r'\s*=\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None


# This function will exclusively extract the density in g/cm^3, because that line in particular is a pain in the ass
def extract_damm_densityg(string):
    pattern = re.compile(r'=\s*([\d\.]+)')
    match = pattern.search(string)
    if match:
        return float(match.group(1))
    else:
        return None


def searcher(filename, search_value):
    with open(filename, 'r') as file:
        file.seek(0, 2)  # move the file pointer to the end of the file
        position = file.tell()  # get the position of the file pointer
        while position >= 0:
            file.seek(position)
            next_char = file.read(1)
            if next_char == '\n':
                line = file.readline().strip()
                if line.startswith(search_value):
                    return line
            position -= 1
    return None


enthalpy_str = searcher('cc-2.castep', 'LBFGS: Final Enthalpy     =')
cell_str = searcher('cc-2.castep', 'Current cell volume =')
density_str = searcher('cc-2.castep', 'density =')
densityg_str = searcher('cc-2.castep', '=') # This line in particular is weird so be careful
a_str = searcher('cc-2.castep', 'a =')
b_str = searcher('cc-2.castep', 'b =')
c_str = searcher('cc-2.castep', 'c =')


enthalpy = extract(enthalpy_str, 'LBFGS: Final Enthalpy')
cell = extract(cell_str, 'Current cell volume')
density = extract(density_str, 'density')
densityg = extract_damm_densityg(densityg_str)
a = extract(a_str, 'a')
b = extract(b_str, 'b')
c = extract(c_str, 'c')
alpha = extract(a_str, 'alpha')
beta = extract(b_str, 'beta')
gamma = extract(c_str, 'gamma')

print("")
print("enthalpy = ",enthalpy)
print("cell = ",cell)
print("density = ",density)
print("densityg = ",densityg)
print("a = ",a)
print("b = ",b)
print("c = ",c)
print("alpha = ",alpha)
print("beta = ",beta)
print("gamma = ",gamma)
print("")


