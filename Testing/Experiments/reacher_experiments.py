import argparse
import rllib_trainers
from gym_scalable.envs.n_joints import NJointArm
from ray import tune
from ray.tune import grid_search

parser = argparse.ArgumentParser(description='Reacher experiment runner')

parser.add_argument('--extra_joints', type=int, default=1)
parser.add_argument('--rl', type=str, default="DDPG")
parser.add_argument('--steps', type=int, default=1000)
parser.add_argument('--tune_search', dest='tune_search', action='store_true', default=False)


args = parser.parse_args()

def nj_runner(trainer, name, nj):
    tune.run(trainer,
             config={"env": NJointArm,
                     'lr': grid_search([0.0001]),
                     # "exploration_config": {"type": "GaussianNoise"},
                     'model': {
                         # 'fcnet_hiddens': grid_search([[128, 128], [256,256]])
                         'fcnet_hiddens': [256, 256],
                     },
                     "env_config":
                         {"extra_joints": nj,
                          "full_state": False,
                          "normalize_state": True}},
             checkpoint_freq=10, checkpoint_at_end=True,
             #stop={"timesteps_total": args.steps},
             name=f"{nj}-joints-{name}")

def tune_ddpg_nj_runner(trainer, name, nj):
    tune.run(trainer,
             config={"env": NJointArm,
                     "buffer_size": grid_search([500, 5000, 10000]),
                     "prioritized_replay": grid_search([True, False]),
                     "tau": grid_search([0, 0.001, 0.002]),
                     "train_batch_size": grid_search([128, 256, 512]),

                     "env_config": {"extra_joints": nj, "full_state": False, "normalize_state": True}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": args.steps},
             name=f"{nj}-tune-joints-{name}", )

def tune_td3_nj_runner(trainer, name, nj):
    tune.run(trainer,
             config={"env": NJointArm,
                     "buffer_size": grid_search([500, 5000, 10000]),
                     "prioritized_replay": grid_search([True, False]),
                     "tau": grid_search([0, 0.001, 0.002]),
                     "train_batch_size": grid_search([128, 256, 512]),

                     "env_config": {"extra_joints": nj, "full_state": False, "normalize_state": True}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": args.steps},
             name=f"{nj}-tune-joints-{name}", )

def tune_ppo_nj_runner(trainer, name, nj):

    tune.run(trainer,
             config={"env": NJointArm,
                     "use_critic": grid_search([True, False]),
                     "clip_param": grid_search([0.1, 0.3, 0.5]),
                     "kl_target": grid_search([0.005, 0.01]),

                     'model': {
                         'fcnet_hiddens': grid_search([[128, 128], [256, 256], [512, 512]])
                     },
                     "env_config": {"extra_joints": nj, "full_state": False, "normalize_state": True}},
             checkpoint_freq=10, checkpoint_at_end=True,
             # stop={"timesteps_total": args.steps},
             name=f"{nj}-tune-joints-{name}",)

trainer = rllib_trainers.get_trainer(args.rl)

###Experiments
name = args.rl
joints = args.extra_joints

if(args.tune_search):
    if(args.rl == "DDPG"):
        tune_ddpg_nj_runner(trainer, name, joints)
    if(args.rl == "TD3"):
        tune_td3_nj_runner(trainer, name,joints)
    if(args.rl == "PPO"):
        tune_ppo_nj_runner(trainer, name, joints)
else:
    nj_runner(trainer,name,joints)
