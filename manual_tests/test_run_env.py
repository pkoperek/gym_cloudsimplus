import gym
import gym_cloudsimplus

env = gym.make('SingleDCAppEnv-v0', initial_vm_count="10")
env.reset()
for _ in range(5):
    rendered = env.render(mode='array')
    print("Rendered env length: " + str(len(rendered)) + " " + str(type(rendered)))
    print(rendered)

    for lst in rendered:
        print(len(lst))

    observation, reward, done, info = env.step(env.action_space.sample())

    if done:
        print("Episode finished!")
        break
