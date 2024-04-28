from math import sin, cos, radians
from skspatial.objects import Line
from hyper_params import *


class LineVision(object):
    def __init__(self, agent_size, angle, body):
        super.__init__()
        self.height, self.width = agent_size
        self.angle = angle
        self.body = body

    def get_offsets(self):
        # Returns front_offset, side_offset
        return ((cos(radians(-self.angle)) * self.height, sin(radians(-self.angle)) * self.height),
                (-sin(radians(-self.angle)) * self.width / 4, cos(radians(-self.angle)) * self.width / 4))

    def get_relative_point(self, offset):
        return self.body.position + offset

    def get_vision_line(self, offset, angle):
        offset_global = self.get_relative_point(offset)
        return Line(offset_global, offset_global + (cos(radians(-self.angle + angle)) * VISION_LINE_LENGTH,
                                                    sin(radians(-self.angle + angle)) * VISION_LINE_LENGTH))