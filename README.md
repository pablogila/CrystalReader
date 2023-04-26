# CrystalReader

CrystalReader is a program to automate the reading and extraction of information from __*.castep__, __*.cif__ and __*.phonon__ files, built with the premise of reliability and ease of reuse through an easy to read code structure, with the potential to be repurposed to process any type of text-based data files.


## Requirements

CrystalReader runs in **Python 3.X** with **Pandas** installed. The use of a virtual environment such as venv is recommended, but not required. 


## CrystalReader Usage

First download the source code, as you prefer:  
* From your **web browser**  
On GitHub, clic on 'Code', 'Download ZIP', and extract.  
* Using **git**  
`git clone https://github.com/pablogila/CrystalReader.git`  

Copy the data folder(s) that you want to analyze inside this **/CrystalReader** folder. Inside your data folder there should be several nested subfolders containing your data files; the folder structure should look like this:  

```.
CrystalReader
│
├── CrystalReader.py
├── ... CrystalReader scripts ...
│
├── data_folder_1
│   ├── 000-000-000-000
│   │   ├── data_file.castep
│   │   ├── data_file.cif
│   │   └── data_file.phonon
│   ├── 270-000-000-000
│   │   └── ... data_files ...
│   ├── pnam-270-180-000-000_test
│   │   └── ...
│   ├── random_subfolder-180-270-000-090
│   │   └── ...
│   └── ...
│
├── data_folder_2
└── data_folder_3
└── ...
 ```

To execute CrystalReader, open a terminal and write:  
* On **Windows PowerShell** or **CMD**  
`python CrystalReader.py`
* On **Linux Terminal**  
`python3 CrystalReader.py`

The first time running CrystalReader, it will create an empty batch jobs file, called `CrystalReader_JOBS.txt`. Inside this file, you have to write the jobs to execute, one per line. Each job starts by the format to read (castep, cif or phonon), followed by the name of the data folder, and the name of the data files, separated by commas.  

`Format, DataFolder, DataFiles`  

The names for the output file and the error log will be generated automatically as `out/errors_DataFolder_DataFiles.csv/txt`, but you can specify them if you want to, as follows:  

`Format, DataFolder, DataFiles, Output, ErrorLog`  

An example of a job for reading phonon **rscan.phonon** files, in a folder called **data_rscan**, and writing the output to **out_rscan.csv**, and the errors to **errors_rscan.txt**, would be:  

`phonon, data_rscan, rscan.phonon, out_rscan.csv, errors_rscan.txt`  

Run CrystalReader again, and it will execute the jobs in the batch file. However, before running CrystalReader, you should modify the data header and rows from within the individual scripts, so that it only analyzes the variables that you are looking for; otherwise you may get some errors. Anyway, in case you did not read this documentation, I turned off the safemode, which discards files with errors.  

Regarding the naming of the subfolders inside your data folder, containing the data files, just know that their name will be extracted in the output file as **filename**. This naming is not relevant, just *do not use commas*.  

If your subfolders follow the xxx-xxx-xxx-xxx naming convention, but you have some comments at the folders such as __comment-*000-000-090-180*_example__, you can clean the comments and leave only the numbers, by setting `rename_files = True` inside the individual scripts.  

The following sections describe a more advanced use of these scripts. If you want to get the most out of CrystalReader, keep reading.  


## Error Management

Sometimes some of your files may be corrupted, for example if the simulation was terminated before it was completed. If a value is not found, an **ERROR** message will be displayed with information about the corrupt file(s). The rest of the variables from a suspicious file are saved by default, but be cautious, because they can be wrong: to avoid mistakes, it is best to make sure to comment the values that you know are not present in your files, as well as modify the header and row variables in the individual scripts; then you can activate the safemode by setting `safemode = True`, so that suspicious files are ignored.  

If a file takes too long to read, it is aborted and an **ERROR** message is displayed. The threshold for considering an error is defined by the variable `cry`, which is usually between 5 and 30 seconds by default, but can be set to **False** to remove the time limit. This variable may need to be changed if you are running the scripts on a supercomputer or in a potato with some wires.  

If a value is not found, an **ERROR** is displayed, regardless of whether the **cry** threshold has been reached or not, and the suspicious files are saved to an error log defined by the `error_log` variable.  

This whole section could be summarized in the following sentence: **Always check the files marked with ERRORS because they may be corrupt**.  

There are other kinds of errors, but don't worry: you will meet them when the time comes.


## Importing and Calling Scripts

CrystalReader is based on the following main scripts:  
* `cr_castep.py`, for reading **.castep** files  
* `cr_cif.py`, for reading **.cif** files  
* `cr_phonon.py`, for **.phonon** files  

You can call CrystalReader scripts from within your own Python scripts, by importing them and calling their `main()` function as follows:

```python
import cr_castep as castep
import cr_cif as cif
import cr_phonon as phonon

castep.main(data_directory='data', data_castep='cc-2.castep', out='out_castep.csv', out_error='errors_castep.txt')

cif.main(data_directory='data', data_cif='cc-2-out.cif', out='out_cif.csv', out_error='errors_cif.txt')

phonon.main(data_directory='data', data_phonon='cc-2_PhonDOS.phonon', out='out_phonon.csv', out_error='errors_phonon.txt')
```

Notice that their default values are listed above; an example for a call to read a castep file would be:  

```python
castep.main('data', 'cc-2.castep', 'out_castep.csv', 'errors_castep.txt')
```

You could also just execute the individual scripts, by previously setting `run_at_import = True`. You could then modify the individual script, and run the same call as:  

`python cr_castep.py`  

The behavior and customization of each script is explained in the following sections.  


## For **.castep** files

The `cr_castep.py` script recursively reads the castep files in the nested folders inside the `data_directory` folder. The names of the files must be set via the `data_castep` variable, for example as **cc-2.castep**, etc.  

Naming example: **data/pnam-p-1-000-000-180-000---400/cc-2.castep**  

The program iterates over this set of files, starting to read from the end of the file, and writes the relevant data to an **out_castep.csv**, line by line, on each iteration. The columns written can contain the following data:  

* name of the parent folder (in **xxx-xxx-xxx-xxx** format if `rename_files = True`)
* final enthalpy, in eV
* final enthalpy, in kJ/mol
* total energy corrected for finite basis set
* space group of crystal
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

`cr_cif.py` uses the same folder structure as before, but the files to read are set with the variables `data_cif`; its default value is `cc-2-out.cif`.  

The program iterates over this set of files and writes the relevant info to an **out_cif.csv**, containing the following data:  
* name of the parent folder, in **xxx-xxx-xxx-xxx** format
* symmetry_space_group_name_H_M


## For **.phonon** files

`cr_phonon.py` uses the same folder structure. The data files are modified via the `data_phonon` variable, and is currently set to **cc-2_Efield.phonon**.  

The program will read the 144 lines corresponding to the 144 vibration modes; this number can be changed with the `data_lines_phonon` variable.  

There is a threshold, set by the variable `threshold`, which triggers a note if one of the first 3 energies are different from zero.  

The program iterates over the set of files, and writes the following info to an **out_phonon.csv**:  

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


## Common Functions

The functions used to read the files are defined in `cr_common.py` and are imported at the beginning of each script. Some of these functions are the following:  

* `searcher(filename, search_value, time_limit=False, number_rows=0)`. This function searches for a line in the specified **filename** that starts with the string **search_value**. It starts searching from the end of the file and moves backwards until it finds a match. Once a match is found, the function returns a string with the entire line that contains the match; optionally, the function can return an array of strings, with additional lines after the match, controlled by the **number_rows** parameter. If the search takes longer than **time_limit** seconds (called as **cry** in the scripts), the function will stop searching and return **None**. If **time_limit** is not specified, the search will continue until a match is found or the entire file has been searched.  

* `extract_float(string, name)`. This function extracts the float value of a given **name** variable from a raw **string**, by searching the given string for a matching pattern as `(name + r'\s*=?\s*(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)')`, where:
  * `\s*=?\s*` matches any whitespace characters, followed by an optional equals sign, followed by any whitespaces
  * `-?` matches an optional minus sign
  * `\d+` matches one or more digits
  * `(?:\.\d+)?` matches an optional decimal point followed by one or more digits
  * `(?:[eE][+\-]?\d+)?` matches an optional exponent in scientific notation, which consists of an "e" or "E" character, an optional plus or minus sign, and one or more digits  

&NewLine;
* `extract_str(string, name)`. Similar to **extract_float()**, but returns string outputs.  

* `extract_str_commas(string, name)`. Similar to **extract_str()**, for when the string has commas: `" '`.  

* `extract_column(string, column)`. Similar to **extract_float** and **extract_str**. It can extract specific columns from a row given as **string**, with **column** being 0, 1, 2...  

* `naming(string)`. This function reads the name of the folder, and returns it in the **xxx-xxx-xxx-xxx** format. Be aware that if your nested folders follow a different naming, you may want to change the **pattern** variable inside this function. However, by default this function is not used, since the variable `rename_files` is set to **False**; by setting it to **True** the filenames would be renamed in this convention.  

* `progressbar(current, total, start=False)`. This will give you an indication of whether or not you can go out and get a coffee. The Estimated Time of Arrival (ETA) is usually more reliable after 20% into the loop. The ETA will not be displayed if **start** is set to **False**, and since it is its default value, it can be called as `progressbar(current, total)`. If an **ERROR** is detected, **start** would be set as **True**, and the ETA will be replaced by a warning message.  
To call the progressbar function, the main loop should have the following structure:

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

* `errorlog(error_log, errors)`. This function manages **errors** for missing variables, as discussed in the *Error Management* section. For this function to work properly, the following code must be executed when saving the data rows:  

``` python

    # row = [file_name, enthalpy, enthalpy_ev, a, b, c, alpha, beta, gamma, volume, density, densityg]

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

* `jobs(job_file)`. Reads the batch job file and executes the listed jobs, or creates an empty template for this job file if it is not found.

* `ev_kjmol()` and `cm_ev()` are the conversion factors used to transform values from eV to kJ/mol and from cm^-1 to eV.  


Please feel free to contact me if you have any questions or suggestions.  
If you find these scripts useful, a citation would be awesome :D  
*Gila-Herranz, Pablo. “CrystalReader”, 2023. https://github.com/pablogila/CrystalReader*  

