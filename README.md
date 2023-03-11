# CrystalReader

The purpose of this set of programs is to automate the reading and extracting of information from `.castep`, `.cif` and `.phonon` files.


## Usage

First download the source code, as you prefer:
* From your **web browser**  
On GitHub, clic on 'Code', 'Download ZIP', and extract.
* Using **git**  
`git clone https://github.com/pablogila/CrystalReader.git`

Enter the folder and copy inside the data you want to extract, in a subfolder called `/data` ; inside this folder there should be several nested folders containing your data files. Note that the name of this parent folder can be changed from within the scripts by modifying the `data_directory` variable. The naming of the files are detailed in the following sections.

To execute the scripts:
* On **Windows PowerShell** or **CMD**  
`python <script>`
* On **Linux Terminal**  
`python3 <script>`

replacing `<script>` with the name of the script you want to execute. This can be any of the following:
* `CrystalReader_castep.py`, for reading `.castep` files
* `CrystalReader_cif.py`, for reading `.cif` files

For example, to extract data from `.castep` files on Windows PowerShell, you would type:  
`python CrystalReader_castep.py`

The behavior and customization of each script is explained in the following sections.


## CrystalReader_castep

The `CrystalReader_castep.py` program recursively reads the `cc-2.castep` files in the nested folders inside the `/data` folder. As for the parent folder, the names of the files are easily modified changing the `data_castep` variable.

Naming example: `data/pnam-p-1-000-000-180-000---400/cc-2.castep`

The program iterates over this set of files, starting to read from the end of the file, and writes the relevant data to an `out_castep.csv`, line by line, on each iteration. The columns written contain the following data:

* name of the parent folder, in `xxx-xxx-xxx-xxx` format
* final enthalpy, in eV
* final enthalpy, in kJ/mol
* cell parameter a, in Angstroms
* cell parameter b
* cell parameter c
* cell parameter alpha, in degrees
* cell parameter beta
* cell parameter gamma
* cell volume, in Angstroms^3
* density of the cell, in amu/Angstroms^3
* density of the cell, in g/cm^3


## CrystalReader_cif

`CrystalReader_cif.py` uses the same folder structure as before, but the files to read are `cc-2-out.cif` and `cc-2_Efield-out.cif`. Again, this behaviour can be modified with the variables `data_cif` and `data_cifE`.

The program iterates over this set of files and writes the relevant info to an `out_cif.csv`, containing the following data:
* name of the parent folder, in `xxx-xxx-xxx-xxx` format
* symmetry_space_group_name_H_M from the normal cif
* symmetry_space_group_name_H_M from the Efield cif


## CrystalReader_phonon

`CrystalReader_phonon.py` uses the same folder structure. The data files are called `cc-2_Efield.phonon`, and can be modified via the `data_phonon` variable.

The program will read the 144 lines corresponding to the 144 vibration modes; this number can be changed with the `data_phonon_lines` variable.

There is a threshold, set by the variable `too_big`, which triggers a note if the first 3 energies are different from zero.

The program iterates over the set of files, and writes the following info to an `out_phonon.csv`:

* name of the parent folder, in `xxx-xxx-xxx-xxx` format
* InfraRed activity of the 1st mode
* IR 2
* IR 3
* Energy of the 1st mode, cm^-1
* E 2
* E 3
* Is E of the first 3 modes different from zero?
* E 73
* E 74
* E 75
* E 76
* Zero Energy Gamma Point, cm^-1 
* Zero Energy Gamma Point, eV


## Common Functions

The scripts use the following functions:

* `searcher(filename, search_value)`. This function reads the `filename` file starting from the end, until it finds a line starting with `search_value`, and then returns the entire line as an output string.

* `searcher_rows(filename, search_value, number_rows)`. Similar to `searcher()`, but returns an array with the matching line at the first position, and the subsequent rows specified by `number_rows` filling the rest of the array.

* `extract_float(string, name)`. This function extracts the float value of a given `name` variable from a raw `string`, by searching the given string for a matching pattern as `(name + r'\s*=?\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')`, where:
  * `\s*=?\s*` matches any whitespace characters, followed by an optional equals sign, followed by any whitespaces
  * `-?` matches an optional minus sign
  * `\d+` matches one or more digits
  * `(?:\.\d+)?` matches an optional decimal point followed by one or more digits
  * `(?:[eE][+\-]?\d+)?` matches an optional exponent in scientific notation, which consists of an "e" or "E" character, an optional plus or minus sign, and one or more digits.


&NewLine;
* `extract_str(string, name)`. Similar to `extract_float()`, but returns string outputs; if the value is between commas it is returned without said commas.

* `extract_column(string, column)`. Similar to `extract_float` and `extract_str`. It can extract specific columns from a row given as `string`, with `column` being 0, 1, 2...

* `naming(string)`. This function reads the name of the folder, and returns it in the `xxx-xxx-xxx-xxx` format. Be aware that if your nested folders follow a different naming, you may want to change the `pattern` variable inside this function.

* `progressbar(current, total)` and `progressbar_ETA(current, total, start)`. These functions give you a hint as to whether or not you can go out and get coffee. The Estimated Time of Arrival (ETA) is usually not reliable until 20% into the loop and is not displayed until then.  
The loop should have the following structure:
``` python
    loop = 0
    time_loop = time.time()
    for directory in directories:
        loop += 1
        progressbar_ETA(loop, len(directories), time_loop)
        # Loopy things
```

If you find this scripts useful, a citation would be greatly appreciated :D  
*Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader*  
This is free software, and you are welcome to redistribute it under GNU General Public License.