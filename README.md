# CrystalReader

CrystalReader is a program to automate the reading and extraction of information from __*.castep__, __*.cif__ and __*.phonon__ files, built with the premise of reliability and ease of reuse through an easy to read code structure, with the potential to be repurposed to process any type of text-based data files.


## Requirements

CrystalReader runs in **Python 3.X** with **Pandas** installed. The use of a virtual environment such as venv is recommended, but not required. 


## Usage

First download the source code, as you prefer:
* From your **web browser**  
On GitHub, clic on 'Code', 'Download ZIP', and extract.
* Using **git**  
`git clone https://github.com/pablogila/CrystalReader.git`

Enter the folder and copy inside the data you want to extract, in a subfolder called `/data` ; inside this folder there should be several nested folders containing your data files. Note that the name of this parent folder can be changed from within the individual scripts by modifying the `data_directory` variable, as well as other parameters that you may also need to modify to accommodate your data; such file naming variables are described in more detail in the following sections.

To execute CrystalReader, open a terminal and type:
* On **Windows PowerShell** or **CMD**  
`python <script>`
* On **Linux Terminal**  
`python3 <script>`

Replacing `<script>` with the name of the CrystalReader script you want to execute. This can be any of the following:
* `CrystalReader.py`, the main Launcher. You will be asked which script to use, or if you prefer, you can run them all to read all the files at once.
* `cr_castep.py`, for reading **.castep** files
* `cr_cif.py`, for reading **.cif** files
* `cr_phonon.py`, for **.phonon** files

For example, to extract data from **.castep** files on Windows PowerShell, you would type:  
`python CrystalReader_castep.py`

The behavior and customization of each script is explained in the following sections.


## For **.castep** files

The `cr_castep.py` script recursively reads the `cc-2.castep` files in the nested folders inside the `/data` folder. As was mentioned for the parent folder, the names of the files are easily modified changing the `data_castep` variable.

Naming example: **data/pnam-p-1-000-000-180-000---400/cc-2.castep**

The program iterates over this set of files, starting to read from the end of the file, and writes the relevant data to an `out_castep.csv`, line by line, on each iteration. The columns written contain the following data:

* name of the parent folder, in **xxx-xxx-xxx-xxx** format
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


## For **.cif** files

`cr_cif.py` uses the same folder structure as before, but the files to read are `cc-2-out.cif` and `cc-2_Efield-out.cif`. Again, this behaviour can be modified with the variables `data_cif` and `data_cifE`.

The program iterates over this set of files and writes the relevant info to an `out_cif.csv`, containing the following data:
* name of the parent folder, in **xxx-xxx-xxx-xxx** format
* symmetry_space_group_name_H_M from the normal cif
* symmetry_space_group_name_H_M from the Efield cif


## For **.phonon** files

`cr_phonon.py` uses the same folder structure. The data files are called `cc-2_Efield.phonon`, and can be modified via the `data_phonon` variable.

The program will read the 144 lines corresponding to the 144 vibration modes; this number can be changed with the `data_lines_phonon` variable.

There is a threshold, set by the variable `threshold`, which triggers a note if one of the first 3 energies are different from zero.

The program iterates over the set of files, and writes the following info to an `out_phonon.csv`:

* name of the parent folder, in **xxx-xxx-xxx-xxx** format
* Energy of the 1st mode, in cm^-1
* E 2
* E 3
* Is E of the first 3 modes different from zero?
* E 73
* E 74
* E 75
* E 76
* Zero Energy Gamma Point, cm^-1 
* Zero Energy Gamma Point, eV


## Error Management

Sometimes some of your files may be corrupted, for example, if the simulation was terminated before it was completed. If a value is not found, an **ERROR** message will be displayed with information about the corrupt file. This particular file will be ignored, because even if other variables could be read, they are probably wrong; however, you can still save the rest of the variables from corrupted files by setting the `safemode` parameter to **False**.

If a file takes too long to read, it is aborted and an **ERROR** message is displayed. The threshold for considering an error is defined by the variable `cry`, which is usually between 5 and 15 seconds by default, but can be set to **False** to remove the time limit. This variable may need to be changed if you are running the scripts on a supercomputer or in a potato with some wires.  

If a value is not found, an **ERROR** is displayed, regardless of whether the **cry** threshold has been reached or not.  

If an error is detected, the relevant information is extracted to an error log defined by the `error_log` variable.  

This whole section could be summarized in the following sentence: **Always check the files marked with ERRORS because they may be corrupt**.


## Common Functions

The functions used to read the files are defined in `cr_common.py` and are imported at the beginning of each script. These functions are the following:

* `searcher(filename, time_limit, search_value)`. This function reads the **filename** file starting from the end, until it finds a line starting with **search_value**, and then returns the entire line as an output string. If the reading takes more than **time_limit** seconds, it will abort and return **None**. This threshold is removed by setting **time_limit** as **False**.

* `searcher_rows(filename, time_limit, search_value, number_rows)`. Similar to **searcher()**, but returns an array with the matching line at the first position, and the subsequent number of lines specified by **number_rows** filling the rest of the array.

* `extract_float(string, name)`. This function extracts the float value of a given **name** variable from a raw **string**, by searching the given string for a matching pattern as `(name + r'\s*=?\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')`, where:
  * `\s*=?\s*` matches any whitespace characters, followed by an optional equals sign, followed by any whitespaces
  * `-?` matches an optional minus sign
  * `\d+` matches one or more digits
  * `(?:\.\d+)?` matches an optional decimal point followed by one or more digits
  * `(?:[eE][+\-]?\d+)?` matches an optional exponent in scientific notation, which consists of an "e" or "E" character, an optional plus or minus sign, and one or more digits.

&NewLine;
* `extract_str(string, name)`. Similar to **extract_float()**, but returns string outputs; if the value is between commas it is returned without said commas.

* `extract_column(string, column)`. Similar to **extract_float** and **extract_str**. It can extract specific columns from a row given as **string**, with **column** being 0, 1, 2...

* `naming(string)`. This function reads the name of the folder, and returns it in the **xxx-xxx-xxx-xxx** format. Be aware that if your nested folders follow a different naming, you may want to change the **pattern** variable inside this function.

* `progressbar(current, total, start)`. This will give you an indication of whether or not you can go out and get a coffee. The Estimated Time of Arrival (ETA) is usually more reliable after 20% into the loop. The ETA will not be displayed if **start** is set to **False**. If an **ERROR** is detected, **start** would be set as **True**, and the ETA will be replaced by a warning message.  
The loop should have the following structure:

``` python
    # Start a timer and counter, for the progress bar and warning messages
    time_start = time.time()
    bar = time_start
    loop = 0
    # Loop through all the folders in the /data path
    for directory in directories:
        # Progress bar, just for fun
        loop += 1
        cr.progressbar(loop, len(directories), bar)
        ### Loopy things ###
```  

* `errorlog(error_log, errors)`. This function manages **errors**, as discussed in the *Error Management* section. For this function to work properly, the following code must be executed when saving the data rows:  

``` python

    row = [file_name, enthalpy, enthalpy_ev, a, b, c, alpha, beta, gamma, volume, density, densityg]

    # ERRORS: Check if any of the values are missing
    error = [file_name]
    for i, var in enumerate(row):
        if var is None:
            errors.append(error)
            bar = True
            if safemode == True:
                row = [file_name]
            break

    rows.append(row)
```  

* `ev_kjmol()` and `cm_ev()` are the conversion factors used to transform values from eV to kJ/mol and from cm^-1 to eV. 


Please feel free to contact me if you have any questions or suggestions.  
If you find these scripts useful, a citation would be awesome :D  
*Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader*  

