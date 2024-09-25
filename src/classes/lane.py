class Lane:

    DEFAULT_LANE_WIDTH=15

    def __init__(self, parent, index, width=DEFAULT_LANE_WIDTH):
        self.parent = parent
        self.index = index
        self.width = width

class LaneBorder:

    def __init__(self):
        lane_type = None