from .vector2 import Vector2
from .lane import Lane
import math

class Connector:pass



class RoadNode:

    class ConnectorConnection:

        def __init__(self, parent, connection, lane_directions=[]):
            self.parent = parent
            self.connection = connection
            self.lane_directions = lane_directions

        def join(self, con: Connector):
            if self.connected():
                self.connection.disconnect(self.parent)
            
            self.connection = con
            if self.connected():
                self.connection.connect(self.parent)

        def connected(self):
            return self.connection is not None

    def __init__(self, pos: Vector2, b =None, f=None, lane_counts = (2,2), facing: Vector2=None):                
        self.position = pos
        self.lanes = ([Lane(self, l) for l in range(lane_counts[0])],[Lane(self, l) for l in range(lane_counts[1])])
        self.back = self.ConnectorConnection(self, None, (self.lanes[0], self.lanes[1]))
        self.front = self.ConnectorConnection(self, None, (self.lanes[1], self.lanes[0]))

        self.facing = facing

        self.front.join(f)
        self.back.join(b)

    def get_facing(self):
        if self.facing is not None:
            return self.facing
        
        if not self.back.connected() and not self.front.connected(): return Vector2(0,1)

        if not self.front.connected():
            return (self.front.connection.position - self.position).normalized()
        
        if not self.back.connected():
            return (self.back.connection.position - self.position).normalized()


        f = (self.front.connection.position - self.position).normalized()
        b = (self.back.connection.position - self.position).normalized()
        face = (f + ((b - f) / 2)).orthogonal()
        if face.x == 0 and face.y == 0:
            face = (self.front.connection.position - self.position)

        return face.normalized()        


        