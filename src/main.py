from classes.map_manager import MapManager
from classes.vector2 import Vector2
import math


mm = MapManager()

DEFAULT_LANES = (2,2)
def draw_circle():
    res = 10
    rad = 200
    last_node = None
    step = int(360/res)
    lane_count = 2
    for i in range(0,360, step):
        pos = Vector2(250 + int(math.sin(math.radians(i)) * rad), 250 + int(math.cos(math.radians(i)) * rad))
        last_node = mm.add_node(pos, [last_node], (lane_count, lane_count))

    first = mm.map.nodes[0]
    last = mm.map.nodes[-1]
    pos = (last.position + (first.position - last.position) / 2).intify()
    mm.connect_nodes(first, last, DEFAULT_LANES, DEFAULT_LANES)
    
    j1 = mm.add_node(Vector2(350,250))
    j2 = mm.add_node(Vector2(150, 250))
    mm.connect_nodes(j1, j2, (2,2), (2,2))

    mm.connect_nodes(mm.map.nodes[int(res / 4)], j1, (1,1), (1,1))
    mm.connect_nodes(mm.map.nodes[int(3 * res / 4)], j2, (1,1), (1,1))

    # j2.back.join(c)

def single_road():
    a = mm.add_node(Vector2(100,100))
    b = mm.add_node(Vector2(200,250),[a])
    c = mm.add_node(Vector2(300,250),[b], [1,2])
    d = mm.add_node(Vector2(400,100),[c])

draw_circle()
# single_road()
mm.run_game()