import numpy as np
from matplotlib import pyplot as plt


class BumperCar:
    def __init__(self, top_speed: float, steering_speed: float, acceleration: float,
                 mass: float, spawn_angle: float, spawn_location: (float, float)):
        self.top_speed = top_speed
        self.steering_speed = steering_speed
        self.acceleration = acceleration
        self.mass = mass

        self.velocity = (0, 0)
        self.angle = spawn_angle
        self.location = spawn_location

    def apply_control(self, control):
        raise NotImplementedError()

    def apply_force(self, force):
        raise NotImplementedError()
