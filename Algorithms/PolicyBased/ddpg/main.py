import gym
import numpy as np
import agent
import gym_scalable
from tensorboardX import SummaryWriter
import time
import pandas as pd
import sys

"""
DDPG implementation using pytorch
Based on Deepminds paper continuous control 
Kinsey Reeves
2020
usage : 
python main.py {extra_joints} 
for an arm with 1 free joint (2 joints)
"""

checkpoint = 5

BATCH_SIZE = 16
N_EPISODES = 2000

MAX_EP_STEPS = 250

HIDDEN_SIZE = 200

VAR_MIN = 0.08
VAR_RED = 0.99995

ACTOR_UPDATE = 1
CRITIC_UPDATE = 1
checkpoint = 2
writer = SummaryWriter(logdir="../runs/" + "DDPG" + time.strftime("%Y%m%d-%H%M%S"))


def run(extra_joints=1):
    out_df = pd.DataFrame(columns=["total_steps", "episode_rewards", "episode_len"])

    rewards = []
    avg_rewards = []
    ep_steps = []
    ep_rewards = []
    total_steps = 0
    all_steps = []
    extra_j = 1
    env = gym.make('n-joints-v0', config = {"extra_joints":extra_joints, "extra_state":False})

    # action_size = env.action_space.shape[0]
    # state_size = env.observation_space.shape[0]
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.shape[0]
    ddpg_agent = agent.DDPGAgent(state_size, action_size, hidden_size=HIDDEN_SIZE)
    # memory = util.ReplayMemory()
    # noise = util.OUNoise(env.action_space)
    # print(env.observation_space.shape )

    var = 2
    ep_n = 0
    while True:
        state = env.reset()
        episode_reward = 0
        # noise.reset()

        for step in range(MAX_EP_STEPS + 1):
            total_steps+=1
            action = ddpg_agent.get_action(state)[0]
            action = np.clip(np.random.normal(action, var), -1, 1)

            # input()
            new_state, reward, done, _ = env.step(action)
            ddpg_agent.memory.push(state, action, reward, new_state, done)

            if len(ddpg_agent.memory) > BATCH_SIZE:
                var *= VAR_RED
                var = max(VAR_MIN, var)
                ddpg_agent.update(BATCH_SIZE)
                if total_steps % ACTOR_UPDATE == 0:
                    ddpg_agent.upate_actor_target()
                if total_steps % CRITIC_UPDATE == 0:
                    ddpg_agent.update_critic_target()

            state = new_state
            episode_reward += reward
            #env.render()
            # if ep_n > 100:
            #    env.render()

            if done or step == MAX_EP_STEPS:
                ep_n +=1
                writer.add_scalar('ddpg/ep_reward', episode_reward, ep_n)
                print(f"Episode {ep_n}, finished:  {done}, reward : {episode_reward:.2f}, LR : {var:.2f} {total_steps}")
                all_steps.append(total_steps)
                ep_steps.append(step)
                ep_rewards.append(episode_reward)
                out_df = out_df.append({"total_steps":total_steps, "episode_rewards":episode_reward, "episode_len":step}, ignore_index=True)

                break

            rewards.append(episode_reward)
            avg_rewards.append(np.mean(rewards[-10:]))

        if(ep_n % checkpoint == 0):
            #print(out_df)
            print("Saving data")

            out_df.to_csv(f"{extra_joints}_df.csv")


run(extra_joints=int(sys.argv[1]))
