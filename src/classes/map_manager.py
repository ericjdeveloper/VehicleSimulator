import pygame

from .map import Map
from .vector2 import Vector2
from .road_node import RoadNode
from .connector import Connector
import math
class MapManager:

    def __init__(self):
        self.map = Map()

    def add_node(self, pos: Vector2, fro: RoadNode = None, to: RoadNode = None):
        con_from = None
        con_to = None

        if fro is not None:
            con_from = fro.forward
            if con_from is None:              
                con_from = self.add_connector([fro])
                fro.forward = con_from

        if to is not None:
            con_to = to.backward
            if con_to is None:                
                con_to =self.add_connector([to])
                to.backward = con_to

        node = RoadNode(pos, con_from, con_to)
        self.map.nodes.append(node)     
        return node

    def add_connector(self, connections=[]):
        junc = Connector(connections)
        self.map.connectors.append(junc)
        return junc

    # def insert_connector(self, pos: Vector2, segment: Connector): 
    #     junc = self.add_connector(pos)       
    #     f = segment[0]
    #     t = segment[1]
    #     node_from = self.add_node(pos, f, None)
    #     node_to = self.add_node(pos, None, t)    
    #     junc.connect(node_from)
    #     junc.connect(node_to)
    #     return junc

    def run_game(self):
        pygame.init()
        screen = pygame.display.set_mode([500,500])


        self.display(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

    def display(self, screen):
       
            
        screen.fill((255,255,255))

        LANE_OFFSET = 15
        ROAD_BORDER = 0
        for line in self.map.connectors:
            polygon_points = []
                        
            for v in line.connections:
                
                org = v.get_facing().orthogonal()
                polygon_points.append(
                        (v.position - org * ((LANE_OFFSET * (len(v.lanes[0]) + 0.5)) + ROAD_BORDER))
                    )
                polygon_points.append(
                        (v.position + org * ((LANE_OFFSET * (len(v.lanes[1]) + 0.5)) + ROAD_BORDER))
                    )

            p = line.position
            def point_sorter(point):                
                # return Vector2.angle(point - p, Vector2(1,0))
                d = (point - p)
                return math.atan2(d.x, d.y)
            
            polygon_points.sort(key=point_sorter)

            point_list = [p.to_list() for p in polygon_points]
            # print(point_list)
            pygame.draw.polygon(screen, (20,20,20), point_list, 0)


        
        for junc in self.map.connectors:
            # pygame.draw.rect(screen, (0,255,0), pygame.Rect(junc.position.x - 5, junc.position.y - 5, 10,10), 3)
            
            # offset = (node_b.position - node_a.position).normalized().orthogonal() * LANE_OFFSET
            for node_a in junc.connections:
                for node_b in junc.connections:
                    if node_a == node_b: continue

                    from_offset = node_a.get_facing().orthogonal() * LANE_OFFSET
                    to_offset = node_b.get_facing().orthogonal() * LANE_OFFSET
                    
                    for l in range(len(node_a.lanes[0])):
                        # pygame.draw.line(screen, (10,50,200), (node_a.position - offset * (l + 0.5)).to_list(), (node_b.position - offset * (l + 0.5)).to_list(), 6)
                        pygame.draw.line(screen, (10,50,200), (node_a.position - from_offset * (l + 0.5)).to_list(), (node_b.position - to_offset * (l + 0.5)).to_list(), 6)
                
                    for l in range(len(node_b.lanes[1])):
                        # pygame.draw.line(screen, (10,200,50), (node_a.position + offset * (l + 0.5)).to_list(), (node_b.position + offset * (l + 0.5)).to_list(), 6)
                        pygame.draw.line(screen, (10,200,50), (node_a.position + from_offset * (l + 0.5)).to_list(), (node_b.position + to_offset * (l + 0.5)).to_list(), 6)
                
        for node in self.map.nodes:
            continue
            pygame.draw.circle(screen, (255,0,0), node.position.to_list(), 15,4)
            # pygame.draw.circle(screen, (100,100,0), (node.position + (node.get_facing() * 10).intify()).to_list(), 3, 0)
            # if node.forward is not None and node.backward is not None: pygame.draw.circle(screen,(100,0,100), (node.position + ((node.forward.position - node.position) + (node.backward.position - node.position) / 2)).intify().to_list(), 4,0)

        pygame.display.flip()