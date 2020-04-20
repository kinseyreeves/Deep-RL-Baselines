

#python maze_experiments.py --steps 1000000 --1reward --name 3goals_capture_reward_200max --num_goals 3
#Fixed goals, fixed start
#python maze_experiments.py --steps 200000 --name encoded_3goals_1_reward_on_goal_200max --1reward --num_goals 3
#python maze_experiments.py --steps 200000 --name encoded_3goals_neg01_reward_on_goal_200max --num_goals 3

#random goals, random start
#python maze_experiments.py --steps 200000 --name encoded_3goals_1reward_on_goal_rgoal_rstart --1reward --random_goals --random_start --num_goals 3

##### MAZE EXPERIMENTS #####


######
##TODO maze experiments with changing number of goals
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 1
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 2
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 4
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 8
######

python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward
python maze_experiments.py --rl DQN --steps 1000000 --name DQN_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward

#######CHASER EVADER EXPERIMENTS##########

###CHASER, EACH ALGORITHM
python chaser_evader_experiments.py --rl PPO --steps 1000000 --name PPO_chaser_rstart_rgoal_1msteps --random_goals --random_start
python chaser_evader_experiments.py --rl DQN --steps 1000000 --name DQN_chaser_rstart_rgoal_1msteps --random_goals --random_start
python chaser_evader_experiments.py --rl A3C --steps 1000000 --name A3C_chaser_rstart_rgoal_1msteps --random_goals --random_start

###EVADER, EACH ALGORITHM
python chaser_evader_experiments.py --rl PPO --steps 1000000 --name PPO_chaser_rstart_rgoal_1msteps --random_goals --random_start --rl_evader
python chaser_evader_experiments.py --rl DQN --steps 1000000 --name DQN_chaser_rstart_rgoal_1msteps --random_goals --random_start --rl_evader
python chaser_evader_experiments.py --rl A3C --steps 1000000 --name A3C_chaser_rstart_rgoal_1msteps --random_goals --random_start --rl_evader



#python reacher_experiments.py

#python chaser_evader_experiments.py
#python evader_experiments.py
#python chaser_vs_evader_experiments.py
