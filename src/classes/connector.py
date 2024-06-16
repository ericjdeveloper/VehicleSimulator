from .entity import Entity
from .vector2 import Vector2
from .road_node import RoadNode

CONNECTOR_RADIUS = 1
class Connector(Entity):


    def __init__(self, nodes):
        self.nodes = nodes
        for i in range(len(nodes)): 
            self.connect(nodes[i])
        self.connection_matrices = []

    @property
    def position(self):
        x = sum(f.position.x for f in self.nodes) / len(self.nodes)
        y = sum(f.position.y for f in self.nodes) / len(self.nodes)
        return Vector2(x,y).intify()

    def connect(self, node: RoadNode):        
        self.nodes.append(node)

    def connect_lane(self, lane, connections=[]):
        id = self.nodes.index(lane.parent)
        ids = [self.nodes.index(connections[c].parent) for c in connections]
        self.connections[id] = ids