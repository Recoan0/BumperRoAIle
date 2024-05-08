import numpy as np
import torch

from network import FeedForwardNN


class PPOAgent:
    def __init__(self, observation_space, action_space):
        self.observation_space = observation_space
        self.action_space = action_space
        self.actor = FeedForwardNN(observation_space.shape, action_space.shape)
        self.critic = FeedForwardNN(observation_space.shape, 1)

    def get_action(self, obs) -> np.ndarray:
        return None

    def rollout(self):
        batch_obs = []  # batch observations
        batch_acts = []  # batch actions
        batch_log_probs = []  # log probs of each action
        batch_rews = []  # batch rewards
        batch_rtgs = []  # batch rewards-to-go
        batch_lens = []  # episodic lengths in batch
