"""
Adds rectangle to target sketch.

Inputs:
    - x-coordinate. 
    - x-axis length.
    - y-coordinate.
    - y-axis length.
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
    "Please input the rectangle's coordinates in \n"
    + "the form {x_coord, y_coord, x_len, y_len } \n"
    + "separated by commas.\n"
)
vals = input()
vals = vals.replace(" ","")
vals = vals.split(",")
vals = [float(i) for i in vals]
print(
    "x-coordinate: " + str(vals[0]) + "\n"
    + "y-coordinate: " + str(vals[1]) + "\n"
    + "x-length: " + str(vals[2]) + "\n"
    + "y-length: " + str(vals[3]) + '\n'
)

while True:
    print(
    "Where is the coordinate (" 
    + str(vals[0]) 
    +", "
    + str(vals[1])
    +") relative to the rectangle?\n\n"
    + "A --- B --- C\n"
    + 2*"|                      |\n"
    + "H --- X --- D\n"
    + 2*"|                      |\n"
    + "G --- F --- E\n"
    )
    response = input().upper()
    if response not in {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'X'}:
        print("Not a valid location.")
    else:
        break

if response in {'A', 'H', 'G'}:
    x0 = vals[0] 
    x1 = vals[0] + vals[2]
elif response in {'B', 'X', 'F'}:
    x0 = vals[0] - (vals[2]/2)
    x1 = vals[0] + (vals[2]/2)
else:
    x0 = vals[0] - vals[2]
    x1 = vals[0] 

if response in {'G', 'F', 'E'}:
    y0 = vals[1] 
    y1 = vals[1] + vals[3]
elif response in {'H', 'X', 'D'}:
    y0 = vals[1] - (vals[3]/2)
    y1 = vals[1] + (vals[3]/2)
else:
    y0 = vals[1] - vals[3]
    y1 = vals[1] 


P1 = [x1, y1]
P2 = [x0, y1]
P3 = [x0, y0]
P4 = [x1, y0]
numLines = [
    str(i)[1:13] for i in target_sketch.Geometry
].count("Line segment")


print("x0: ", x0)
print("x1: ", x1)
print("y0: ", y0)
print("y1: ", y1)
print("P1: ",P1)
print("P2: ",P2)
print("P3: ",P3)
print("P4: ",P4)
print("numLines: ", numLines)

# Generating line segments in FreeCAD's sketcher
geoList = []
geoList.append(Part.LineSegment(App.Vector(*P3, 0),App.Vector(*P4, 0)))
geoList.append(Part.LineSegment(App.Vector(*P4, 0),App.Vector(*P1, 0)))
geoList.append(Part.LineSegment(App.Vector(*P1, 0),App.Vector(*P2, 0)))
geoList.append(Part.LineSegment(App.Vector(*P2, 0),App.Vector(*P3, 0)))
target_sketch.addGeometry(geoList,False)

# Connecting line segments using FreeCAD Coincident Constraints.
conList = []
conList.append(Sketcher.Constraint('Coincident',numLines,2,numLines+1,1))
conList.append(Sketcher.Constraint('Coincident',numLines+1,2,numLines+2,1))
conList.append(Sketcher.Constraint('Coincident',numLines+2,2,numLines+3,1))
conList.append(Sketcher.Constraint('Coincident',numLines+3,2,numLines,1))

# Line segments must be parallel with corresponding x and y axes. 
conList.append(Sketcher.Constraint('Horizontal',numLines))
conList.append(Sketcher.Constraint('Horizontal',numLines+2))
conList.append(Sketcher.Constraint('Vertical',numLines+1))
conList.append(Sketcher.Constraint('Vertical',numLines+3))
target_sketch.addConstraint(conList)
App.ActiveDocument.recompute()

print("Rectangle Generated!")