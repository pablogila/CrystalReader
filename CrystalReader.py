"""
CrystalReader Launcher. Read and extract data from simulation files.
Copyright (C) 2023  Pablo Gila-Herranz

If you find this code useful, a citation would be greatly appreciated :D
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

version = "vCR.2023.03.14.2400"

import time
import cr_common as cr

print("\n")
print("  Welcome to CrystalReader version " + version)
print("  This is free software, and you are welcome to redistribute it under GNU General Public License")
print("  You should have already introduced the files to read in the corresponding scripts")
print("  Else check the documentation on https://github.com/pablogila/CrystalReader")
print("")
print("  Conversion factors:")
print("  cm^-1 to eV =", cr.cm_ev())
print("  eV to kJ/mol =", cr.ev_kjmol())
print("")
print("  Enter which files would you like to read:")
print("  1.  *.castep")
print("  2.  *.cif")
print("  3.  *.phonon")
print("  4.  ALL")
print("")
choice = input("  > ")
if choice == "1" or choice == "castep" or choice == "CASTEP":
    print("  Reading 'castep' files...\n")
    import cr_castep
elif choice == "2" or choice == "cif" or choice == "CIF":
    print("  Reading 'cif' files...\n")
    import cr_cif
elif choice == "3" or choice == "phonon" or choice == "PHONON":
    print("  Reading 'phonon' files...\n")
    import cr_phonon
elif choice == "4" or choice == "all" or choice == "ALL":
    print("  Reading all files...\n")
    time_all = time.time()
    import cr_cif
    import cr_castep
    import cr_phonon
    print("\n  All files read in", round(time.time() - time_all, 2), "seconds\n")
else:
    print("")
    print("  Invalid input. Please try again.")
print("")

