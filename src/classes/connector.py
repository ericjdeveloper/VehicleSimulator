from .entity import Entity
from .vector2 import Vector2
from .road_node import RoadNode

CONNECTOR_RADIUS = 1
class Connector(Entity):

    def __init__(self, connections=[]):
        self.connections = connections
        self.connection_matrices = []

    @property
    def position(self):
        x = sum(f.position.x for f in self.connections) / len(self.connections)
        y = sum(f.position.y for f in self.connections) / len(self.connections)
        return Vector2(x,y).intify()

    def connect(self, node: RoadNode):        
        self.connections.append(node)

    def disconnect(self, node: RoadNode):
        return self.connections.Remove(node)
