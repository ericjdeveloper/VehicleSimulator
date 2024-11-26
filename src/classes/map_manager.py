import pygame

from .map import Map
from .vector2 import Vector2
from .road_node import RoadNode, Alignments, Direction
from .agent import Agent
from time import sleep
import math


class MapManager:

    def __init__(self):
        self.map = Map()

    def add_node(self, pos: Vector2, connected_nodes=[], lanes = (1,1)):

        node = RoadNode(pos)

        for n in connected_nodes:
            if n is None: continue
            self.connect_nodes(node, n, lanes, list(reversed(lanes)))

        self.map.nodes.append(node)     
        return node

    def connect_nodes(self, node_a: RoadNode, node_b: RoadNode, a_lanes=[], b_lanes=[]):
            c1 = node_a.create_connection(a_lanes)
            c2 = node_b.create_connection(b_lanes)
            c1.join(c2)
            c2.join(c1)

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
        self.map.screen = screen
        
        self.a = Agent(Vector2(50,100))
        self.a.lane = self.map.nodes[0].connections[0].lanes[Direction.IN][0]

        running = True
        while running:
            self.a.tick()
            self.display(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            

        pygame.quit()

    def display(self, screen):       
        def point_sorter(point, center):                
            d = (point - center)
            return math.atan2(d.x, d.y)

        def draw_line(fro: Vector2, to: Vector2, color, thickness, is_dashed = False):
            if not is_dashed:
                pygame.draw.line(screen, color, fro.to_list(), to.to_list(), thickness)
                
            
            diff_vec = fro - to
            dist  = diff_vec.magnitude
            line_length = 10
            gap_length = 7
            c_pos = 0
            while c_pos < dist:
                start_pos = c_pos / dist
                end_pos = min(start_pos + line_length / dist, 1)
                pygame.draw.line(screen, color, (fro - diff_vec * start_pos).to_list(), (fro - diff_vec * end_pos).to_list(), thickness)
                c_pos += line_length + gap_length
        screen.fill((255,255,255))        

        def draw_junction(junc):

            if len(junc.connections) < 2: return

            polygon_points = []
            for con in junc.connections:
                polygon_points.append(
                        (con.get_offset_position() + con.get_edge(Direction.OUT))
                    )
                polygon_points.append(
                        (con.get_offset_position() + con.get_edge(Direction.IN))
                    ) 

            polygon_points.sort(key=lambda a: point_sorter(a, junc.position))

            point_list = [p.to_list() for p in polygon_points]
            pygame.draw.polygon(screen, (20,20,20), point_list)            

        # draw roads
        def draw_roads(node):
            for con in node.connections:                 
                polygon_points = []             

                if con.connection is None: continue

                polygon_points.append(
                        (con.get_offset_position() + con.get_edge(Direction.OUT))
                    )
                polygon_points.append(
                        (con.get_offset_position() + con.get_edge(Direction.IN))
                    )
                
                polygon_points.append(
                        (con.connection.get_offset_position() + con.connection.get_edge(Direction.IN))
                    )
                polygon_points.append(
                        (con.connection.get_offset_position() + con.connection.get_edge(Direction.OUT))
                    )                        
            
                polygon_points.sort(key=lambda a: point_sorter(a, node.position))
                
                point_list = [p.to_list() for p in polygon_points]
                # print(point_list)
                pygame.draw.polygon(screen, (20,20,20), point_list)
            
        def draw_intersection_lanes(node): 

            m = node.get_connected_matrix()

            cons = list(range(len(node.connections)))
            cons.sort(key=lambda a: point_sorter(node.connections[a].get_offset_position(), node.position))

            for i in cons:
                con_a = node.connections[i]
                con_b = node.connections[(i - 1) % len(node.connections)]

                pos_a = con_a.get_offset_position() + con_a.get_edge(Direction.OUT, include_margin=False)
                pos_b = con_b.get_offset_position() + con_b.get_edge(Direction.IN, include_margin=False)

                draw_line(pos_a, pos_b, (200,200,200), 3)                
                

            if len(node.connections) == 2:
                    
                con_a = node.connections[0]
                con_b = node.connections[1]

                pygame.draw.line(screen, (247,181,0), (con_a.get_offset_position()).to_list(), (con_b.get_offset_position()).to_list(), 3)

                for dir in Direction:
                    for l in range(len(con_a.lanes[dir]) -1,):       
                        from_offset = con_a.get_lane_offset(l, dir, Alignments.OUTER)
                        to_offset = con_b.get_lane_offset(l, dir.opposite(), Alignments.OUTER) 

                        draw_line((con_a.get_offset_position() + from_offset),
                                (con_b.get_offset_position() + to_offset),
                                    (200,200,200),
                                    2,
                                    True
                                    )
                    
                return
            
            # for i in range(len(m)):
            #     lane_a, l_a = node.get_lane_by_index(i, Direction.IN)
            #     lanes = [node.get_lane_by_index(j, Direction.OUT) for j in range(len(m[i])) if m[i][j] == 1]

                
            #     for lane_b, l_b in lanes:
            #         from_offset = lane_a.parent.get_edge(Direction.OUT, include_margin=False)
            #         to_offset = lane_b.parent.get_edge(Direction.IN, include_margin=False)

            #         draw_line(lane_a.parent.get_offset_position() - from_offset * (l_a + 0.5), lane_b.parent.get_offset_position() + to_offset * (l_b + 0.5), (10,200,50), 2)

                # for con_b in junc.connections:
                #     if con_a == con_b: continue

                #     from_offset = con_a.get_facing().orthogonal() * LANE_OFFSET
                #     to_offset = con_b.get_facing().orthogonal() * LANE_OFFSET
                    
                #     for l in range(len(con_a.lanes[Direction.OUT])):
                #         # pygame.draw.line(screen, (10,50,200), (con_a.position - offset * (l + 0.5)).to_list(), (node_b.position - offset * (l + 0.5)).to_list(), 6)
                #         pygame.draw.line(screen, (10,50,200), (con_a.get_position() - from_offset * (l + 0.5)).to_list(), (con_b.get_position() + to_offset * (l + 0.5)).to_list(), 6)
                
                #     for l in range(len(con_b.lanes[Direction.IN])):
                #         # pygame.draw.line(screen, (10,200,50), (con_a.position + offset * (l + 0.5)).to_list(), (node_b.position + offset * (l + 0.5)).to_list(), 6)
                #         pygame.draw.line(screen, (10,200,50), (con_a.get_position() + from_offset * (l + 0.5)).to_list(), (con_b.get_position() - to_offset * (l + 0.5)).to_list(), 6)

        def draw_road_lanes(node):
            for con in node.connections:                
                con_a = con
                con_b = con.connection

                pygame.draw.line(screen, (247,181,0), con_a.get_offset_position().to_list(), con_b.get_offset_position().to_list(), 3)
                
                for l in range(len(con_a.lanes[Direction.OUT])):     

                    thickness = 2
                    dashed = True

                    if l+1 == len(con_a.lanes[Direction.OUT]):
                        thickness = 3
                        dashed = False

                    from_offset = con_a.get_lane_offset(l, Direction.OUT, Alignments.OUTER)
                    to_offset = con_b.get_lane_offset(l, Direction.IN, Alignments.OUTER)  

                    draw_line((con_a.get_offset_position() + from_offset),
                               (con_b.get_offset_position() + to_offset),
                                (200,200,200),
                                 thickness,
                                 dashed
                                )


        self.map.calculate_offsets()

        for node in self.map.nodes:            
            draw_junction(node)
            draw_roads(node)

        for node in self.map.nodes:                        
            draw_intersection_lanes(node)
            draw_road_lanes(node)


        self.a.draw(screen)        

        pygame.display.flip()