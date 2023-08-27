import gym
import gym_cloudsimplus
import json
import sys
import random

from read_swf import jobs

if len(sys.argv) > 1:
    initial_vm_count = sys.argv[1]
else:
    initial_vm_count = '1'

env = gym.make('ThreeSizeAppEnv-v0',
               initial_vm_count=initial_vm_count,
               jobs_as_json=json.dumps(jobs),
               simulation_speedup="60",
               split_large_jobs="true",
               )


def episode():
    env.reset()

    it = 0
    reward_sum = 0
    while True:
        action = random.randint(0, 6)
        observation, reward, done, info = env.step(action)
        print(f'{it}, {[str(i) for i in observation]}, {reward}')
        reward_sum += reward

        it += 1
        if done:
            print(f"Episode finished! Reward sum: {reward_sum}")
            break


if __name__ == "__main__":

    for i in range(1000):
        print(f">>>>>>>>>>>>>>>>> Episode ${i} <<<<<<<<<<<<<<<<<<<")
        episode()
