from .entity import Entity
from .road_node import RoadNode, Alignments, Direction
from .vector2 import Vector2
import pygame

class Map(Entity):

    def __init__(self):
        self.nodes = []
        self.screen = None

    def calculate_offsets(self):        
        class Line:
            def __init__(self, pos: Vector2, dir: Vector2):
                self.pos = pos
                self.dir = dir

            def solve(self, x: float):
                return (x - self.pos.x) * self.dir.slope + self.pos.y

            def intersect(self, other, allow_backwards=False):             
                if abs(abs(Vector2.Dot(self.dir.normalized(), other.dir.normalized())) - 1) < 0.001: return None

                p = None
                if self.dir.x == 0: p = Vector2(self.pos.x, other.solve(self.pos.x))
                elif other.dir.x == 0: p = Vector2(other.pos.x, self.solve(other.pos.x))
                else:
                    x = (other.pos.y + self.dir.slope * self.pos.x - self.pos.y - other.dir.slope * other.pos.x) / (self.dir.slope - other.dir.slope)
                    y = self.solve(x)

                    p = Vector2(x,y)

                if not allow_backwards:
                    
                    if Vector2.Dot(p - other.pos, other.dir) < 0 or \
                        Vector2.Dot(p - self.pos, self.dir) < 0:
                        return None

                return p   

        for junc in self.nodes:
            all_lines = [Line(x.get_position() + x.get_edge(Direction.OUT), x.get_facing()) for x in junc.connections] +\
                        [Line(x.get_position() + x.get_edge(Direction.IN), x.get_facing()) for x in junc.connections]

            points  = [line.pos for line in all_lines]

            for line_a in all_lines:
                for line_b in all_lines:
                    p = line_a.intersect(line_b)
                    if p is None:
                        continue
                        
                    points.append(p)

            for con in junc.connections:
                dists = map(lambda a: Vector2.Dot(a - junc.position, con.get_facing()), points)      
                dist = max(dists)       
                con.spacing = dist
