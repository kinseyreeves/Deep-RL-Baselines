import gym
import gym_simple


env = gym.make('simple-v0')

while True:

    env.render()
    action = 1
    
    env.step(action)
    a = input()

