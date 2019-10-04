import torch.nn as nn
import torch
import torch.nn.functional as F
from collections import deque
import util
import torch.optim as optim
from torch.autograd import Variable


class Critic(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Critic, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, 100)
        self.linear3 = nn.Linear(100, 1)

        # torch.nn.init.xavier_uniform(self.linear1.weight)
        # torch.nn.init.xavier_uniform(self.linear2.weight)
        # torch.nn.init.xavier_uniform(self.linear3.weight)
        # self.linear1.bias.data.fill_(0.01)
        # self.linear2.bias.data.fill_(0.01)
        # self.linear3.bias.data.fill_(0.01)

    def forward(self, state, action):
        """
        Params state and actions are torch tensors
        """
        x = torch.cat([state, action], 1)
        x = F.relu6(self.linear1(x))
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
        self.l22 = nn.Linear(hidden_size, 100)
        self.l3 = nn.Linear(100, output_size)

        # torch.nn.init.xavier_uniform(self.l1.weight)
        # torch.nn.init.xavier_uniform(self.l2.weight)
        # torch.nn.init.xavier_uniform(self.l22.weight)
        # torch.nn.init.xavier_uniform(self.l3.weight)
        # self.l1.bias.data.fill_(0.001)
        # self.l2.bias.data.fill_(0.001)
        # self.l22.bias.data.fill_(0.001)
        # self.l3.bias.data.fill_(0.001)

    def forward(self, state):

        x = F.relu6(self.l1(state))
        x = F.relu6(self.l2(x))
        x = F.relu(self.l22(x))
        x = F.tanh(self.l3(x))
        x = torch.clamp(x,-1,1)
        return x


class DDPGAgent():
    def __init__(self, state_size,
                 action_size,hidden_size=256,
                 a_lr = 1e-4,c_lr = 1e-4,
                 gamma=0.99,tau=0.001,
                 max_memory_size=5000):

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
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=self.a_lr)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr = self.c_lr)
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
        #print(Qvals.shape)
        # input()
        next_actions = self.actor_target.forward(states_)
        next_Q = self.critic_target.forward(states_, next_actions.detach())
        Qprime = rewards + self.gamma * next_Q
        #print(Qprime.shape)
        critic_loss = self.critic_criterion(Qvals, Qprime)
        #a = input()

        # Actor loss
        policy_loss = -self.critic.forward(states, self.actor.forward(states)).mean()

        # update networks
        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()

        #Update critic
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

    def upate_actor_target(self):
        self.tau = 0
        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))
            #target_param.data.copy_(param.data)

    def update_critic_target(self):
        self.tau = 0
        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            #target_param.data.copy_(param.data)
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))


        #Actor loss

        #Update networks


        #Update t