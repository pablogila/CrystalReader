"""
CrystalReader Launcher. Read and extract data from different files.
Copyright (C) 2023  Pablo Gila-Herranz
Check the latest version at https://github.com/pablogila/CrystalReader
Feel free to contact me at pablo.gila.herranz@gmail.com

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


import cr_common as cr
import cr_castep as castep
import cr_cif as cif
import cr_phonon as phonon
import time


print("\n")
print("  Welcome to CrystalReader version " + cr.version())
print("  This is free software, and you are welcome to redistribute it under GNU General Public License")
print("  You should have already configured the batch job and the corresponding scripts")
print("  Else check the documentation on https://github.com/pablogila/CrystalReader")
print("")
print("  Conversion factors:")
print("  cm^-1 to eV =", cr.cm_ev())
print("  eV to kJ/mol =", cr.ev_kjmol())
print("")
time_start = time.time()


##############################################################
#             EXAMPLES FOR CALLING THE SCRIPTS
##############################################################
# Default values are listed in the examples.
# Other parameters can be modified from within the scripts.
#
# castep.main(data_directory='data', data_castep='cc-2.castep', out='out_castep.csv', out_error='errors_castep.txt')
# cif.main(data_directory='data', data_cif='cc-2-out.cif', out='out_cif.csv', out_error='errors_cif.txt')
# phonon.main(data_directory='data', data_phonon='cc-2_PhonDOS.phonon', out='out_phonon.csv', out_error='errors_phonon.txt')
##############################################################



cif.main('data_PBEsol-MP-2x2x2', 'cc-2-out.cif', 'out_cif_PBEsol-MP-2x2x2.csv', 'errors_cif_PBEsol-MP-2x2x2.txt')
#cif.main('data_PBEsol-MP-2x2x2', 'cc-2_Efield-out.cif', 'out_cif-Efield_PBEsol-MP-2x2x2.csv', 'errors_cif-Efield_PBEsol-MP-2x2x2.txt')

castep.main('data_pbe-d3', 'cc-2_PhonDOS.castep', 'out_castep_pbe-d3.csv', 'errors_castep_pbe-d3.txt')
#castep.main('data_pbe-ts', 'cc-2_PhonDOS.castep', 'out_castep_pbe-ts.csv', 'errors_castep_pbe-ts.txt')
#castep.main('data_rscan', 'cc-2_PhonDOS.castep', 'out_castep_rscan.csv', 'errors_castep_rscan.txt')

phonon.main('data_pbe-d3', 'cc-2_PhonDOS.phonon', 'out_phonon_pbe-d3.csv', 'errors_phonon_pbe-d3.txt')
#phonon.main('data_pbe-ts', 'cc-2_PhonDOS.phonon', 'out_phonon_pbe-ts.csv', 'errors_phonon_pbe-ts.txt')
#phonon.main('data_rscan', 'cc-2_PhonDOS.phonon', 'out_phonon_rscan.csv', 'errors_phonon_rscan.txt')



print("")
print("  All jobs finished in", round(time.time() - time_start, 2), "seconds\n")
print("")

