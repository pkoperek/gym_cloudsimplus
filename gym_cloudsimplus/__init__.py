from gym.envs.registration import register

register(
    id='SingleDCAppEnv-v0',
    entry_point='gym_cloudsimplus.envs:SingleDCAppEnv',
)

register(
    id='ThreeSizeAppEnv-v0',
    entry_point='gym_cloudsimplus.envs:ThreeSizeAppEnv',
)
