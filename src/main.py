from classes.map_manager import MapManager
from classes.vector2 import Vector2
from classes.connector import Connector
import math


mm = MapManager()

def draw_circle():
    res = 10
    rad = 200
    last_node = None
    step = int(360/res)
    lane_count = 2
    for i in range(0,360, step):
        pos = Vector2(250 + int(math.sin(math.radians(i)) * rad), 250 + int(math.cos(math.radians(i)) * rad))
        last_node = mm.add_node(pos, last_node, None, (lane_count, lane_count))

    first = mm.map.nodes[0]
    last = mm.map.nodes[-1]
    pos = (last.position + (first.position - last.position) / 2).intify()
    c = mm.add_connector([first, last])
    first.back.join(c)
    last.front.join(c)
    print("adding connectors... ")
    j1 = mm.add_node(Vector2(350,250))
    j2 = mm.add_node(Vector2(150, 250))
    c = mm.add_connector([j1, j2])
    j1.front.join(c)
    j1.back.join(mm.map.connectors[int(res / 4)])

    j2.front.join(mm.map.connectors[int(3 * res / 4)])
    j2.back.join(c)

def single_road():
    a = mm.add_node(Vector2(100,100))
    b = mm.add_node(Vector2(250,250),a)
    c = mm.add_node(Vector2(400,100),b)

draw_circle()
# single_road()
mm.run_game()