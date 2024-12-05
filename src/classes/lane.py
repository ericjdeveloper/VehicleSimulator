from .enums import Direction
from .vector2 import Vector2

class Lane:

    DEFAULT_LANE_WIDTH=15

    def __init__(self, parent, index, direction, width=DEFAULT_LANE_WIDTH):
        self.parent = parent
        self.index = index
        self.direction = direction
        self.width = width

    @property
    def slope(self):
        return ((self.parent.connection.get_position() + self.parent.connection.get_lane_offset(self.index, Direction.OUT)) - (self.parent.get_position() + self.parent.get_lane_offset(self.index, Direction.IN))).normalized()

    def get_projection(self, point: Vector2, bFacing=False):

        pp = self.get_position()
        proj = Vector2.Dot(point - pp, self.slope)
        proj += bFacing * dir        

        return pp + self.slope * (proj)
    

    def get_position(self):
        return self.parent.get_offset_position() - self.parent.get_lane_offset(self.index, self.direction)

class LaneBorder:

    def __init__(self):
        lane_type = None