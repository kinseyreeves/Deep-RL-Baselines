# import argparse
#
#
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--steps', type=int)
# parser.add_argument('--1reward', dest='reward', action='store_true')
# parser.add_argument('--goals', type = int)
#
#
# args = parser.parse_args()
# print(args.steps)
# print(args.reward)
# print(args.goals)
#
import gym
import gym_minigrid.wrappers
import gym_minigrid
from gym_minigrid.wrappers import FullyObsWrapper


env = gym.make('MiniGrid-Empty-5x5-v0')
env = FullyObsWrapper(env)

s = env.reset()

i = 0
while i < 100:

    env.render()
    action = env.action_space.sample()
    obs, r, done, _ = env.step(action)
    print(obs)
    input()
print(s)
