#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 3 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 7 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_tune_full --random_start --1reward --num_goals 3 --encoding st --map_size 9 --curriculum --curriculum_eps 100

#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 3 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 7 --curriculum --curriculum_eps 100
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_tune_full --random_start --num_goals 3 --encoding st --map_size 9 --curriculum --curriculum_eps 100

# #5x5 only
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum_50 --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 50
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum_100 --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum_200 --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 200
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name 5x5_curriculum_400 --random_start --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 400

# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum_50 --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 50
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum_100 --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 100
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum_200 --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 200
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name 5x5_curriculum_400 --random_start --1reward --num_goals 3 --encoding st --map_size 5 --curriculum --curriculum_eps 400

# #control maze
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name curriculum_control --random_goals --random_start --1reward --num_goals 3 --map_size 5
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name curriculum_control --random_goals --random_start --num_goals 3 --map_size 5


# #chaser evader
# #Chaser
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 10
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 50
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 100
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 200

/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 10
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 50
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 100
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_curriculum --random_goals --random_start --curriculum --curriculum_eps 200

#Evader
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 10
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 50
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 100
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 200

/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 10
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 50
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 100
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_curriculum --random_goals --random_start --rl_evader --curriculum --curriculum_eps 200


#Controls
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_curriculum_cont --random_goals --random_start --rl_evader
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_curriculum_cont --random_goals --random_start --rl_evader

/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_curriculum_cont --random_goals --random_start
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_curriculum_cont --random_goals --random_start

