import gym
import os
import json
from gym import spaces
from py4j.java_gateway import JavaGateway, GatewayParameters

import numpy as np

# Available actions
ACTION_NOTHING = 0
ACTION_ADD_SMALL_VM = 1
ACTION_REMOVE_SMALL_VM = 2
ACTION_ADD_MEDIUM_VM = 3
ACTION_REMOVE_MEDIUM_VM = 4
ACTION_ADD_LARGE_VM = 5
ACTION_REMOVE_LARGE_VM = 6

buffer_size = int(os.getenv('HISTORYENV_HISTORY_SIZE', "128"))
address = os.getenv('CLOUDSIM_GATEWAY_HOST', 'cloudsimplus-gateway')
port = os.getenv('CLOUDSIM_GATEWAY_PORT', '25333')
parameters = GatewayParameters(address=address,
                               port=int(port),
                               auto_convert=True)
gateway = JavaGateway(gateway_parameters=parameters)
simulation_environment = gateway.entry_point


def to_string(java_array):
    return gateway.jvm.java.util.Arrays.toString(java_array)


# Based on https://github.com/openai/gym/blob/master/gym/core.py
# This app reports a history of last `buffer_size` metric observations as an array
class HistoryAppEnv(gym.Env):
    metadata = {'render.modes': ['human', 'ansi', 'array']}

    def __init__(self, **kwargs):
        # actions are identified by integers 0-n
        self.num_of_actions = 7
        self.action_space = spaces.Discrete(self.num_of_actions)

        # observation metrics - all within 0-1 range
        # "vmAllocatedRatioHistory",
        # "avgCPUUtilizationHistory",
        # "p90CPUUtilizationHistory",
        # "avgMemoryUtilizationHistory",
        # "p90MemoryUtilizationHistory",
        # "waitingJobsRatioGlobalHistory",
        # "waitingJobsRatioRecentHistory"
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(buffer_size, 7, 1),
            dtype=np.float32,
        )
        params = {
            'INITIAL_VM_COUNT': kwargs.get('initial_vm_count'),
            'SOURCE_OF_JOBS': 'PARAMS',
            'JOBS': kwargs.get('jobs_as_json', '[]'),
            'SIMULATION_SPEEDUP': kwargs.get('simulation_speedup', '1.0'),
            'SPLIT_LARGE_JOBS': kwargs.get('split_large_jobs', 'false'),
        }

        if 'queue_wait_penalty' in kwargs:
            params['QUEUE_WAIT_PENALTY'] = kwargs['queue_wait_penalty']

        self.simulation_id = simulation_environment.createSimulation(params)
        self._clear_history_buffer()

    def _clear_history_buffer(self):
        self.history_buffer = np.zeros(shape=(buffer_size, 7, 1), dtype=np.float32)

    def step(self, action):
        if type(action) == np.int64:
            action = action.item()
        result = simulation_environment.step(self.simulation_id, action)
        reward = result.getReward()
        done = result.isDone()
        raw_obs = result.getObs()
        self._add_to_buffer(raw_obs)

        return (
            self.history_buffer,
            reward,
            done,
            {}
        )

    def _add_to_buffer(self, raw_obs):
        raw_obs_lst = list(raw_obs)
        self.history_buffer = np.append(
            self.history_buffer[1:],
            [
                [
                    [observation]
                    for observation
                    in raw_obs_lst
                ]
            ],
            axis=0
        )

    def reset(self):
        result = simulation_environment.reset(self.simulation_id)
        self._clear_history_buffer()
        raw_obs = result.getObs()
        self._add_to_buffer(raw_obs)

        return self.history_buffer

    def render(self, mode='human', close=False):
        # result is a string with arrays encoded as json
        result = simulation_environment.render(self.simulation_id)
        arr = json.loads(result)
        if mode == 'ansi' or mode == 'human':
            if mode == 'human':
                print([ser[-1] for ser in arr])

            return result
        elif mode == 'array':
            return arr
        elif mode != 'ansi' and mode != 'human':
            return super().render(mode)

    def close(self):
        # close the resources
        simulation_environment.close(self.simulation_id)

    def seed(self):
        simulation_environment.seed(self.simulation_id)
