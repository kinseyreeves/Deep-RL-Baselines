

#python maze_experiments.py --steps 1000000 --1reward --name 3goals_capture_reward_200max --num_goals 3
#Fixed goals, fixed start
#python maze_experiments.py --steps 200000 --name encoded_3goals_1_reward_on_goal_200max --1reward --num_goals 3
#python maze_experiments.py --steps 200000 --name encoded_3goals_neg01_reward_on_goal_200max --num_goals 3

#random goals, random start
#python maze_experiments.py --steps 200000 --name encoded_3goals_1reward_on_goal_rgoal_rstart --1reward --random_goals --random_start --num_goals 3

###### Reacher Experiments ##########

python reacher_experiments.py --rl DDPG --extra_joints 1 --steps 100000
python reacher_experiments.py --rl DDPG --extra_joints 2 --steps 100000
python reacher_experiments.py --rl DDPG --extra_joints 4 --steps 100000

python reacher_experiments.py --rl TD3 --extra_joints 1 --steps 100000
python reacher_experiments.py --rl TD3 --extra_joints 2 --steps 100000
python reacher_experiments.py --rl TD3 --extra_joints 4 --steps 100000

python reacher_experiments.py --rl PPO --extra_joints 1 --steps 100000
python reacher_experiments.py --rl PPO --extra_joints 2 --steps 100000
python reacher_experiments.py --rl PPO --extra_joints 4 --steps 100000


##### MAZE EXPERIMENTS ################

#Maze 5x5 ALL ALGORITHMS
#python maze_experiments.py --rl PPO --steps 500000 --name 1r_rsrg_5g_500k_smenc --random_goals --random_start --1reward --num_goals 5
#python maze_experiments.py --rl PG --steps 500000 --name 1r_rsrg_5g_500k_smenc --random_goals --random_start --1reward --num_goals 5
#python maze_experiments.py --rl A2C --steps 500000 --name 1r_rsrg_5g_500k_smenc --random_goals --random_start --1reward --num_goals 5
#python maze_experiments.py --rl DQN --steps 500000 --name 1r_rsrg_5g_500k_smenc --random_goals --random_start --1reward --num_goals 5

#maze experiments with changing number of goals
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 1
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 2
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 4
#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 8
######
#python maze_experiments.py --rl DQN --steps 100000 --name DQN_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward

#python maze_experiments.py --rl PPO --steps 1000000 --name PPO_1reward_rstart_rgoal_1msteps_nwenc --random_goals --random_start --1reward
#python maze_experiments.py --rl DQN --steps 1000000 --name DQN_1reward_rstart_rgoal_1msteps_nwenc --random_goals --random_start --1reward
#python maze_experiments.py --rl A2C --steps 1000000 --name A2C_1reward_rstart_rgoal_1msteps_nwenc --random_goals --random_start --1reward

#Maze experiments curriculum
#python maze_experiments.py --rl PPO --steps 500000 --name 1r_rsrg_5g_500k_nw_curr50 --random_goals --random_start --1reward --num_goals 5 --curriculum --curriculum_eps 50
#python maze_experiments.py --rl PPO --steps 500000 --name 1r_rsrg_5g_500k_nw_curr100 --random_goals --random_start --1reward --num_goals 5 --curriculum --curriculum_eps 100
#python maze_experiments.py --rl PPO --steps 500000 --name 1r_rsrg_5g_500k_nw_curr200 --random_goals --random_start --1reward --num_goals 5 --curriculum --curriculum_eps 200
#
#python maze_experiments.py --rl PPO --steps 500000 --name 1r_rsrg_5g_500k_nw_curr50 --random_goals --random_start --1reward --num_goals 5 --curriculum --curriculum_eps 50
#python maze_experiments.py --rl PPO --steps 500000 --name 1r_rsrg_5g_500k_nw_curr100 --random_goals --random_start --1reward --num_goals 5 --curriculum --curriculum_eps 100
#python maze_experiments.py --rl PPO --steps 500000 --name 1r_rsrg_5g_500k_nw_curr200 --random_goals --random_start --1reward --num_goals 5 --curriculum --curriculum_eps 200

#########CHASER EVADER EXPERIMENTS##########
##
#####CHASER, EACH ALGORITHM
python chaser_evader_experiments.py --rl PPO --steps 500000 --name PPO_chaser_rsrg_500k_smenc --random_goals --random_start
python chaser_evader_experiments.py --rl DQN --steps 500000 --name DQN_chaser_rsrg_500k_smenc --random_goals --random_start
python chaser_evader_experiments.py --rl A2C --steps 500000 --name A2C_chaser_rsrg_500k_smenc --random_goals --random_start
python chaser_evader_experiments.py --rl APEX-DQN --steps 500000 --name APEX-DQN_chaser_rsrg_500k_smenc --random_goals --random_start
python chaser_evader_experiments.py --rl PG --steps 500000 --name PG_chaser_rsrg_1msteps_smenc --random_goals --random_start

#####EVADER, EACH ALGORITHM
python chaser_evader_experiments.py --rl PPO --steps 500000 --name chaser_rsrg_500k_smenc --random_goals --random_start --rl_evader
python chaser_evader_experiments.py --rl DQN --steps 500000 --name chaser_rsrg_500k_smenc --random_goals --random_start --rl_evader
python chaser_evader_experiments.py --rl A2C --steps 500000 --name chaser_rsrg_500k_smenc --random_goals --random_start --rl_evader
python chaser_evader_experiments.py --rl APEX-DQN --steps 500000 --name APEX-DQN_chaser_rsrg_500k_smenc --random_goals --random_start --rl_evader
python chaser_evader_experiments.py --rl PG --steps 500000 --name PG_chaser_rsrg_500k_smenc --random_goals --random_start --rl_evader

#python reacher_experiments.py

#python chaser_evader_experiments.py
#python evader_experiments.py
#python chaser_vs_evader_experiments.py
