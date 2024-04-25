import numpy as np
import pygame
import pymunk
import os
from pygame.color import THECOLORS
from pygame.math import Vector2
from math import floor


CART_SIZE = (50, 30)


class BumperCar(pygame.sprite.Sprite):
    def __init__(self, spawn_angle: float, spawn_location: Vector2, color: str,
                 top_speed: float = 10., steering_speed: float = .1, acceleration: float = 100., mass: float = .1):
        super().__init__()
        self.top_speed = top_speed
        self.steering_speed = steering_speed
        self.acceleration = acceleration
        self.mass = mass
        self.color = color
        self.angle = spawn_angle

        # Pymunk body and shape
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, CART_SIZE))
        self.body.position = spawn_location.x, spawn_location.y
        self.body.angle = -self.angle * np.pi / 180  # Convert to radians and reverse direction
        self.shape = pymunk.Poly.create_box(self.body, CART_SIZE)
        self.shape.elasticity = 0.5  # Adjust elasticity as needed
        # self.shape.friction = 0.5  # Adjust friction as needed
        self.shape.color = THECOLORS[color]

        # Pygame drawing
        self.car_image = self.load_car_image()
        self.image = pygame.transform.rotate(self.car_image, self.angle)
        self.rect = self.image.get_rect(center=spawn_location)

        self.is_alive = True

    def update(self, space_centre, space_radius) -> None:
        # Update the sprite's position to match the physics body
        self.angle = (-self.body.angle * 180 / np.pi) % 360
        self.image = pygame.transform.rotate(self.car_image, self.angle)
        self.rect = self.image.get_rect(center=self.body.position)
        self.is_alive = self.is_alive and self.is_in_radius(space_centre, space_radius)

    def apply_control(self, acceleration, steering) -> None:
        if not self.is_alive: return
        # Apply forces based on control inputs
        self.body.angular_velocity = \
            np.clip(self.body.angular_velocity + steering * self.steering_speed, -2, 2)

        force = acceleration * self.acceleration * self.body.mass
        impulse = Vector2(force, 0).rotate(-self.body.angle)
        self.body.apply_force_at_local_point((impulse.x, impulse.y))

    def get_observation(self) -> np.ndarray:
        return np.array([0])  # TODO

    def is_in_radius(self, space_centre: Vector2, space_radius: float) -> bool:
        print((Vector2(self.body.position) - space_centre).length(), space_radius)
        return (Vector2(self.body.position) - space_centre).length() < space_radius

    def kill(self) -> None:
        self.is_alive = False

    def get_pymunk(self):
        return self.body, self.shape

    @staticmethod
    def load_car_image():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path).convert_alpha()
        car_image = pygame.transform.scale(car_image, CART_SIZE)
        return car_image
