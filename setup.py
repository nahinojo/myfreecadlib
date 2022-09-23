import sys

path_to_mfc = input(
    "Please input the parent folder containing myfreecadlib: \n"
).replace(" ","'")

sys.path.append(path_to_mfc)
print("Path successfully appended!")
print("You may now import myfreecadlib using FreeCAD's Python console.")
