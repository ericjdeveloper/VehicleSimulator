from classes.map_manager import MapManager
from classes.road_segment import RoadSegment
from classes.vector2 import Vector2
import math


mm = MapManager()

res = 10
rad = 200
last_con = None
step = int(360/res)
for i in range(0,360, step):
    pos = Vector2(250 + int(math.sin(math.radians(i)) * rad), 250 + int(math.cos(math.radians(i)) * rad))
    last_con = mm.add_connector(pos, last_con)

mm.map.connectors[0].join_back(last_con)
mm.map.segments.append(RoadSegment(last_con, mm.map.connectors[0]))
print("adding junctions... ")
j1 = mm.insert_junction(Vector2(350,250), mm.map.segments[int(res/4)])
j2 = mm.insert_junction(Vector2(150, 250), mm.map.segments[int(3 * res/4)])
c1 = mm.add_connector(j1.position)
j1.connect(c1)
c2 = mm.add_connector(j2.position, c1)
j2.connect(c2)

mm.display()