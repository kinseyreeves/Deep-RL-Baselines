import os
import time

from gym_scalable.envs.grid.maps import map_loader
from gym_scalable.envs.grid.multi_chaser_evader_env import GridChaserVsEvaderEnv

print(os.getcwd())
env = GridChaserVsEvaderEnv(
    config={"mapfile": map_loader.get_8x8_map(), "RL_evader": False, "full_state": False, "normalize_state": True})

state = env.reset()
i = 0
goal = env.grid.goal

while True:
    i += 1
    env.render()

    action1 = env.action_space.sample()
    action2 = env.action_space.sample()

    state, reward, done, _ = env.step(actions={"evader": action1, "chaser": action2})

    print(f"state :  {state}")
    print(f"reward : {reward}")
    print(f"done : {done}")

    # print(env.normalize_state)
    if (done["__all__"]):
        env.reset()

    # input()
    time.sleep(0.1)
