import pygame

from .map import Map
from .vector2 import Vector2
from .road_node import RoadNode
import math

class MapManager:

    def __init__(self):
        self.map = Map()

    def add_node(self, pos: Vector2, connected_nodes=[], lanes = (1,1)):

        node = RoadNode(pos)

        for n in connected_nodes:
            if n is None: continue
            self.connect_nodes(node, n, lanes, lanes)

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


        self.display(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

    def display(self, screen):
       
        def draw_line(fro: Vector2, to: Vector2, color, thickness, is_dashed = False):
            if not is_dashed:
                pygame.draw.line(screen, color, fro.to_list(), to.to_list(), thickness)
                return
            
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

        LANE_OFFSET = 15
        ROAD_BORDER = 0
        for point in self.map.nodes:            
            polygon_points = []
                     
            for con in point.connections: 
                continue               
                org = con.get_facing().orthogonal()
                polygon_points.append(
                        (con.get_position() - org * ((LANE_OFFSET * (len(con.lanes[0]) + 0.5)) + ROAD_BORDER))
                    )
                polygon_points.append(
                        (con.get_position() + org * ((LANE_OFFSET * (len(con.lanes[1]) + 0.5)) + ROAD_BORDER))
                    )
            if len(polygon_points) == 2: continue

            p = point.position
            def point_sorter(point):                
                # return Vector2.angle(point - p, Vector2(1,0))
                d = (point - p)
                return math.atan2(d.x, d.y)
            
            polygon_points.sort(key=point_sorter)

            point_list = [p.to_list() for p in polygon_points]
            # print(point_list)
            pygame.draw.polygon(screen, (20,20,20), point_list, 0)

            for con in point.connections: 
                polygon_points = []             
                con2 = con.connection
                if con2 is None: continue

                org = con.get_facing().orthogonal()
                org2 = con2.get_facing().orthogonal()
                polygon_points.append(
                        (con.get_position() - org * ((LANE_OFFSET * (len(con.lanes[0]) + 0.5)) + ROAD_BORDER))
                    )
                polygon_points.append(
                        (con.get_position() + org * ((LANE_OFFSET * (len(con.lanes[1]) + 0.5)) + ROAD_BORDER))
                    )
                
                polygon_points.append(
                        (con2.get_position() - org2 * ((LANE_OFFSET * (len(con2.lanes[0]) + 0.5)) + ROAD_BORDER))
                    )
                polygon_points.append(
                        (con2.get_position() + org2 * ((LANE_OFFSET * (len(con2.lanes[1]) + 0.5)) + ROAD_BORDER))
                    )                        
            
                polygon_points.sort(key=point_sorter)

                point_list = [p.to_list() for p in polygon_points]
                # print(point_list)
                pygame.draw.polygon(screen, (20,20,20), point_list, 0)
        
        for junc in self.map.nodes:   
            
            # pygame.draw.rect(screen, (0,255,0), pygame.Rect(junc.position.x - 5, junc.position.y - 5, 10,10), 3)
            
            # offset = (node_b.position - con_a.position).normalized().orthogonal() * LANE_OFFSET
            m = junc.get_connected_matrix()
            for i in range(len(m)): 
                continue
                print(i, m[i])
                lane_a, l_a = junc.get_in_lane_by_index(i)
                lanes = [junc.get_out_lane_by_index(j) for j, x in enumerate(m[i]) if x == 1]


                for lane_b, l_b in lanes:
                    from_offset = lane_a.parent.get_facing().orthogonal() * LANE_OFFSET
                    to_offset = lane_b.parent.get_facing().orthogonal() * LANE_OFFSET

                    pygame.draw.line(screen, (10,200,50), (lane_a.parent.get_position() - from_offset * (l_a + 0.5)).to_list(), (lane_b.parent.get_position() + to_offset * (l_b + 0.5)).to_list(), 6)

                # for con_b in junc.connections:
                #     if con_a == con_b: continue

                #     from_offset = con_a.get_facing().orthogonal() * LANE_OFFSET
                #     to_offset = con_b.get_facing().orthogonal() * LANE_OFFSET
                    
                #     for l in range(len(con_a.lanes[0])):
                #         # pygame.draw.line(screen, (10,50,200), (con_a.position - offset * (l + 0.5)).to_list(), (node_b.position - offset * (l + 0.5)).to_list(), 6)
                #         pygame.draw.line(screen, (10,50,200), (con_a.get_position() - from_offset * (l + 0.5)).to_list(), (con_b.get_position() + to_offset * (l + 0.5)).to_list(), 6)
                
                #     for l in range(len(con_b.lanes[1])):
                #         # pygame.draw.line(screen, (10,200,50), (con_a.position + offset * (l + 0.5)).to_list(), (node_b.position + offset * (l + 0.5)).to_list(), 6)
                #         pygame.draw.line(screen, (10,200,50), (con_a.get_position() + from_offset * (l + 0.5)).to_list(), (con_b.get_position() - to_offset * (l + 0.5)).to_list(), 6)
                
            for con in junc.connections:
                con_a = con
                con_b = con.connection

                pygame.draw.line(screen, (247,181,0), (con_a.get_position()).to_list(), (con_b.get_position()).to_list(), 3)

                from_offset = con_a.get_facing().orthogonal() * LANE_OFFSET
                to_offset = con_b.get_facing().orthogonal() * LANE_OFFSET
                for l in range(len(con_a.lanes[0])):         
                    thickness = 2
                    dashed = True

                    if l+1 == len(con_a.lanes[0]):
                        thickness = 3
                        dashed = False

                    draw_line((con_a.get_position() + from_offset * (l + 1)),
                               (con_b.get_position()- to_offset * (l + 1)),
                                (200,200,200),
                                 thickness,
                                 dashed
                                )

        pygame.display.flip()