import util

class HalfSpace:
    def __init__(self, normal):
            self.normal = normal

    def point_inside(self, point):
        return util.dot(self.normal, point) >= 0
