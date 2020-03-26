from stable_baselines.common.env_checker import check_env
import gym_scalable
import gym



env = gym.make('n-joints-v0',  config = {"extra_joints": 5, "extra_state": False})

print(check_env(env))

