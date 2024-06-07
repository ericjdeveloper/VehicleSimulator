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
    for i in range(0,360, step):
        pos = Vector2(250 + int(math.sin(math.radians(i)) * rad), 250 + int(math.cos(math.radians(i)) * rad))
        last_node = mm.add_node(pos, last_node)    

    first = mm.map.nodes[0]
    last = mm.map.nodes[-1]
    pos = (last.position + (first.position - last.position) / 2).intify()
    c = mm.add_connector([first, last])
    first.join_back(c)
    last.join_front(c)
    print("adding connectors... ")
    j1 = mm.add_node(Vector2(350,250))
    j2 = mm.add_node(Vector2(150, 250))
    c = mm.add_connector([j1, j2])
    j1.join_front(c)
    j1.join_back(mm.map.connectors[int(res / 4)])

    j2.join_front(mm.map.connectors[int(3 * res / 4)])
    j2.join_back(c)

def single_road():
    a = mm.add_node(Vector2(100,100))
    b = mm.add_node(Vector2(250,250),a)
    c = mm.add_node(Vector2(400,100),b)

draw_circle()
# single_road()
mm.run_game()