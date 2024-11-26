from .enums import Direction
from .vector2 import Vector2

class Lane:

    DEFAULT_LANE_WIDTH=15

    def __init__(self, parent, index, width=DEFAULT_LANE_WIDTH):
        self.parent = parent
        self.index = index
        self.width = width

    @property
    def slope(self):
        return ((self.parent.connection.get_position() + self.parent.connection.get_lane_offset(self.index, Direction.OUT)) - (self.parent.get_position() + self.parent.get_lane_offset(self.index, Direction.IN))).normalized()

    def get_projection(self, point: Vector2, dir=Direction.OUT, bFacing=False):

        pp = self.parent.get_position() + self.parent.get_lane_offset(self.index, dir)
        proj = Vector2.Dot(point - pp, self.slope)
        proj += bFacing * dir        

        return pp + self.slope * (proj)
        

class LaneBorder:

    def __init__(self):
        lane_type = None