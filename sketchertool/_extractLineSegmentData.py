from ._validLineSegment import _validLineSegment

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