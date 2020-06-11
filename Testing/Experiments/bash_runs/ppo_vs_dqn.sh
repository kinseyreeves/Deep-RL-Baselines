##maze experiments with changing number of goals

##DQN vs PPO changing number of goals
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 1 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 2 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 4 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 6 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 8 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 10 --encoding st
#
#
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_goal_changing --random_goals --random_start --num_goals 1 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_goal_changing --random_goals --random_start --num_goals 2 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_goal_changing --random_goals --random_start --num_goals 4 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_goal_changing --random_goals --random_start --num_goals 6 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_goal_changing --random_goals --random_start --num_goals 8 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_goal_changing --random_goals --random_start --num_goals 10 --encoding st
#
#
##PPO vs DQN changing maze size
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_maze_changing --random_goals --random_start --1reward --num_goals 3 --map_size 3
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_maze_changing --random_goals --random_start --1reward --num_goals 3 --map_size 5
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_maze_changing --random_goals --random_start --1reward --num_goals 3 --map_size 7
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name PPO_maze_changing --random_goals --random_start --1reward --num_goals 3 --map_size 9
#
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_maze_changing --random_goals --random_start --num_goals 3 --map_size 3
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_maze_changing --random_goals --random_start --num_goals 3 --map_size 5
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_maze_changing --random_goals --random_start --num_goals 3 --map_size 7
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name DQN_maze_changing --random_goals --random_start --num_goals 3 --map_size 9
#
#
