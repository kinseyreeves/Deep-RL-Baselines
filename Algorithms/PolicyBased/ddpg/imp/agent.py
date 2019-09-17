import torch.nn as nn
import torch
import torch.nn.functional as F
from collections import deque
import util
import torch.optim as optim
from torch.autograd import Variable


BATCH_SIZE = 128


class Critic(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Critic, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, state, action):
        """
        Params state and actions are torch tensors
        """
        #print(state.shape)
        #print(action.shape)

        x = torch.cat([state, action], 1)

        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x


class Actor(nn.Module):
    """
    Inputs the state and returns the action
    """

    def __init__(self, input_size, hidden_size, output_size, lr=3e-4):
        super(Actor, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l22 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, output_size)

    def forward(self, state):
        x = F.relu(self.l1(state))
        x = F.relu(self.l2(x))
        x = F.relu(self.l22(x))
        x = F.tanh(self.l3(x))
        return x


class DDPGAgent():
    def __init__(self, state_size,
                 action_size,hidden_size=256,
                 a_lr = 1e-4,c_lr = 1e-4,
                 gamma=0.99,tau=1e-2,
                 max_memory_size=50000):

        self.state_size = state_size
        self.action_size = action_size
        self.hidden_size = hidden_size

        self.a_lr = a_lr
        self.c_lr = c_lr
        self.gamma = gamma
        self.tau = tau

        #Networks
        self.actor = Actor(self.state_size, hidden_size, self.action_size)
        self.actor_target = Actor(self.state_size, hidden_size, self.action_size)
        self.critic = Critic(self.state_size + self.action_size, hidden_size, self.action_size)
        self.critic_target = Critic(self.state_size + self.action_size, hidden_size, self.action_size)

        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data)

        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data)

        self.memory = util.ReplayMemory(max_memory_size)

        #Training

        self.critic_criterion = nn.MSELoss()
        self.actor_optimizer = optim.RMSprop(self.actor.parameters(), lr=self.a_lr)
        self.critic_optimizer = optim.RMSprop(self.critic.parameters(), lr = self.c_lr)
        #optim.RMSprop()

    def get_action(self, state):
        state_var = Variable(torch.from_numpy(state).float().unsqueeze(0))
        action = self.actor.forward(state_var)
        action = action.detach().numpy()
        return action

    def update(self, batch_size):

        states, actions, rewards, states_, _ = self.memory.sample(batch_size)
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        rewards = torch.FloatTensor(rewards)
        states_ = torch.FloatTensor(states_)

        # Critic loss
        Qvals = self.critic.forward(states, actions)
        # print(Qvals)
        # input()
        next_actions = self.actor_target.forward(states_)
        next_Q = self.critic_target.forward(states_, next_actions.detach())
        Qprime = rewards + self.gamma * next_Q
        critic_loss = self.critic_criterion(Qvals, Qprime)

        # Actor loss
        policy_loss = -self.critic.forward(states, self.actor.forward(states)).mean()

        # update networks
        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Soft network updates
        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))

        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))


        #Actor loss

        #Update networks


        #Update t