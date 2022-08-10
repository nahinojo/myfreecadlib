import FreeCAD as App
import Part
import Sketcher


def AddCircle(sketch, x, y, radius):
    """
    Adds circle to sketch at specified coordinate.
    """
    sketch.addGeometry(
        Part.Circle(
            App.Vector(x,y,0),
            App.Vector(0,0,1),
            radius),
        False)
    App.ActiveDocument.recompute()
    return


def AddRectangle(sketch, x, y, x_len, y_len, loc = 'X'):
    """
    Adds rectangle to sketch at specified coordinate. 

    The coordinates' relative location may be further specified.

    A --- B --- C
    |           |
    |           |
    H     X     D
    |           |
    |           |
    G --- F --- E 

    Inputted location 'loc' dictates this relation. 
    """

    if loc not in {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'X'}:
        print("Location specified is invalid")
        return
    
    if loc in {'A', 'H', 'G'}:
        x0 = x 
        x1 = x + x_len
    elif loc in {'B', 'X', 'F'}:
        x0 = x - (x_len/2)
        x1 = x + (x_len/2)
    else:
        x0 = x - x_len
        x1 = x 

    if loc in {'G', 'F', 'E'}:
        y0 = y 
        y1 = y + y_len
    elif loc in {'H', 'X', 'D'}:
        y0 = y - (y_len/2)
        y1 = y + (y_len/2)
    else:
        y0 = y - y_len
        y1 = y 
    
    P1 = [x1, y1]
    P2 = [x0, y1]
    P3 = [x0, y0]
    P4 = [x1, y0]

    numLines = [
        str(i)[1:13] for i in sketch.Geometry
    ].count("Line segment")

    # Generating line segments in FreeCAD's sketcher
    geoList = []
    geoList.append(Part.LineSegment(App.Vector(*P3, 0),App.Vector(*P4, 0)))
    geoList.append(Part.LineSegment(App.Vector(*P4, 0),App.Vector(*P1, 0)))
    geoList.append(Part.LineSegment(App.Vector(*P1, 0),App.Vector(*P2, 0)))
    geoList.append(Part.LineSegment(App.Vector(*P2, 0),App.Vector(*P3, 0)))
    sketch.addGeometry(geoList,False)

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
    sketch.addConstraint(conList)
    
    App.ActiveDocument.recompute()