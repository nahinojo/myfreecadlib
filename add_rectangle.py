"""
Adds rectangle to target sketch.

Inputs:
    - x-coordinate of center of rectangle. 
    - x-axis length.
    - y-coordinate of center of rectangle.
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

print("Please input the rectangle's coordinates")
print("in the form {x_coord, y_coord, x_len, y_len }")
print("separated by commas.\n")
coords = input()
coords = coords.replace(" ","")
coords = coords.split(",")
coords = [float(i) for i in coords]
print("x-coordinate: " + str(coords[0]))
print("y-coordinate: " + str(coords[1]))
print("x-length: " + str(coords[2]))
print("y-length: " + str(coords[3]) + '\n')

P1 = [coords[0] + (coords[2]/2), coords[1] + (coords[3]/2), 0]
P2 = [coords[0] - (coords[2]/2), coords[1] + (coords[3]/2), 0]
P3 = [coords[0] - (coords[2]/2), coords[1] - (coords[3]/2), 0]
P4 = [coords[0] + (coords[2]/2), coords[1] - (coords[3]/2), 0]
numLines = [
    str(i)[1:13] for i in target_sketch.Geometry
].count("Line segment")

# Generating line segments in FreeCAD's sketcher
geoList = []
geoList.append(Part.LineSegment(App.Vector(*P3),App.Vector(*P4)))
geoList.append(Part.LineSegment(App.Vector(*P4),App.Vector(*P1)))
geoList.append(Part.LineSegment(App.Vector(*P1),App.Vector(*P2)))
geoList.append(Part.LineSegment(App.Vector(*P2),App.Vector(*P3)))
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