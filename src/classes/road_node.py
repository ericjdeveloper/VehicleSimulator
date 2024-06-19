from .vector2 import Vector2
from .lane import Lane
import math
import numpy

class RoadNode:

    class Connector:

        def __init__(self, parent, lane_counts=(2,2), pos=None):
            self.position = None

            if pos is not None:
                self.position = pos            

            self.parent = parent
            self.lanes = ([Lane(self, l) for l in range(lane_counts[0])],[Lane(self, l) for l in range(lane_counts[1])])
            self.connection = None

        def join(self, con):
            if self.connected():
                self.connection.disconnect(self.parent)
            
            self.connection = con

        def connected(self):
            return self.connection is not None
        
        def get_position(self):
            if self.position is not None: return self.position
            return self.parent.position

        def get_facing(self):
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

    def get_connected_matrix(self):
        if self.con_matrix is not None: return self.con_matrix

        out_count = sum(len(x.lanes[0]) for x in self.connections)
        in_count = sum(len(x.lanes[1]) for x in self.connections)

        mat = []
        for c1 in self.connections:            
            for i in range(len(c1.lanes[1])):     
                lane_row = [0] * out_count           
                for c in self.connections:
                    
                    if len(c.lanes[0]) > i:
                        ind = self.get_out_index_by_lane(c.lanes[0][i])
                        lane_row[ind] = 1
            
                mat.append(lane_row)
            
        return mat

    def get_out_index_by_lane(self, lane):
        all_lanes = [a for x in self.connections for a in x.lanes[0]]
        return all_lanes.index(lane)

    def get_in_index_by_lane(self, lane):
        all_lanes = [a for x in self.connections for a in x.lanes[1]]
        return all_lanes.index(lane)

    def get_in_lane_by_index(self, index):
        prev_top = 0

        for cc in self.connections:
            if prev_top + len(cc.lanes[1]) > index:
                return cc.lanes[1][index - prev_top], index - prev_top
            prev_top += len(cc.lanes[1])            

    def get_out_lane_by_index(self, index):
        prev_top = 0
        
        for cc in self.connections:
            if prev_top + len(cc.lanes[0]) > index:
                return cc.lanes[0][index - prev_top], index - prev_top
            prev_top += len(cc.lanes[0])  



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


        