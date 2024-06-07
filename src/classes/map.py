from .entity import Entity
from .road_node import RoadNode
from .connector import Connector

class Map(Entity):

    def __init__(self):
        self.nodes = []
        self.connectors = []