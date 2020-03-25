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
    id='n-grid_evaders-v0',
    entry_point='gym_scalable.envs:GridEvaderEnv',
)

register(
    id='n-pathing-v0',
    entry_point='gym_scalable.envs:PathingEnv',
)

register(
    id='n-maze-v0',
    entry_point='gym_scalable.envs:MazeEnv',
)


register(
    id='n-grid_chaser-vs-evader-v0',
    entry_point='gym_scalable.envs:GridChaserVsEvaderEnv',
)
