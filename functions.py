import FreeCAD as App
import Part

def AddCircle(sketch, x, y, radius):
    sketch.addGeometry(
        Part.Circle(
            App.Vector(x,y,0),
            App.Vector(0,0,1),
            radius),
        False)
    App.ActiveDocument.recompute()
    return