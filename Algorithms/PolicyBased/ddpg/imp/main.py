import sys
import gym
import numpy as np
import pandas as pd
import agent
import util
import gym_scalable

BATCH_SIZE = 16
N_EPISODES = 500

MAX_EP_STEPS = 200

HIDDEN_SIZE = 256

def run():
    rewards = []
    avg_rewards = []

    #env = util.NormalizedEnv(gym.make("Pendulum-v0"))
    #env = gym.make("Pendulum-v0")
    extra_j = 2
    env = gym.make('n-joints-v0', extra_joints=extra_j)

    #action_size = env.action_space.shape[0]
    #state_size = env.observation_space.shape[0]
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.shape[0]
    ddpg_agent = agent.DDPGAgent(state_size, action_size, hidden_size=HIDDEN_SIZE)
    #memory = util.ReplayMemory()
    noise = util.OUNoise(env.action_space)
    #print(env.observation_space.shape )
    var = 2

    for ep_n in range(0, N_EPISODES):
        state = env.reset()
        episode_reward = 0
        noise.reset()

        for step in range(MAX_EP_STEPS+1):
            action = ddpg_agent.get_action(state)[0]
            action = np.clip(np.random.normal(action,var),-1,1)
            var*=0.995
            var = max(0.01, var)

            #print(action)

            #action2 = ddpg_agent.get_action(state)
            #print(action)
            #action = noise.get_action(action,step)

            #input()
            #ADD NOISE
            #input()
            new_state, reward, done, _ = env.step(action)
            #print("here")

            ddpg_agent.memory.push(state, action, reward, new_state, done)

            if len(ddpg_agent.memory) > BATCH_SIZE:
                ddpg_agent.update(BATCH_SIZE)

            state = new_state
            episode_reward += reward
            if(ep_n>200):
                env.render()

            if(done or step == MAX_EP_STEPS):
                print("episode {} reward : {} \n".format(ep_n, episode_reward))
                print(done)

            rewards.append(episode_reward)
            avg_rewards.append(np.mean(rewards[-10:]))


run()