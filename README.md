# CrystalReader

The purpose of this set of programs is to automate the reading and extracting of information from `.castep`, `.cif` and `.phonon` files.

## CastepReader

The `CastepReader.py` program recursively reads a folder called `/data`, which contains several nested folders, each containing a `cc-2.castep` file.\
Naming example: `data/pnam-p-1-000-000-180-000---400/cc-2.castep`.\
The program iterates over this set of files, starting to read from the end of the file, and writes the relevant data to an `out_castep.csv`, line by line, on each iteration. The columns written contain the following data:

* name of the parent folder, in `xxx-xxx-xxx-xxx` format
* final enthalpy, in eV
* final enthalpy, in kJ/mol -----NEEDS FIXING-----
* cell parameter a, in Angstroms
* cell parameter b
* cell parameter c
* cell parameter alpha, in degrees
* cell parameter beta
* cell parameter gamma
* cell volume, in Angstroms^3
* density of the cell, in amu/Angstroms^3
* density of the cell, in g/cm^3

### CastepReader Functions

The program `CastepReader.py` calls the following functions:

* `searcher(filename, search_value)`. This function reads a given file in `filename` from the end, until it finds a line starting with `search_value`, and then returns the entire line as an output string.

* `extract(string, name)`. This function extracts the float value of a given variable from a raw string by searching the given string for a matching pattern as `name + r'\s*=\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'`, where:
  * `\s*=\s*` matches zero or more whitespace characters, followed by an equals sign, followed by zero or more whitespace characters
  * `-?` matches an optional minus sign
  * `\d+` matches one or more digits
  * `(?:\.\d+)?` matches an optional decimal point followed by one or more digits
  * `(?:[eE][+\-]?\d+)?` matches an optional exponent in scientific notation, which consists of an "e" or "E" character, an optional plus or minus sign, and one or more digits.

&NewLine;
* `naming(string)`. This function reads the name of the parent folder, and returns it in the `xxx-xxx-xxx-xxx` format.

* `progressbar(current, total)`. Don't mind how it works, just know that it gives you a hint as to whether or not you can go out and get coffee.