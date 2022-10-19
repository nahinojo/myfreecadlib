import FreeCAD as App
import Part
import Sketcher


class SketcherTool:
    
    def __init__(self, sketch) -> None:
        self.sketch = sketch
        return 
    
    def _recomputeApp() -> None:
        App.ActiveDocument.recompute()
        return
        
    def _extractLineSegmentData(self) -> None:
        """
        Generates list coordinate pairs for each line segment in the sketch.
        """
        line_coords_list = [
            val for val in self.sketch.Geometry if 'Line segment' in val
        ]
        # Extracts only (x,y,z) coordinates as strings from list.
        line_coords_list = [
            str(c)[
                str(c).find('t') + 2:str(c).find('>') - 1
            ].split(' ') for c in line_coords_list
        ]
        self.line_coords = []
        for line_coords in line_coords_list:
            new_coord = []
            for lc in line_coords:
                lc = lc.replace(')','').replace('(','').split(',')
                lc = tuple([float(n) for n in lc])
                new_coord.append(lc)
            self.line_coords.append(new_coord)
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
            SketcherTool._recomputeApp()
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
        self._recomputeApp()
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
        
        SketcherTool._recomputeApp()
        return
        
        
    def sliceLine(
            self, 
            line_index: int, 
            coordinate: tuple, 
            symmetrical: bool = False
    ) -> None:
        """
        Splits line into segments at specified coordinates.
        
        Parameters
        ----------
        line: int
            The index of the line to be sliced. The line's index is noted
            in the Sketcher's 'Elements' tab. 
        coord: tuple
            The x and y coordinate to slice the line. Must be a real number
            formatted as (x, y). 
        symmetry: boolean, optional.
            If True, slicing will be mirrored actoss
        """

        SketcherTool._recomputeApp()
        return
    