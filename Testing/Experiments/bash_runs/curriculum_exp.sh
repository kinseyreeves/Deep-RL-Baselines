/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 3 --curriculum
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 7 --curriculum
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 9 --curriculum

/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune --random_goals --random_start --num_goals 3 --encoding st --map_size 3 --curriculum
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune --random_goals --random_start --num_goals 3 --encoding st --map_size 5 --curriculum
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune --random_goals --random_start --num_goals 3 --encoding st --map_size 7 --curriculum
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune --random_goals --random_start --num_goals 3 --encoding st --map_size 9 --curriculum


