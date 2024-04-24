import numpy as np
import pygame
import pymunk
import gymnasium as gym

from pygame.math import Vector2
from bumper_car import BumperCar
from hyper_params import *


class BumperRoAIle(gym.Env):
    def __init__(self, n_agents=N_AGENTS, start_radius=START_RADIUS, shrink_speed=SHRINK_SPEED, fps=FPS):
        super(BumperRoAIle, self).__init__()

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(AREA_SIZE)
        pygame.display.set_caption("Bumper Car Battle Royale")
        self.clock = pygame.time.Clock()

        # Setup env
        self.n_agents = n_agents
        self.radius = start_radius
        self.shrink_speed = shrink_speed
        self.draw = True
        self.fps = fps

        # Define mappings for acceleration based on control ranges
        self.acceleration_mapping = {0: 1, 1: 0, 2: -.5}
        self.steering_mapping = {0: -1, 1: 0, 2: 1}

        # Setup Pymunk (physics)
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.agents = pygame.sprite.Group()
        self.arena_center = Vector2(AREA_CENTRE)
        self.current_radius = start_radius

        # Set Gym Variables
        self.action_space = gym.spaces.Discrete(ACTIONS)
        self.observation_space = gym.spaces.Box(low=0, high=800, shape=(n_agents * 2,), dtype=np.float32)

    def reset(self, **kwargs) -> np.ndarray:
        self.agents = pygame.sprite.Group()
        self.current_radius = self.radius

        # Initialize agents
        for color in range(self.n_agents):
            car = self.create_car(color)
            self.space.add(*car.get_pymunk())
            self.agents.add(car)

        # Return initial observation
        return self.get_observations()

    def step(self, actions):
        assert len(actions) == len(self.agents), f"Need {len(self.agents)} actions, got {len(actions)}"
        # Apply actions, update pymunk space, handle shrinking, calculate rewards, etc.
        controls = list(map(lambda action: self.map_control(action), actions))
        [car.apply_control(control[0], control[1]) for car, control in zip(self.agents, controls)]

        self.agents.update()
        self.shrink_circle()
        self.space.step(1. / self.fps)

        if self.draw:
            self.render()

        self.clock.tick(self.fps)  # Limit the frame rate to FPSs

        # Return observation, reward, done, infos
        done = np.sum(self.get_alives()) > 1
        return self.get_observations(), self.get_rewards(), done, {}

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear the screen with black

        # Draw the shrinking arena
        pygame.draw.circle(self.screen, (255, 255, 255),
                           self.arena_center, int(self.current_radius), 1)

        # Draw each agent
        self.agents.draw(self.screen)

        pygame.display.flip()  # Update the full display Surface to the screen

        # Handle window events (e.g., close the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

    def map_control(self, control):
        # Compute acceleration and steering
        acceleration = self.acceleration_mapping[control // 3]
        steering = self.steering_mapping[control % 3]

        return acceleration, steering

    def shrink_circle(self):
        self.current_radius -= self.shrink_speed / self.fps

    def get_observations(self) -> np.ndarray:
        return np.array(list(map(lambda agent: agent.get_observation(), self.agents)))

    def get_rewards(self) -> np.ndarray:
        return self.get_alives() * 2 - 1  # TODO

    def get_alives(self) -> np.ndarray:
        return np.array(list(map(lambda agent: agent.is_alive, self.agents)))

    def create_car(self, color: int) -> BumperCar:
        angle = np.random.uniform(0, 360)
        offset = Vector2(*np.random.uniform(-self.radius * 0.9, self.radius * 0.9, 2))
        location = Vector2(AREA_CENTRE) + Vector2(offset)
        return BumperCar(angle, location, COLORS[color])

    def close(self):
        # Clean up Pygame or other graphical resources
        pygame.quit()


class ManualPlayer:
    TICKS = 60

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.tracks = []

    def run(self):
        game = BumperRoAIle(n_agents=1)
        game.reset()
        done = False
        while not done:
            pressed = pygame.key.get_pressed()
            action = self.keys_to_choice(pressed)
            print(action)
            _ = game.step([action])
            game.render()

    @staticmethod
    def keys_to_choice(pressed):
        if pressed[pygame.K_UP]:
            if pressed[pygame.K_LEFT]:
                return 0
            elif pressed[pygame.K_RIGHT]:
                return 2
            else:
                return 1
        elif pressed[pygame.K_DOWN]:
            if pressed[pygame.K_LEFT]:
                return 6
            elif pressed[pygame.K_RIGHT]:
                return 8
            else:
                return 7
        else:
            if pressed[pygame.K_LEFT]:
                return 3
            elif pressed[pygame.K_RIGHT]:
                return 5
            else:
                return 4


def main():
    env = BumperRoAIle()
    env.reset()
    done = False
    while not done:
        env.step([0] * N_AGENTS)


def manual_main():
    ManualPlayer().run()


if __name__ == "__main__":
    # main()
    manual_main()
