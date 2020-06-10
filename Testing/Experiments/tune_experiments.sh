#python reacher_experiments.py --rl DDPG --extra_joints 4 --steps 50000 --tune_search
# python reacher_experiments.py --rl PPO --extra_joints 4 --steps 250000 --tune_search

python maze_experiments.py --rl DQN --name tune_grid_DQN --random_goals --random_start --1reward --num_goals 3 --map_size 5 --steps 50000 --tune_search
#python maze_experiments.py --rl PPO --name tune_grid --random_goals --random_start --1reward --num_goals 3 --map_size 5 --steps 100000 --tune_search
