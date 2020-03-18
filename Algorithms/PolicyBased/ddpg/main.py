import gym
import numpy as np
import agent
import gym_scalable
from tensorboardX import SummaryWriter
import time


BATCH_SIZE = 16
N_EPISODES = 2000

MAX_EP_STEPS = 250

HIDDEN_SIZE = 200

VAR_MIN = 0.08
VAR_RED = 0.99995

ACTOR_UPDATE = 1
CRITIC_UPDATE = 1

writer = SummaryWriter(logdir="../runs/" + "DDPG" + time.strftime("%Y%m%d-%H%M%S"))


def run():
    rewards = []
    avg_rewards = []

    extra_j = 1
    env = gym.make('n-joints-v0')

    # action_size = env.action_space.shape[0]
    # state_size = env.observation_space.shape[0]
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.shape[0]
    ddpg_agent = agent.DDPGAgent(state_size, action_size, hidden_size=HIDDEN_SIZE)
    # memory = util.ReplayMemory()
    # noise = util.OUNoise(env.action_space)
    # print(env.observation_space.shape )

    var = 2
    total_steps = 0

    for ep_n in range(0, N_EPISODES):
        state = env.reset()
        episode_reward = 0
        # noise.reset()

        for step in range(MAX_EP_STEPS + 1):
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
            #if ep_n > 200:
            #    env.render()

            if done or step == MAX_EP_STEPS:
                writer.add_scalar('ddpg/ep_reward', episode_reward, ep_n)
                print(f"Episode {ep_n}, finished:  {done}, reward : {episode_reward:.2f}, LR : {var:.2f}")
                break

            rewards.append(episode_reward)
            avg_rewards.append(np.mean(rewards[-10:]))

run()
