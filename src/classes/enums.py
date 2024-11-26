from enum import IntEnum

class Alignments(IntEnum):
    INNER=-1
    CENTER=0
    OUTER=1

class Direction(IntEnum):
    OUT=1
    IN=-1

    def opposite(self):
        return self * -1