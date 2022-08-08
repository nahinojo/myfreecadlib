"""
Adds a circle to sketch based on inputted coordinates. 
"""
print("Initializing Macro...\n")
try:
    target_sketch
except:
    raise NameError(
        "Please define target sketch as 'target_sketch'" 
        + "using FreeCAD's python console."
    )

print("Please input the circles coordinates")
print("in the form [x_coord, y_coord, radius]")
print("separated by commas.\n")
coords = input()
coords = coords.replace(" ","")
coords = coords.split(",")
coords = [float(i) for i in coords]
print("x-coordinate: " + str(coords[0]))
print("y-coordinate: " + str(coords[1]))
print("radius: "+ str(coords[2]) + '\n')

target_sketch.addGeometry(
    Part.Circle(
        App.Vector(coords[0],coords[1],0),
        App.Vector(0,0,1),
        coords[2]),
    False)
App.ActiveDocument.recompute()

print("Circle Generated!")