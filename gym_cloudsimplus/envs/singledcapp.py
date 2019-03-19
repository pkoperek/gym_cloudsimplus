import gym
import os
import json
from gym import spaces
from py4j.java_gateway import JavaGateway, GatewayParameters

import numpy as np

# Available actions
ACTION_NOTHING = 0
ACTION_ADD_VM = 1
ACTION_REMOVE_VM = 2

address = os.getenv('CLOUDSIM_GATEWAY_HOST', 'cloudsimplus-gateway')
port = os.getenv('CLOUDSIM_GATEWAY_PORT', '25333')
parameters = GatewayParameters(address=address, port=int(port))
gateway = JavaGateway(gateway_parameters=parameters)
simulation_environment = gateway.entry_point


def to_string(java_array):
    return gateway.jvm.java.util.Arrays.toString(java_array)


def to_nparray(raw_obs):
    obs = []
    for serie in raw_obs:
        obs.extend(list(serie))

    return np.array(obs)


# Based on https://github.com/openai/gym/blob/master/gym/core.py
class SingleDCAppEnv(gym.Env):
    metadata = {'render.modes': ['human', 'ansi', 'array']}

    def __init__(self):
        # actions are identified by integers 0-n
        self.num_of_actions = 3
        self.action_space = spaces.Discrete(self.num_of_actions)

        # format of observations - delta in current step
        # 1. number of VMs - up to 1000
        # 2. p99 latency - max 5000 ms
        # 3. p90 latency - max 5000 ms
        # 4. Average CPU utilization
        # 5. p90 CPU utilization
        # 6. total wait time
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0]),
            high=np.array([99999, 9999999, 9999999, 100, 100, 9999999])
        )

    def step(self, action):
        result = simulation_environment.step(action)
        reward = result.getReward()
        done = result.isDone()
        raw_obs = result.getObs()

        obs = to_nparray(raw_obs)
        return (
            obs,
            reward,
            done,
            {}
        )

    def reset(self):
        result = simulation_environment.reset()
        raw_obs = result.getObs()
        obs = to_nparray(raw_obs)
        return obs

    def render(self, mode='human', close=False):
        # result is a string with arrays encoded as json
        result = simulation_environment.render()
        if mode == 'human' or mode == 'ansi':
            if mode == 'human':
                print("Measurements: ")
                print(result)

            return result
        elif mode == 'array':
            return json.loads(result)
        elif mode != 'ansi' and mode != 'human':
            return super().render(mode)

    def close(self):
        # close the resources
        simulation_environment.close()

    def seed(self):
        simulation_environment.seed()
