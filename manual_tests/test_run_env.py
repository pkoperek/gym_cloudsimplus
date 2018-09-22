import gym
import gym_cloudsimplus

env = gym.make('SingleDCAppEnv-v0')
env.reset()
for _ in range(5):
    rendered = env.render(mode='array')
    print("Rendered env length: " + str(len(rendered)) + " " + str(type(rendered)))

    observation, reward, done, info = env.step(env.action_space.sample())

    if done:
        print("Episode finished!")
        break
