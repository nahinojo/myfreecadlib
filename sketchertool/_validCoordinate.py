def _validCoordinate(coord: tuple) -> tuple:
    """
    Ensures provided coordinate is properly formatted.
    """
    if type(coord) != tuple:
        raise TypeError("Coordinate must be 'tuple' type")
    if (len(coord) != 3) and (len(coord) != 2):
        raise ValueError(
            "Coordinate must have size 2 or 3"
        )
    else:
        return (coord[0], coord[1], 0)