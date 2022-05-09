from enum import Enum

class LengthType(Enum):
    INFINITE_BIDIRECTIONAL = 1,
    INFINITE_UNIDIRECTIONAL = 2,
    FINITE = 3

class Length:
    def __init__(self, length_type, value=None):
        self._length_type = length_type
        self._value = value

    @property
    def value(self):
        if self._length_type == LengthType.FINITE:
            return self._value
        else:
            raise RuntimeError("Cannot get length value of non-finite length")

    @property
    def type(self):
        return self._length_type

class LineSegment:
    def __init__(self, origin, direction, length):
        self.origin = origin
        self.direction = direction
        self.length = length

    def plane_intersection(self, plane_normal):
        

class Region:
    def __init__(self):
        self.type = 
