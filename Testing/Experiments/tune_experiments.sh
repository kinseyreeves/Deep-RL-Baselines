python reacher_experiments.py --rl DQN --extra_joints 4 --steps 50000 --tune_search

python maze_experiments.py --rl DQN --extra_joints 4 --steps 50000 --tune_search

python maze_experiments.py --rl PPO --name tune_grid --random_goals --random_start --1reward --num_goals 3 --map_size 5 --steps 50000 --tune_search