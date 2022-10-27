import FreeCAD as App
import Part
import Sketcher


def _refreshApp() -> None:
        App.ActiveDocument.recompute()
        return


def _validLineSegment(line_segment):
    if type(line_segment) is not Part.LineSegment:
        raise TypeError("Not 'Part.LineSegment' type")
    else:
        return line_segment


def _validCoordinate(coord: tuple) -> tuple:
    if type(coord) != tuple:
        raise TypeError("Coordinate must be 'tuple' type")
    if (len(coord) != 3) and (len(coord) != 2):
        raise ValueError(
            "Coordinate must have size 2 or 3"
        )
    else:
        return (coord[0], coord[1], 0)

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


    def __init__(self, 
                 sketch
    ) -> None:
        self.sketch = sketch
        return
    
    def getLineSegmentData (self) -> list:
        data = []
        for element in self.sketch.Geometry:
            if "Line segment" in str(element):
                data.append(_extractLineSegmentData(element))
        return data
        
    
    def addPoint(self,
                 x: int or float or tuple,
                 y: int or float = None,
                 refresh: bool = True,
    ) -> None:
        """
        Adds point at specified coordinate
        """
        if type(x) is tuple:
            coord = x
        else:
            coord = (x, y)
        coord = _validCoordinate(coord)
        App.ActiveDocument.Sketch.addGeometry(Part.Point(App.Vector(*coord)))
        if refresh: _refreshApp()
        return
    
    def constrainCoincident(self,
                            x: int or float or tuple,
                            y: int or float = None,
                            refresh: bool = True, 
    ) -> None:
        if type(x) is tuple:
            coord = x
        else:
            coord = (x, y)
        coord = _validCoordinate(coord)
        
        match_indeces = []
        for i, line_coords in enumerate(self.getLineSegmentData()):
            for j, lc in enumerate(line_coords):
                if lc == coord:
                    match_indeces.append((i, j + 1))
        
        if len(match_indeces) > 1:
            for i in range(len(match_indeces) - 1):
                self.sketch.addConstraint(
                    Sketcher.Constraint(
                        'Coincident',
                        *match_indeces[i],
                        *match_indeces[i + 1]
                    )
                )

        if refresh: _refreshApp()
        return
        
    def addLine(self, 
                coord_1: tuple,
                coord_2: tuple,
                coincident: bool = False,
                refresh: bool = True
    ) -> None:
        """
        Adds line between specified coordinates.
        """
        coord_1 = _validCoordinate(coord_1)
        coord_2 = _validCoordinate(coord_2)
        self.sketch.addGeometry(
            Part.LineSegment(
                App.Vector(*coord_1),
                App.Vector(*coord_2)
            ), False
        )
        if coincident:
            line_data = self.getLineSegmentData()
            for i, coord_pair in enumerate(line_data[:-1]):
                if coord_1 in coord_pair:
                    self.sketch.addConstraint(Sketcher.Constraint(
                        'Coincident', 
                        len(line_data) - 1,
                        1,
                        i,
                        coord_pair.index(coord_1) + 1
                    ))
                if coord_2 in coord_pair:
                    self.sketch.addConstraint(Sketcher.Constraint(
                        'Coincident', 
                        len(line_data) - 1,
                        2,
                        i,
                        coord_pair.index(coord_2) + 1
                    ))
        if refresh: _refreshApp()
        return

    def addCircle(self, 
                  coordinate: tuple, 
                  radius: float or int,
                  refresh: bool = True
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
        if refresh: _refreshApp()
        return

    def addRectangle(self, 
                     coord: tuple, 
                     x_len: float or int, 
                     y_len: float or int, 
                     relative_location: str = 'X',
                     refresh: bool = True
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
        relative_location = relative_location.upper()
        if relative_location not in {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'X'}:
            raise ValueError("Invalid location inputted")
        
        if relative_location in {'A', 'H', 'G'}:
            x0 = coord[0] 
            x1 = coord[0] + x_len
        elif relative_location in {'B', 'X', 'F'}:
            x0 = coord[0] - (x_len/2)
            x1 = coord[0] + (x_len/2)
        else:
            x0 = coord[0] - x_len
            x1 = coord[0] 
        if relative_location in {'G', 'F', 'E'}:
            y0 = coord[1] 
            y1 = coord[1] + y_len
        elif relative_location in {'H', 'X', 'D'}:
            y0 = coord[1] - (y_len/2)
            y1 = coord[1] + (y_len/2)
        else:
            y0 = coord[1] - y_len
            y1 = coord[1] 
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
        con_list.append(Sketcher.Constraint('Coincident', num_lines, 2, num_lines + 1, 1))
        con_list.append(Sketcher.Constraint('Coincident', num_lines + 1, 2, num_lines + 2, 1))
        con_list.append(Sketcher.Constraint('Coincident', num_lines + 2, 2,num_lines + 3, 1))
        con_list.append(Sketcher.Constraint('Coincident', num_lines + 3, 2,num_lines, 1))
        con_list.append(Sketcher.Constraint('Horizontal', num_lines))
        con_list.append(Sketcher.Constraint('Horizontal', num_lines + 2))
        con_list.append(Sketcher.Constraint('Vertical', num_lines + 1))
        con_list.append(Sketcher.Constraint('Vertical', num_lines + 3))
        self.sketch.addConstraint(con_list)
        
        if refresh: _refreshApp()
        return
        
        
    def sliceLine(self, 
                  line_index: int,
                  coord: tuple,
                  coincident: bool = False,
                  refresh: bool = True
    ) -> None:
        """
        Splits line into segments at specified coordinates.
        """
        coord_slice = _validCoordinate(coord)
        line_segment = _validLineSegment(self.sketch.Geometry[line_index - 1])
        line_coord_1, line_coord_2 = _extractLineSegmentData(line_segment)
        slope_1 = (coord_slice[1] - line_coord_1[1])/(coord_slice[0] - line_coord_1[0])
        slope_2 = (coord_slice[1] - line_coord_2[1])/(coord_slice[0] - line_coord_2[0])
        
        if abs(slope_1 - slope_2) >= .000001:
            # Approximates the coordinate on line_segment closest to coord_slice.
            coord_a = line_coord_1
            coord_b = line_coord_2
            length_a = (
                (coord_a[0] - coord_slice[0])**2 
                + (coord_a[1] - coord_slice[1])**2
            )
            length_b = (
                (coord_b[0] - coord_slice[0])**2 
                + (coord_b[1] - coord_slice[1])**2
            )
            while abs(length_a - length_b) >= .000005:
                coord_mid = (
                    (coord_a[0] + coord_b[0])/2,
                    (coord_a[1] + coord_b[1])/2
                )
                if length_a > length_b:
                    coord_a = coord_mid
                    length_a = (
                        (coord_a[0] - coord_slice[0])**2 
                        + (coord_a[1] - coord_slice[1])**2
                    )
                else:
                    coord_b = coord_mid
                    length_b = (
                        (coord_b[0] - coord_slice[0])**2 
                        + (coord_b[1] - coord_slice[1])**2
                    )
            coord_slice = coord_mid
        
        self.addLine(line_coord_1, coord_slice, False)
        self.addLine(coord_slice, line_coord_2, False)
        if coincident: 
            self.sketch.addConstraint(Sketcher.Constraint(
                'Coincident',
                len(self.sketch.Geometry) - 2,
                2,
                len(self.sketch.Geometry) - 1,
                1
            ))
        self.sketch.delGeometry(line_index - 1)
        if refresh: _refreshApp()
        return
    