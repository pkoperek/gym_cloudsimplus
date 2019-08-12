import gym
import gym_cloudsimplus
import json

from read_swf import jobs

env = gym.make('SingleDCAppEnv-v0',
               initial_vm_count="10",
               jobs_as_json=json.dumps(jobs),
               simulation_speedup="1000",
               split_large_jobs="true",
               )

env.reset()

it = 0
reward_sum = 0
while True:
    observation, reward, done, info = env.step(0)
    print(f'{it}, {observation}, {reward}')
    reward_sum += reward

    it += 1
    if done:
        print("Episode finished! Reward sum: {reward_sum}")
        break
