from math import sin, cos, radians
from skspatial.objects import Line, Circle
from pygame.math import Vector2
import pygame
import numpy as np
from const.hyper_params import *


class VisionLine:
    def __init__(self, start_point: Vector2, angle: float, length: float,
                 normalized_distance=True, color=(255, 255, 255), opacity=96):
        self.start_point = start_point
        self.angle = angle
        self.end_offset = Vector2(cos(radians(angle)) * length, sin(radians(angle)) * length)
        self.end_point = start_point + self.end_offset
        self.length = length
        self.normalized_distance = normalized_distance
        self.allowed_draw_distance = 1 if normalized_distance else CAR.VISION_LINE_LENGTH
        self.line = Line.from_points(self.start_point, self.end_point)
        self.color = color
        self.opacity = opacity
        self.enemy_collision_distance = 0.
        self.enemy_collision_point = None
        self.circle_collision_distance = 0.
        self.circle_collision_point = None

    def calculate_collisions(self, env, enemies):
        self.enemy_collision_distance, self.enemy_collision_point = self.calculate_nearest_enemy_collision(enemies)
        self.circle_collision_distance, self.circle_collision_point = self.calculate_nearest_circle_collision(env)
        if self.normalized_distance:
            self.enemy_collision_distance /= self.length + 1
            self.circle_collision_distance /= self.length + 1
        return self.enemy_collision_distance, self.circle_collision_distance

    def update_with_offset(self, new_start_point, new_angle):
        self.start_point = new_start_point
        self.angle = new_angle
        self.end_offset = Vector2(cos(radians(new_angle)) * self.length,
                                  sin(radians(new_angle)) * self.length)
        self.end_point = new_start_point + self.end_offset
        self.line = Line.from_points(self.start_point, self.end_point)
        pass

    def calculate_nearest_enemy_collision(self, enemies):
        return min([self.get_enemy_collision_distance(enemy) for enemy in enemies])

    def calculate_nearest_circle_collision(self, env):
        point_a, point_b = self.calc_circle_intersect(env)
        if point_a is None or point_b is None:
            return self.length + 1, None
        direction = Vector2(self.end_point - self.start_point)
        vec2a, vec2b = (Vector2(*point_a) - self.start_point), (Vector2(*point_b) - self.start_point)
        if direction.dot(vec2a) > 0:
            a_dist = vec2a.length()
            return (a_dist, point_a) if a_dist <= self.length else (self.length + 1, None)
        else:
            b_dist = vec2b.length()
            return (b_dist, point_b) if b_dist <= self.length else (self.length + 1, None)

    def get_enemy_collision_distance(self, enemy):
        hitbox_lines = enemy.get_hitbox_lines()
        intersects = [self.calc_line_intersect(line) for line in hitbox_lines]
        distances = [self.calc_distance_to(intersect) for intersect in intersects]
        return min(zip(distances, intersects))

    def draw(self, screen):  # Call after self.calculate_collisions()
        pygame.draw.line(screen, self.color + (self.opacity,), self.start_point, self.end_point)
        if self.enemy_collision_point is not None and self.enemy_collision_distance <= self.allowed_draw_distance:
            pygame.draw.circle(screen, COLORS.RED, self.enemy_collision_point, 5)
        if self.circle_collision_point is not None and self.circle_collision_distance <= self.allowed_draw_distance:
            pygame.draw.circle(screen, COLORS.PURPLE, self.circle_collision_point, 5)

    def calc_circle_intersect(self, env):
        circle = Circle(env.arena_center, env.current_radius)
        try:
            point_a, point_b = circle.intersect_line(self.line)
        except ValueError:
            return None, None
        return point_a, point_b

    def calc_line_intersect(self, other_line):
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        x3, y3 = other_line[0]
        x4, y4 = other_line[1]
        if (x4 - x3) * (y1 - y2) - (x1 - x2) * (y4 - y3) == 0:
            return None
        t1 = ((y3 - y4) * (x1 - x3) + (x4 - x3) * (y1 - y3)) / ((x4 - x3) * (y1 - y2) - (x1 - x2) * (y4 - y3))
        t2 = ((y1 - y2) * (x1 - x3) + (x2 - x1) * (y1 - y3)) / ((x4 - x3) * (y1 - y2) - (x1 - x2) * (y4 - y3))

        if 0 <= t1 <= 1 and 0 <= t2 <= 1:
            return (x1, y1) + np.multiply(t1, tuple(np.subtract((x2, y2), (x1, y1))))
        else:
            return None

    def calc_distance_to(self, point) -> float:
        return (Vector2(*point) - Vector2(self.start_point)).length() if point is not None else self.length + 1
