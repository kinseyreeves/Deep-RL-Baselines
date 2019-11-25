import torch
import gym
import agent
import util
import time
import numpy as np
import gym_scalable
from tensorboardX import SummaryWriter

#from gym.envs.box2d.bipedal_walker import BipedalWalker

MAX_EP_STEPS = 250

def run():
    writer = SummaryWriter(logdir="../runs/" + "PPO" + time.strftime("%Y%m%d-%H%M%S"))

    render = False
    solved_reward = 300  # stop training if avg_reward > solved_reward
    log_interval = 1  # print avg reward in the interval
    max_episodes = 10000  # max training episodes

    update_timestep = 4000  # update policy every n timesteps
    action_std = 0.5  # constant std for action distribution (Multivariate Normal)
    K_epochs = 80  # update policy for K epochs
    eps_clip = 0.2  # clip parameter for PPO
    gamma = 0.99  # discount factor

    lr = 0.0003  # parameters for Adam optimizer
    betas = (0.9, 0.999)

    random_seed = None
    #############################################

    # creating environment
    #env = gym.make('BipedalWalker-v2')
    extra_j = 1
    env = gym.make('n-joints-v0', extra_joints=extra_j)

    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]

    print(state_dim)
    print(action_dim)

    if random_seed:
        print("Random Seed: {}".format(random_seed))
        torch.manual_seed(random_seed)
        env.seed(random_seed)
        np.random.seed(random_seed)

    memory = util.ReplayMemory()
    ppo = agent.PPOAgent(state_dim, action_dim, action_std, lr, betas, gamma, K_epochs, eps_clip)
    print(lr, betas)

    # logging variables
    running_reward = 0
    avg_length = 0
    time_step = 0

    # training loop
    for i_episode in range(1, max_episodes + 1):
        state = env.reset()
        ep_reward = 0
        for t in range(MAX_EP_STEPS):
            time_step += 1
            # Running policy_old:
            action = ppo.select_action(state, memory)
            state, reward, done, _ = env.step(action)
            ep_reward += reward

            # Saving reward and is_terminals:

            memory.rewards.append(reward)
            memory.is_terminals.append(done)

            # update if its time
            if time_step % update_timestep == 0:
                ppo.update(memory)
                memory.clear_memory()
                time_step = 0
            running_reward += reward
            if render:
                env.render()
            if done:
                break

        avg_length += t

        if i_episode % log_interval == 0:
            avg_length = int(avg_length / log_interval)
            running_reward = int((running_reward / log_interval))
            writer.add_scalar("ppo/ep_reward", ep_reward, i_episode)

            #print('Episode {} \t Avg length: {} \t Avg reward: {}'.format(i_episode, avg_length, running_reward))
            print(f"Ep : {i_episode}, Reward : {ep_reward} ")
            running_reward = 0
            avg_length = 0

run()