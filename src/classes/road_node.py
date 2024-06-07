from .vector2 import Vector2
from .lane import Lane
import math

class Connector:pass

class RoadNode:

    def __init__(self, pos: Vector2, b=None, f=None, facing: Vector2=None):        
        self.backward = None
        self.forward = None
        self.position = pos
        self.lanes = ([Lane(), Lane()],[Lane(), Lane()])
        self.markers = []

        self.facing = facing

        if f is not None: self.join_front(f)
        if b is not None: self.join_back(b)

    def get_facing(self):
        if self.facing is not None:
            return self.facing
        
        if self.backward is None and self.forward is None: return Vector2(0,1)

        if self.backward is None:
            return (self.forward.position - self.position).normalized()
        
        if self.forward is None:
            return (self.backward.position - self.position).normalized()

        # a = Vector2.Angle((self.forward.position - self.position), (self.backward.position - self.position)) / 2
        # print(math.degrees(a))
        # x =  Vector2(math.cos(a) * self.forward.position.x - math.sin(a) * self.forward.position.y,
        #                math.sin(a) * self.forward.position.x + math.cos(a) * self.forward.position.y)
        # print(x)
        # return x.normalized()
        f = (self.forward.position - self.position).normalized()
        b = (self.backward.position - self.position).normalized()
        face = (f + ((b - f) / 2)).orthogonal()
        if face.x == 0 and face.y == 0:
            face = (self.forward.position - self.position)

        return face.normalized()
        # return (self.forward.position - self.position).normalized()



    def join_front(self, f: Connector):
        if self.forward is not None:
            self.forward.disconnect(self)

        self.forward = f
        if f is not None:            
            self.forward.connect(self)

    def join_back(self, b: Connector):
        if self.backward is not None:
            self.backward.disconnect(self)

        self.backward = b
        if b is not None:
            self.backward.connect(self)


        