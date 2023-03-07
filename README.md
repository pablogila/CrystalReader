# CrystalReader

The purpose of this set of programs is to automate the reading and extracting of information from `.castep`, `.cif` and `.phonon` files.

## CastepReader

The `CastepReader.py` program recursively reads a folder called `data`, which itself contains several folders, each containing a cc-2.castep file.\
Naming example: `data/pnam-p-1-000-000-180-000---400/cc-2.castep`\
The program extracts the relevant data from these files, starting from the end of the file, and writes everything in an `out_castep.csv`, in the following columns:

* name of the parent folder, in `xxx-xxx-xxx-xxx` format
* enthalpy of the final iteration, in eV
* enthalpy of the final iteration, in kJ/mol (NEEDS FIXING)
* cell parameter a, in Angstroms
* cell parameter b
* cell parameter c
* cell parameter alpha, in degrees
* cell parameter beta
* cell parameter gamma
* volume of the cell, in Angstroms^3
* density of the cell, in amu/Angstroms^3
* density of the cell, in g/cm^3