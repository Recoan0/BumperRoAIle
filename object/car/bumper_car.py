import os
from abc import ABC, abstractmethod
from math import sin, cos, radians

import numpy as np
import pygame
import pymunk
from pygame.color import THECOLORS
from pygame.math import Vector2
from pymunk import Vec2d

from const.hyper_params import *


class BumperCar(pygame.sprite.Sprite, ABC):
    def __init__(self, car_nr: int, spawn_angle: float, spawn_location: Vector2, color: str, top_speed=CAR.TOP_SPEED,
                 max_steer_speed=CAR.MAX_ANGULAR_VELOCITY, steering_speed=CAR.STEERING_SPEED,
                 acceleration=CAR.ACCELERATION, mass=CAR.MASS):
        super().__init__()
        self.car_nr = car_nr
        self.height, self.width = CAR.CART_SIZE
        self.top_speed = top_speed
        self.max_steer_speed = max_steer_speed
        self.steering_speed = steering_speed
        self.acceleration = acceleration
        self.mass = mass
        self.color = color
        self.angle = spawn_angle
        self.observation_space = None

        # Pymunk body and shape
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, CAR.CART_SIZE))
        self.body.position = (spawn_location.x, spawn_location.y)
        self.body.angle = -self.angle * np.pi / 180  # Convert to radians and reverse direction
        self.body.car = self  # Store reference to self for collision reward
        self.body.velocity_func = lambda body, gravity, damping, dt: \
            self.limit_velocity(body, gravity, damping, dt, self.top_speed)
        self.shape = pymunk.Poly.create_box(self.body, CAR.CART_SIZE)
        self.shape.collision_type = CAR.COLLISION_TYPE
        self.shape.elasticity = 0.5  # Adjust elasticity as needed
        self.shape.color = THECOLORS[color]

        # Pygame drawing
        self.car_image = self.load_car_image()
        self.image = pygame.transform.rotate(self.car_image, self.angle)
        self.rect = self.image.get_rect(center=spawn_location)

        self.is_alive = True
        self.last_collided_with = None
        self.step_extra_score = 0.

    def update(self, space_centre, space_radius) -> None:
        # Update the sprite's position to match the physics body
        # print(self.body.velocity.length)
        self.angle = (-self.body.angle * 180 / np.pi) % 360
        self.image = pygame.transform.rotate(self.car_image, self.angle)
        self.rect = self.image.get_rect(center=self.body.position)
        self.update_alive_status(space_centre, space_radius)

    def apply_control(self, acceleration, steering) -> None:
        if not self.is_alive: return
        # Apply forces based on control inputs
        self.body.angular_velocity = \
            np.clip(self.body.angular_velocity + steering * self.steering_speed,
                    -self.max_steer_speed, self.max_steer_speed)

        force = acceleration * self.acceleration * self.body.mass
        impulse = Vector2(force, 0).rotate(-self.body.angle)
        self.body.apply_force_at_local_point((impulse.x, impulse.y))

    def get_offsets(self):
        # Returns front_offset, side_offset
        return Vector2((cos(radians(-self.angle)) * self.height / 2, sin(radians(-self.angle)) * self.height / 2)), \
            Vector2((-sin(radians(-self.angle)) * self.width / 2, cos(radians(-self.angle)) * self.width / 2))

    def get_hitbox_lines(self):
        # Returns hitbox lines in clockwise direction
        front_offset, side_offset = self.get_offsets()
        front_line = (self.get_global_point(np.add(front_offset, side_offset)),
                      self.get_global_point(np.subtract(front_offset, side_offset)))
        right_line = (self.get_global_point(np.add(front_offset, side_offset)),
                      self.get_global_point(np.subtract(side_offset, front_offset)))
        rear_line = (self.get_global_point(np.subtract(side_offset, front_offset)),
                     self.get_global_point(np.subtract(np.negative(front_offset), side_offset)))
        left_line = (self.get_global_point(np.subtract(front_offset, side_offset)),
                     self.get_global_point(np.subtract(np.negative(side_offset), front_offset)))

        return front_line, right_line, rear_line, left_line

    def get_global_point(self, offset):
        return self.body.position + offset

    def update_alive_status(self, space_centre: Vector2, space_radius: float) -> None:
        if not self.is_alive: return
        died = not self.is_in_radius(space_centre, space_radius)
        if died:
            self.attribute_score_to_killer()
            self.add_score(SCORES.DIED)
            self.is_alive = False

    def is_in_radius(self, space_centre: Vector2, space_radius: float) -> bool:
        return (Vector2(self.body.position) - space_centre).length() < space_radius

    def attribute_score_to_killer(self) -> None:
        if self.last_collided_with:
            self.last_collided_with.add_score(SCORES.KILL)

    def add_score(self, score: float) -> None:
        self.step_extra_score += score

    def get_and_reset_extra_score(self):
        step_extra_score = self.step_extra_score
        self.step_extra_score = 0.
        return step_extra_score

    def kill(self) -> None:
        self.is_alive = False

    def get_relative_velocity(self) -> Vec2d:
        return self.body.velocity.rotated(-self.body.angle)

    def get_normalized_relative_velocity(self):
        return self.get_relative_velocity() / self.top_speed

    def get_normalized_angular_velocity(self):
        return self.body.angular_velocity / self.max_steer_speed

    def get_pymunk(self):
        return self.body, self.shape

    @staticmethod
    def limit_velocity(body, gravity, damping, dt, max_velocity):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity *= scale

    @staticmethod
    def load_car_image():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path).convert_alpha()
        car_image = pygame.transform.scale(car_image, CAR.CART_SIZE)
        return car_image

    @abstractmethod
    def draw_vision(self, screen) -> None:
        return
