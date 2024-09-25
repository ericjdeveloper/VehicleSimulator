from .vector2 import Vector2
from .lane import Lane
import math
import numpy

from enum import IntEnum

class Alignments(IntEnum):
    INNER=-1
    CENTER=0
    OUTER=1

class Direction(IntEnum):
    OUT=1
    IN=-1

    @staticmethod
    def opposite(d):
        return d * -1


class RoadNode:

    class Connector:

        DEFAULT_ROAD_MARGIN=6

        def __init__(self, parent, lane_counts=(2,2), pos=None):
            self.position = None

            if pos is not None:
                self.position = pos            

            self.parent = parent
            self.lanes = {Direction.OUT: [Lane(self, l) for l in range(lane_counts[0])],
                          Direction.IN: [Lane(self, l) for l in range(lane_counts[1])]
                        }
            self.connection = None
            self.spacing = 0
            self.margins = {
                Direction.OUT: self.DEFAULT_ROAD_MARGIN,
                Direction.IN: self.DEFAULT_ROAD_MARGIN
            }
            self.facing = None


        def join(self, con):
            if self.connected():
                self.connection.disconnect(self.parent)
            
            self.connection = con

        def connected(self):
            return self.connection is not None
        
        def get_position(self):
            if self.position is not None: return self.position
            return self.parent.position

        def get_offset_position(self):
            return self.get_position() + self.get_facing() * self.spacing
        
        def get_lane_offset(self, lane_index, direction = Direction.OUT, alg=Alignments.CENTER):
            magnitude = 0
            for i in range(lane_index):
                magnitude += self.lanes[direction][i].width

            if alg is Alignments.CENTER:
                magnitude += int(self.lanes[direction][lane_index].width / 2)
            elif alg is Alignments.OUTER:
                magnitude += self.lanes[direction][lane_index].width
            
            return self.get_facing().orthogonal() * (magnitude * direction)

        def get_edge(self, direction: Direction, include_margin=True):
            width= self.get_lane_offset(len(self.lanes[direction]) -1, direction, Alignments.OUTER)

            if include_margin: 
                width += width.normalized() * self.margins[direction]

            return width

        def get_facing(self):
            if self.facing is not None: return self.facing
            if not self.connection: return Vector2(0,1)
            return (self.connection.get_position() - self.get_position()).normalized()

    def __init__(self, pos: Vector2):
        self.position = pos
        self.connections = []  
        self.con_matrix = None      

    def create_connection(self, lanes):
        con = self.Connector(self, lanes)
        self.connections.append(con)
        return con

    def get_connected_matrix(self, dir = Direction.OUT):
        if self.con_matrix is not None: return self.con_matrix

        count = sum(len(x.lanes[dir]) for x in self.connections)

        mat = []
        for c1 in self.connections:            
            for i in range(len(c1.lanes[Direction.opposite(dir)])):     
                lane_row = [0] * count           
                for c in self.connections:

                    if len(c.lanes[dir]) > i:
                        ind = self.get_index_by_lane(c.lanes[dir][i])
                        lane_row[ind] = 1
            
                mat.append(lane_row)
            
        return mat

    def get_index_by_lane(self, lane, direction=Direction.OUT):
        all_lanes = [a for x in self.connections for a in x.lanes[direction]]
        return all_lanes.index(lane)
    
    def get_lane_by_index(self, index, direction=Direction.OUT):
        prev_top = 0
        
        for cc in self.connections:
            if prev_top + len(cc.lanes[direction]) > index:
                return cc.lanes[direction][index - prev_top], index - prev_top
            prev_top += len(cc.lanes[direction])       



    # def get_facing(self):
        
    #     if len(self.connections) == 0: return Vector2(0,1)

    #     avg_faces = []
    #     for con in self.connections:
    #         face = (con.connection.parent.position - self.position).normalized()
    #         avg_faces.append(face)

    #     face = 
    #     if face.x == 0 and face.y == 0:
    #         return Vector2(0,1)

    #     return face.normalized()        


        