from .entity import Entity
from .vector2 import Vector2
from pygame import draw

JUNCTION_RADIUS = 1
class Junction(Entity):

    def __init__(self, pos: Vector2):
        self.position = pos
        self.connections = []
        self.connection_matrices = []

    def connect(self, connector):        
        self.connections.append(connector)