from agent.ppo_agent import PPOAgent
from environment.bumper_roaile import BumperRoAIle
from const.hyper_params import *

class Manager:
    def __init__(self, n_agents, agent_types=PPOAgent, timesteps_per_batch=MANAGER.TIMESTEPS_PER_BATCH,
                 max_timesteps_per_episode=MANAGER.MAX_TIMESTEPS_PER_EPISODE):
        self.n_agents = n_agents
        self.env = BumperRoAIle(n_agents)
        self.agents = self.init_agents(agent_types, self.env.observation_space, self.env.action_space)
        self.max_timesteps_per_episode = max_timesteps_per_episode
        self.timesteps_per_batch = timesteps_per_batch

    def learn(self, total_timesteps):
        dt = 0

        while dt < total_timesteps:
            return

    def init_agents(self, agent_types, observation_space, action_space):
        if isinstance(agent_types, list):
            return [agent_type(observation_space, action_space) for agent_type in agent_types]
        else:
            return [agent_types(observation_space, action_space)] * self.n_agents
