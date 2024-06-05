from .entity import Entity
from .connector import Connector
from .road_segment import RoadSegment

class Map(Entity):

    def __init__(self):
        self.segments = []
        self.connectors = []
        self.junctions = []

    def get_segments_by_connector(self, connector: Connector):
        return (next((i for i in self.segments if i.to_connector == connector), None), next((i for i in self.segments if i.from_connector == connector), None))    