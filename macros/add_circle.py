"""
Adds circle to target sketch.

Inputs:
 - x-coordinate of center
 - y-coordinate of center
 - radius of circle. 
"""

print("Initializing Macro...\n")
try:
    target_sketch
except:
    raise NameError(
        "Please define target sketch as 'target_sketch' using FreeCAD's"
        + "python console. Then, re-execute this macro."
    )

print(
    "Please input the circles coordinates"
    + "in the form {x_coord, y_coord, radius}"
    + "separated by commas.\n"
)
vals = input()
vals = vals.replace(" ","")
vals = vals.split(",")
vals = [float(i) for i in vals]
print("x-coordinate: " + str(vals[0]))
print("y-coordinate: " + str(vals[1]))
print("radius: "+ str(vals[2]) + '\n')

# Appending circle using FreeCAD's syntax. 
target_sketch.addGeometry(
    Part.Circle(
        App.Vector(vals[0],vals[1],0),
        App.Vector(0,0,1),
        vals[2]),
    False)
App.ActiveDocument.recompute()
print("Circle Generated!")