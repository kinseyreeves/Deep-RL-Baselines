import gym
import n_joints


env = gym.make('n-joints-v0')
i=0
while True:
    i+=1
    env.render()
    action = 1
    
    env.step(action)
    a = input()
    if(i%50==0):
        env.reset()


