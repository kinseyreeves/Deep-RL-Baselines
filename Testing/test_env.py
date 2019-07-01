import gym




env = gym.make("CartPole-v1")
observation_space = env.observation_space.shape[0]
action_space = env.action_space.n

env.reset()

while True:

    env.render()
    state_next, reward, terminal, info = env.step(0)
    
    if terminal:
        env.reset