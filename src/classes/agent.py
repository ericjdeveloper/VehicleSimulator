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
        self.color = pygame.color.Color(choice(["blue4", "chartreuse4", "darkmagenta", "darkred", "darkorange3", "darkslateblue", "gold1", "gray34", "white", "lawngreen", "violetred4"]))

    def face(self, dir: Vector2):
        if dir.magnitude < 0.001: dir = Vector2(0,1)
        mult = 1 
        if dir.y < 0: mult = -1       
        self.rotation = math.degrees(math.acos(Vector2.Dot(Vector2(1,0), dir.normalized()))) * mult

    def tick(self, delta_time):
        if self.lane is None: return
        
        if (self.focus - self.position).magnitude < 3:
            if self.in_intersection:
                self.in_intersection = False
                self.set_target(self.lane.parent.connection.lanes[Direction.OUT][self.lane.index])
            else:
                node = self.lane.parent.parent

                ind = node.get_index_by_lane(self.lane)
                mat = node.get_connected_matrix()
                options = mat[ind]
                out_ind = choice([o for o in range(len(options)) if options[o] > 0])
                self.in_intersection = True
                self.set_target(node.get_lane_by_index(out_ind, Direction.IN)[0])

        # move forward
        self.position += Vector2.rotate(Vector2(100,0), self.rotation) * delta_time

    def set_target(self, lane):
        self.lane = lane
        self.focus = self.lane.get_position()
        self.face((self.focus - self.position).normalized())

    def draw(self, screen):
        rect_points = (
            Vector2(-5,5),
            Vector2(10,5),
            Vector2(10,-5),
            Vector2(-5, -5),
        )

        points = [(self.position + p.rotate(self.rotation)).to_list() for p in rect_points]
        pygame.draw.polygon(screen, self.color, points)
        # pygame.draw.circle(screen, (100, 100, 100), self.focus.to_list(), 6)   

        # dir = Direction.OUT if self.in_intersection else Direction.IN
        # pygame.draw.circle(screen, (200,0,0), (self.lane.parent.get_offset_position() + self.lane.parent.get_lane_offset(self.lane.index, dir)).to_list(), 10)
        # pygame.draw.circle(screen, (200,0,0), (self.lane.parent.get_offset_position() + self.lane.parent.get_lane_offset(self.lane.index, dir) + self.lane.slope * dir * 10).to_list(), 5)