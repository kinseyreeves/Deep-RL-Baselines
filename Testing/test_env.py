import gym




env = gym.make("CartPole-v1")
observation_space = env.observation_space.shape[0]
action_space = env.action_space.n

env.reset()

print(env.observation_space)
print(type(env.observation_space))
while True:

    env.render()
    state_next, reward, terminal, info = env.step(0)

    print(reward)
    
    if terminal:
        print(reward)
        print("here")
        env.reset()