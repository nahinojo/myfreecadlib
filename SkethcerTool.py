import FreeCAD as App
import Part
import Sketcher


def _recomputeApp() -> None:
        App.ActiveDocument.recompute()
        return


def _validLineSegment(line_segment):
    if type(line_segment) is not Part.LineSegment:
        raise TypeError("Not 'Part.LineSegment' type")
    else:
        return line_segment


def _validCoordinate(coord: tuple) -> tuple:
    if type(coord) != tuple:
        raise TypeError("Not 'tuple' type")
    length = len(coord)
    if length == 3:
        return coord
    elif length == 2:
        return (coord[0], coord[1], 0)
    else:
        raise ValueError("Coordinate must have size 2 or 3")


def _extractLineSegmentData(line_segment) -> None:
    """
    Generates coordinate endpoints of given line segment.
    """
    _validLineSegment(line_segment)
    line_segment = str(line_segment)
    line_segment = line_segment[
        line_segment.find('t') + 2: line_segment.find('>') - 1
    ].split(' ')
    line_coords = []
    for val in line_segment:
        val = val.replace(')','').replace('(','').split(',')
        val = tuple([float(n) for n in val])
        line_coords.append(val)
    return line_coords
        

class SketcherTool:


    def __init__(self, sketch) -> None:
        self.sketch = sketch
        return
    
    def addLine(
            self, 
            coordinate_1: tuple,
            coordinate_2: tuple,
            recompute: bool = True
    ) -> None:
        """
        Adds line between specified coordinates.
        """
        self.sketch.addGeometry(
            Part.LineSegment(
                App.Vector(*coordinate_1, 0),
                App.Vector(*coordinate_2, 0)
            ), False
        )
        if recompute:
            _recomputeApp()
        return

    def addCircle(
            self, 
            coordinate, 
            radius
    ) -> None:
        """
        Adds circle to sketch at specified coordinate.
        """        
        self.sketch.addGeometry(
            Part.Circle(
                App.Vector(*coordinate),
                App.Vector(0,0,1),
                radius
            ),
            False)
        _recomputeApp()
        return

    def addRectangle(
            self, 
            coordinate, 
            x_len, 
            y_len, 
            location = 'X'
    ) -> None:
        """
        Adds rectangle to sketch on xy-plane at specified coordinate. 

        The coordinates' relative location may be further specified.

        A --- B --- C
        |           
        |           
        H     X     D
        |           
        |           
        G     F     E 

        Inputted location 'loc' dictates this relation. 
        """
        location = location.upper()
        if location not in {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'X'}:
            raise ValueError("Invalid location inputted")
        
        if location in {'A', 'H', 'G'}:
            x0 = coordinate[0] 
            x1 = coordinate[0] + x_len
        elif location in {'B', 'X', 'F'}:
            x0 = coordinate[0] - (x_len/2)
            x1 = coordinate[0] + (x_len/2)
        else:
            x0 = coordinate[0] - x_len
            x1 = coordinate[0] 
        if location in {'G', 'F', 'E'}:
            y0 = coordinate[1] 
            y1 = coordinate[1] + y_len
        elif location in {'H', 'X', 'D'}:
            y0 = coordinate[1] - (y_len/2)
            y1 = coordinate[1] + (y_len/2)
        else:
            y0 = coordinate[1] - y_len
            y1 = coordinate[1] 
        P1 = [x1, y1]
        P2 = [x0, y1]
        P3 = [x0, y0]
        P4 = [x1, y0]
        num_lines = [
            str(i)[1:13] for i in self.sketch.Geometry
        ].count("Line segment")

        geo_list = []
        geo_list.append(Part.LineSegment(App.Vector(*P3, 0),App.Vector(*P4, 0)))
        geo_list.append(Part.LineSegment(App.Vector(*P4, 0),App.Vector(*P1, 0)))
        geo_list.append(Part.LineSegment(App.Vector(*P1, 0),App.Vector(*P2, 0)))
        geo_list.append(Part.LineSegment(App.Vector(*P2, 0),App.Vector(*P3, 0)))
        self.sketch.addGeometry(geo_list,False)
        con_list = []
        con_list.append(Sketcher.Constraint('Coincident',num_lines,2,num_lines+1,1))
        con_list.append(Sketcher.Constraint('Coincident',num_lines+1,2,num_lines+2,1))
        con_list.append(Sketcher.Constraint('Coincident',num_lines+2,2,num_lines+3,1))
        con_list.append(Sketcher.Constraint('Coincident',num_lines+3,2,num_lines,1))
        con_list.append(Sketcher.Constraint('Horizontal',num_lines))
        con_list.append(Sketcher.Constraint('Horizontal',num_lines+2))
        con_list.append(Sketcher.Constraint('Vertical',num_lines+1))
        con_list.append(Sketcher.Constraint('Vertical',num_lines+3))
        self.sketch.addConstraint(con_list)
        
        _recomputeApp()
        return
        
        
    def sliceLine(
            self, 
            line_index: int,
            coord: tuple, 
    ) -> None:
        """
        Splits line into segments at specified coordinates.
        """
        midd_coord = _validCoordinate(coord)
        line_segment = _validLineSegment(self.sketch.Geometry[line_index])
        line_coord_1,line_coord_2 = _extractLineSegmentData(line_segment)
        slope_1 = (midd_coord[1] - line_coord_1[1])/(midd_coord[0] - line_coord_1[0])
        slope_2 = (midd_coord[1] - line_coord_2[1])/(midd_coord[0] - line_coord_2[0])
        
        if abs(slope_1 - slope_2) < .000001:
            proper_coord = True
        else:
            # Numerical Analysis Here
            pass
                
        print("slope 1:", slope_1)
        print("slope 2:", slope_2)
        return
        
        self.addLine(line_coord_1, midd_coord)
        self.addLine(midd_coord, line_coord_2)
        
        _recomputeApp()
        return
    