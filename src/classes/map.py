from .entity import Entity
from .road_node import RoadNode
class Map(Entity):

    def __init__(self):
        self.nodes = []