#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 3 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 7 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 9 --curriculum --curriculum_eps 100

#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 3 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 7 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 9 --curriculum --curriculum_eps 100

#5x5 only
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 50
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 200
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 400

/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 50
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 200
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 400

#control maze
/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_control --random_goals --random_start --1reward --num_goals 3 --map_size 5
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_control --random_goals --random_start --num_goals 3 --map_size 5


#chaser evader

