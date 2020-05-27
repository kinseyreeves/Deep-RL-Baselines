import gym
from gym_scalable.envs.n_joints import NJointArm
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()

env = gym.make('n-joints-v0', config={"extra_joints": 4, "extra_state": False})
i = 0

# print(env.action_space)
# print(env.observation_space.shape)
# print(env.action_space.shape)
#
#
# print(type(env.action_space))
# print(type(env.observation_space))
# state = env.reset()
# input()
# print("shape : " , env.observation_space.shape[0])

while i < 200000:
    i += 1
    # env.render()
    input()
    action_size = env.action_space.shape[0]
    # print(action_size)
    # exit(0)
    # print(action_size)
    # print(env.action_space)
    action = env.action_space.sample()

    # print(action)
    # action[1] = 0
    # print(action)
    # for i in range
    state, reward, done, _ = env.step(action)
    # print(state)
    env.render()
    # print(i)
    # print("reward : ", reward)
    # print(state)
    env.render()
    if (done):
        # print("done")
        # a = input()
        env.reset()

        env.render()

tracker.print_diff()
