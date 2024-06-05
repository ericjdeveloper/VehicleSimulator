from .vector2 import Vector2
from .lane import Lane

class Connector:

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
        if self.forward is None and self.backward is None: return Vector2(0,1)
        
        dirs = [(self.position - i.position) for i in [i for i in (self.forward, self.backward) if i is not None]]
        x = sum(f.x for f in dirs) / len(dirs)
        y = sum(f.y for f in dirs) / len(dirs)

        return Vector2(x,y).normalized()


    def join_front(self, f):
        if self.forward is not None:
            self.forward.backward = None
        self.forward = f
        if f is not None:
            f.backward = self

    def join_back(self, b):
        if self.backward is not None:
            self.backward.forward = None
        self.backward = b
        if b is not None:
            b.forward = self


        