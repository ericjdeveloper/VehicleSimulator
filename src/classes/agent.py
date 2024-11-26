from .entity import Entity
from .vector2 import Vector2
from .enums import Direction
from random import choice
import pygame
import math

class Agent(Entity):
    
    def __init__(self, pos=Vector2(), rot = 0):
        self.lane = None
        self.position = pos
        self.rotation = rot
        self.focus = Vector2(0,0)
        self.in_intersection = True

    def face(self, dir: Vector2):
        if dir.magnitude < 0.001: dir = Vector2(0,1)
        mult = 1 
        if dir.y < 0: mult = -1       
        self.rotation = math.degrees(math.acos(Vector2.Dot(Vector2(1,0), dir.normalized()))) * mult

    def tick(self):
        if self.lane is None: return

        dir = Direction.OUT if self.in_intersection else Direction.IN
        self.focus = self.lane.get_projection(self.position, dir, True)
        self.face((self.focus - self.position).normalized())
        
        if self.in_intersection:
            if self.lane.parent.is_passed(self.focus, Direction.IN):
                self.lane = self.lane.parent.connection.lanes[Direction.OUT][self.lane.index]
                self.in_intersection = False
        else:
            
            if self.lane.parent.is_passed(self.focus):
                node = self.lane.parent.parent

                ind = node.get_index_by_lane(self.lane)
                mat = node.get_connected_matrix()
                options = mat[ind]
                out_ind = choice([o for o in range(len(options)) if o > 0])
                self.lane = node.get_lane_by_index(out_ind, Direction.OUT)[0]
                self.in_intersection = True


        # move forward
        self.position += Vector2.rotate(Vector2(1,0), self.rotation)

    def draw(self, screen):
        rect_points = (
            Vector2(-5,5),
            Vector2(10,5),
            Vector2(10,-5),
            Vector2(-5, -5),
        )

        points = [(self.position + p.rotate(self.rotation)).to_list() for p in rect_points]
        pygame.draw.polygon(screen, (255,255, 0), points)
        pygame.draw.circle(screen, (100, 100, 100), self.focus.to_list(), 6)   

        dir = Direction.OUT if self.in_intersection else Direction.IN
        pygame.draw.circle(screen, (200,0,0), (self.lane.parent.get_offset_position() + self.lane.parent.get_lane_offset(self.lane.index, dir)).to_list(), 10)
        pygame.draw.circle(screen, (200,0,0), (self.lane.parent.get_offset_position() + self.lane.parent.get_lane_offset(self.lane.index, dir) + self.lane.slope * dir * 10).to_list(), 5)