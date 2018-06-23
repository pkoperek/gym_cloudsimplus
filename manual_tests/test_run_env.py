import gym
import gym_cloudsimplus

env = gym.make('SingleDCAppEnv-v0')
env.reset()
for _ in range(5):
    env.render()
    observation, reward, done, info = env.step(env.action_space.sample())

    if done:
        print("Episode finished!")
        break
