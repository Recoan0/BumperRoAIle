from math import sin, cos, radians

import numpy as np
from pygame.math import Vector2

from object.car.bumper_car import BumperCar
from object.vision.vision_line import VisionLine
from const.hyper_params import *


class LineVisionCar(BumperCar):
    def __init__(self, car_nr: int, spawn_angle: float, spawn_location: Vector2, color: str,
                 top_speed: float = 10., steering_speed: float = .1, acceleration: float = 100., mass: float = .1):
        super().__init__(car_nr, spawn_angle, spawn_location, color, top_speed, steering_speed, acceleration, mass)
        self.vision_lines: list[VisionLine] = []

    def get_observation(self, env) -> np.ndarray:
        self.vision_lines = self.create_vision_lines()

        # TODO: Calculate closest intersection with circle and enemies for each lines
        enemies = env.agents.sprites()
        enemies.remove(self)
        intersect_dists = [line.calculate_collisions(env, enemies) for line in self.vision_lines]
        flattened_intersect_dists = np.concatenate(intersect_dists)
        obs = np.array([self.body.angular_velocity, *self.get_relative_velocity(), *flattened_intersect_dists])
        return obs

    def create_vision_lines(self) -> list[VisionLine]:
        front_offset, side_offset = self.get_offsets()
        vision_params = self.calculate_vision_line_params(front_offset, side_offset)
        return list(map(lambda x: self.get_vision_line(*x), vision_params))

    def get_vision_line(self, offset, angle):
        offset_global = self.get_global_point(offset)
        return VisionLine(offset_global, offset_global + (cos(radians(-self.angle + angle)) * VISION_LINE_LENGTH,
                                                          sin(radians(-self.angle + angle)) * VISION_LINE_LENGTH))

    def draw_vision(self, screen) -> None:
        if self.is_alive:
            for vl in self.vision_lines:
                vl.draw(screen)

    @staticmethod
    def calculate_vision_line_params(front_offset, side_offset) -> list:
        # [front_line, front_right_diagonal_side_line, front_left_diagonal_side_line,
        #  front_right_perpendicular_side_line, front_left_perpendicular_side_line, front_right_forward_side_line,
        #  front_left_forward_side_line, rear_line, rear_right_side_line, rear_left_side_line]
        vision_params = [(front_offset, 0), (-1 * front_offset, 180), (front_offset + side_offset, 45),
                         (front_offset - side_offset, -45), (front_offset + side_offset, 90),
                         (front_offset - side_offset, -90), (front_offset + side_offset, 10),
                         (front_offset - side_offset, -10), (side_offset - front_offset, 135),
                         (-1 * side_offset - front_offset, -135)]
        return vision_params
