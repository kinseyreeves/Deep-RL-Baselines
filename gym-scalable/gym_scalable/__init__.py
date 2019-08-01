from gym.envs.registration import register

register(
    id='n-joints-v0',
    entry_point='gym_scalable.envs:NJointArm',
)


register(
    id='n-evaders-v0',
    entry_point='gym_scalable.envs:EvadersEnv',
)



register(
    id='n-traffic-v0',
    entry_point='gym_scalable.envs:TrafficEnv',
)


# register(
#     id='n-chasers-v0',
#     entry_point='gym_scalable.envs:Chasers',
# )

