import Part

def _validLineSegment(line_segment):
    """
    Ensures provided line segment is proper type
    """
    if type(line_segment) is not Part.LineSegment:
        raise TypeError("Not 'Part.LineSegment' type")
    else:
        return line_segment