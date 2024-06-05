from .entity import Entity
from .connector import Connector

class RoadSegment(Entity):

    def __init__(self, j_from: Connector, j_to: Connector):        
        self.from_connector = j_from
        self.to_connector = j_to

        