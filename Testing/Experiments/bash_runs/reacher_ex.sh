
################################# Reacher Experiments #####################################


#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 1

#TEST all algorithms all joints


#/usr/bin/timeout 1800s python reacher_experiments.py --rl DDPG --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl DDPG --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl DDPG --extra_joints 4
#
#/usr/bin/timeout 1800s python reacher_experiments.py --rl TD3 --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl TD3 --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl TD3 --extra_joints 4
#
#/usr/bin/timeout 1800s python reacher_experiments.py --rl PPO --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl PPO --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl PPO --extra_joints 4
#
#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 4


python reacher_experiments.py --rl DDPG --extra_joints 2 --name reacher_rllib --tune_search --steps 40000
python reacher_experiments.py --rl TD3 --extra_joints 2 --name reacher_rllib --tune_search --steps 40000
python reacher_experiments.py --rl PPO --extra_joints 2 --name reacher_rllib --tune_search --steps 100000
python reacher_experiments.py --rl A2C --extra_joints 2 --name reacher_rllib --tune_search --steps 100000

