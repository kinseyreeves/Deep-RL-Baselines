import gym_scalable
import gym
import numpy as np
import time
import math
import pandas as pd
THRESH = 10
dist_per_update = 60
N_EPS = 10000

def get_state_data(state, nj):
    obj = state[0:2]
    joint_poss = state[2:((nj + 1) * 2)]
    eff_pos = state[((nj + 1) * 2):((nj + 1) * 2) + 2]
    joint_angs = state[((nj + 1) * 2) + 2:]
    obj -= np.asarray([200, 200])
    eff_pos -= np.asarray([200, 200])
    for i in range(0, len(joint_poss), 2):
        joint_poss[i] -= 200
        joint_poss[i + 1] -= 200

    return obj, joint_poss, joint_angs, eff_pos


def get_jacobian(nj, eff_coords, joints):
    """
    Gets the jacobian matrix
    :param nj:
    :param eff_coords:
    :param joints:
    :return:
    """
    kUnitVec = np.array([[0, 0, 1]], dtype=np.float)
    jacobian = np.zeros((3, (nj + 1)), dtype=np.float)
    eff_coords = np.concatenate((eff_coords, [0]))
    eff_coords = np.reshape(eff_coords, (3, 1))

    joints = np.reshape(joints, (2, nj + 1), order='F')
    joints = np.vstack([joints, np.zeros(nj + 1)])

    for i in range(0, nj + 1):
        currentJointCoords = joints[:, [i]]

        jacobian[:, i] = np.cross(
            kUnitVec, (eff_coords - currentJointCoords).reshape(3, ))

    return jacobian

#Run tests
out_df = pd.DataFrame()
for test in range(7, 10):
    extra_j = 7
    env = gym.make('n-joints-v0', config={"extra_joints": extra_j, "extra_state": True})
    # f.write(str(extra_j) + ",")
    act_size = env.action_space.shape[0]
    steps = 0
    all_steps = []
    #f = open(f"results_{test}.txt", "w+")

    ep = 0
    while ep < 100:
        state = env.reset()
        done = False
        rewards = []
        for step in range(0, 1000):
            obj_pos, joint_poss, joint_angs, eff_pos = get_state_data(state, extra_j + 1)
            if done:
                state = env.reset()
                #f.write(str(step) + "," + str(np.mean(rewards)) + "\n")
                if(step!=401):
                    all_steps.append(step)
                    ep+=1
                break

            targ_vec = np.concatenate((obj_pos - eff_pos, [0]))
            print(targ_vec)

            targ_vec = np.reshape(targ_vec, (3, 1))
            targ_unit_vec = targ_vec / np.linalg.norm(targ_vec)

            deltaR = dist_per_update * targ_unit_vec
            J = get_jacobian(extra_j, eff_pos, joint_poss)
            print(J)
            JInv = np.linalg.pinv(J)
            deltaTheta = JInv.dot(deltaR)
            dt_action = np.reshape(deltaTheta, (extra_j + 1,))
            action = np.clip(dt_action, -1, 1)

            if (math.sqrt((obj_pos[0] - eff_pos[0]) ** 2 + (obj_pos[1] - eff_pos[1]) ** 2)) < THRESH:
                action *= 0

            env.render()
            time.sleep(0.01)
            state, reward, done, _ = env.step(action)
            # print(reward)
            rewards.append(reward)
            # print(rewards)
            time.sleep(0.001)
            input()
            # print("here")

    #f.write("\n")
    out_df[f"{test}joints"] = all_steps
for col in out_df:
    print(col)
    print(np.mean(out_df[col]))
out_df.to_csv("all_joints_df.csv")

