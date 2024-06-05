import pygame

from .map import Map
from .vector2 import Vector2
from .connector import Connector
from .junction import Junction
from .road_segment import RoadSegment

class MapManager:

    def __init__(self):
        self.map = Map()

    def add_connector(self, pos: Vector2, fro: Connector=None, to: Connector=None):
        con = Connector(pos, fro, to)
        self.map.connectors.append(con)

        if fro is not None:
            segment = self.map.get_segments_by_connector(fro)[1]
            if segment is None:      
                segment = RoadSegment(fro, con)
                self.map.segments.append(segment)
            else:
                segment.to_connector = con

        if to is not None:
            segment = self.map.get_segments_by_connector(to)[0]
            if segment is None:
                segment = RoadSegment(con, to)
                self.map.segments.append(segment)
            else:
                segment.from_connector = con

        return con

    def add_junction(self, pos: Vector2):
        junc = Junction(pos)
        self.map.junctions.append(junc)
        return junc

    def insert_junction(self, pos: Vector2, segment: RoadSegment): 
        junc = self.add_junction(pos)       
        f = segment.from_connector
        t = segment.to_connector
        con_from = self.add_connector(pos, f, None)
        con_to = self.add_connector(pos, None, t)    
        junc.connect(con_from)
        junc.connect(con_to)
        return junc

    def display(self):
        pygame.init()
        screen = pygame.display.set_mode([500,500])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            screen.fill((255,255,255))

            for junc in self.map.junctions:
                pygame.draw.circle(screen, (20,20,20), junc.position.to_list(), 30, 0)

            LANE_OFFSET = 10
            ROAD_BORDER = 5
            for line in self.map.segments:
                polygon_points = (
                    (line.from_connector.position + line.from_connector.get_facing() * (LANE_OFFSET * len(line.from_connector.lanes[0]) + ROAD_BORDER)).to_list(),
                    (line.from_connector.position - line.from_connector.get_facing() * (LANE_OFFSET * len(line.from_connector.lanes[1]) + ROAD_BORDER)).to_list(),
                    (line.to_connector.position - line.to_connector.get_facing() * (LANE_OFFSET * len(line.to_connector.lanes[0]) + ROAD_BORDER)).to_list(),
                    (line.to_connector.position + line.to_connector.get_facing() * (LANE_OFFSET * len(line.to_connector.lanes[1]) + ROAD_BORDER)).to_list(),
                )
                pygame.draw.polygon(screen, (20,20,20), polygon_points, 0)


            
            for line in self.map.segments:
                # offset = (line.to_connector.position - line.from_connector.position).normalized().orthogonal() * LANE_OFFSET

                from_offset = line.from_connector.get_facing() * LANE_OFFSET
                to_offset = line.to_connector.get_facing() * LANE_OFFSET
                
                for l in range(len(line.from_connector.lanes[0])):
                    # pygame.draw.line(screen, (10,50,200), (line.from_connector.position - offset * (l + 0.5)).to_list(), (line.to_connector.position - offset * (l + 0.5)).to_list(), 6)
                    pygame.draw.line(screen, (10,50,200), (line.from_connector.position - from_offset * (l + 0.5)).to_list(), (line.to_connector.position - to_offset * (l + 0.5)).to_list(), 6)
            
                for l in range(len(line.to_connector.lanes[1])):
                    # pygame.draw.line(screen, (10,200,50), (line.from_connector.position + offset * (l + 0.5)).to_list(), (line.to_connector.position + offset * (l + 0.5)).to_list(), 6)
                    pygame.draw.line(screen, (10,200,50), (line.from_connector.position + from_offset * (l + 0.5)).to_list(), (line.to_connector.position + to_offset * (l + 0.5)).to_list(), 6)

            for con in self.map.connectors:
                pygame.draw.rect(screen, (0,0,255), pygame.Rect(con.position.x - 20, con.position.y - 10, 40, 20), 4)



            pygame.display.flip()

        pygame.quit()