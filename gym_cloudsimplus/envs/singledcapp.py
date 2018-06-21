import gym
from gym import error, spaces, utils
from gym.utils import seeding
from py4j.java_gateway import JavaGateway

import numpy as np

# Available actions
ACTION_NOTHING = 0
ACTION_ADD_VM = 1
ACTION_REMOVE_VM = 2

gateway = JavaGateway()
simulation_environment = gateway.entry_point


# Based on https://github.com/openai/gym/blob/master/gym/core.py
class SingleDCAppEnv(gym.Env):
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self):
        # actions are identified by integers 0-n
        self.num_of_actions = 2
        self.action_space = spaces.Discrete(self.num_of_actions)

        # format of observations - delta in current step
        # 1. number of VMs - up to 1000
        # 2. p99 latency - max 5000 ms
        # 3. p90 latency - max 5000 ms
        # 4. Average CPU utilization
        # 5. p90 CPU utilization
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0]),
            high=np.array([1000, 5000, 5000, 100, 100])
        )

    def step(self, action):
        result = simulation_environment.step(action)
        obs = result.getObs()
        reward = result.getReward()
        done = result.isDone()
        return (
            obs,
            reward,
            done,
            {}
        )

    def reset(self):
        simulation_environment.reset()

    def render(self, mode='human', close=False):
        result = simulation_environment.render()
        if mode == 'human':
            print(result)
        elif mode != 'ansi' and mode != 'human':
            return super().render(mode)

        return result

    def close(self):
        # close the resources
        simulation_environment.close()

    def seed(self):
        simulation_environment.seed()
