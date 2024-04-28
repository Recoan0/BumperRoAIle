from math import sin, cos, radians

import numpy as np
from skspatial.objects import Line
from pygame.math import Vector2

from object.bumper_car import BumperCar
from const.hyper_params import *


class LineVisionCar(BumperCar):
    def __init__(self, spawn_angle: float, spawn_location: Vector2, color: str,
                 top_speed: float = 10., steering_speed: float = .1, acceleration: float = 100., mass: float = .1):
        super().__init__(spawn_angle, spawn_location, color, top_speed, steering_speed, acceleration, mass)

    def get_observation(self, env) -> np.ndarray:
        vls = self.vision_lines()
        enemies = env.agents.sprites().remove(self)

        # TODO: Calculate closest intersection with circle and enemies for each lines

        obs = np.array([self.body.angular_velocity, *self.get_relative_velocity()])
        return obs  # TODO

    def vision_lines(self):
        front_offset, side_offset = self.get_offsets()

        front_line = self.get_vision_line(front_offset, 0)
        rear_line = self.get_vision_line(-1 * front_offset, 180)
        front_right_diagonal_side_line = self.get_vision_line(front_offset + side_offset, 45)
        front_left_diagonal_side_line = self.get_vision_line(front_offset - side_offset, -45)
        front_right_perpendicular_side_line = self.get_vision_line(front_offset + side_offset, 90)
        front_left_perpendicular_side_line = self.get_vision_line(front_offset - side_offset, -90)
        front_right_forward_side_line = self.get_vision_line(front_offset + side_offset, 10)
        front_left_forward_side_line = self.get_vision_line(front_offset - side_offset, -10)
        rear_right_side_line = self.get_vision_line(side_offset - front_offset, 135)
        rear_left_side_line = self.get_vision_line(-1 * side_offset - front_offset, -135)

        lines = [front_line, front_right_diagonal_side_line, front_left_diagonal_side_line,
                 front_right_perpendicular_side_line, front_left_perpendicular_side_line, front_right_forward_side_line,
                 front_left_forward_side_line, rear_line, rear_right_side_line, rear_left_side_line]
        return lines

    def get_vision_line(self, offset, angle):
        offset_global = self.get_global_point(offset)
        return Line(offset_global, offset_global + (cos(radians(-self.angle + angle)) * VISION_LINE_LENGTH,
                                                    sin(radians(-self.angle + angle)) * VISION_LINE_LENGTH))
