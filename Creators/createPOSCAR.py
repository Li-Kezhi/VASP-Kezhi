# Create POSCAR
from vaspy.matstudio import XsdFile

file = raw_input("Enter the .xsd file name:")
if ".xsd" not in file:
    file += ".xsd"

xsd = XsdFile(filename=file)
poscar_content = xsd.get_poscar_content(bases_const=1.0)
with open('POSCAR', 'w') as f:
    f.write(poscar_content)