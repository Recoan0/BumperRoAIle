import numpy as np
import pygame
import pymunk
from pygame.color import THECOLORS
from pygame.math import Vector2


CART_SIZE = (50, 30)


class BumperCar(pygame.sprite.Sprite):
    def __init__(self, spawn_angle: float, spawn_location: Vector2, color: str,
                 top_speed: float = 10., steering_speed: float = 1., acceleration: float = 3., mass: float = 1.):
        super().__init__()
        self.top_speed = top_speed
        self.steering_speed = steering_speed
        self.acceleration = acceleration
        self.mass = mass
        self.color = color

        # Pymunk body and shape
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, (50, 30)))
        self.body.position = spawn_location.x, spawn_location.y
        self.body.angle = -spawn_angle * np.pi / 180  # Convert to radians and reverse direction
        self.shape = pymunk.Poly.create_box(self.body, (50, 30))
        self.shape.elasticity = 0.5  # Adjust elasticity as needed
        self.shape.friction = 0.5  # Adjust friction as needed
        self.shape.color = THECOLORS[color]

        # Pygame drawing
        self.image = pygame.Surface((50, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=spawn_location)

        self.is_alive = True

    def update(self) -> None:
        # Update the sprite's position to match the physics body
        self.rect.center = self.body.position
        self.image = pygame.transform.rotate(pygame.Surface((50, 30)), -self.body.angle * 180 / np.pi)
        self.image.fill(self.shape.color)

    def apply_control(self, steering, acceleration) -> None:
        # Apply forces based on control inputs
        self.body.angular_velocity -= steering * self.steering_speed

        force = acceleration * self.acceleration * self.body.mass
        impulse = Vector2(force, 0).rotate_rad(-self.body.angle)
        self.body.apply_impulse_at_local_point((impulse.x, impulse.y))

    def get_observation(self) -> np.ndarray:
        return np.array([0])  # TODO

    def kill(self) -> None:
        self.is_alive = False

