


################################# Reacher Experiments #####################################


#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 1

#TEST all algorithms all joints


#/usr/bin/timeout 1800s python reacher_experiments.py --rl DDPG --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl DDPG --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl DDPG --extra_joints 4
#/usr/bin/timeout 1800s python reacher_experiments.py --rl DDPG --extra_joints 8
#
#/usr/bin/timeout 1800s python reacher_experiments.py --rl TD3 --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl TD3 --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl TD3 --extra_joints 4
#/usr/bin/timeout 1800s python reacher_experiments.py --rl TD3 --extra_joints 8
#
#/usr/bin/timeout 1800s python reacher_experiments.py --rl PPO --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl PPO --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl PPO --extra_joints 4
#/usr/bin/timeout 1800s python reacher_experiments.py --rl PPO --extra_joints 8
#
#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 1
#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 2
#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 4
#/usr/bin/timeout 1800s python reacher_experiments.py --rl A2C --extra_joints 8

#Test gaussian vs OU noise

#TEST todo hyperparam tuning

#TEST population based learning
#python maze_experiments.py --rl PPO --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 1

##### ################### MAZE EXPERIMENTS ##########################################

######TEST  Maze ALL ALGORITHMS all encodings experiment changing encodings

# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding pos
# /usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding pos
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding pos

#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding w
#/usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding w
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding w

# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding nw
# /usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding nw
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding nw

# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name encoding_test --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st

##TEST Fixed vs random states
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name rsrg --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding nw
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name fsfg --1reward --num_goals 3 --map_size 5 --encoding nw

#TEST -ve 1 reward vs 1 reward
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name rsrg --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding nw
#/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name rsrg --random_goals --random_start --num_goals 3 --map_size 5 --encoding nw

/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name neg_reward --random_goals --random_start --num_goals 3 --map_size 5 --encoding st
/usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name neg_reward --random_goals --random_start --num_goals 3 --map_size 5 --encoding st
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name neg_reward --random_goals --random_start --num_goals 3 --map_size 5 --encoding st

/usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name pos_reward --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st
/usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name pos_reward --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st
/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name pos_reward --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st


#python maze_experiments.py --rl PPO --name PPO_1reward_rstart_rgoal_1msteps --random_goals --random_start --1reward --num_goals 1

##BASELINE MAZE experiments with changing number of goals
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name stacked_changinggoals --random_goals --random_start --1reward --num_goals 1 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name stacked_changinggoals --random_goals --random_start --1reward --num_goals 2 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name stacked_changinggoals --random_goals --random_start --1reward --num_goals 4 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name stacked_changinggoals --random_goals --random_start --1reward --num_goals 6 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name stacked_changinggoals --random_goals --random_start --1reward --num_goals 8 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name stacked_changinggoals --random_goals --random_start --1reward --num_goals 10 --encoding st

#MAZE ALL ALGS 
# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name basline_ch_maze_size --random_goals --random_start --1reward --num_goals 3 --map_size 3 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name basline_ch_maze_size --random_goals --random_start --1reward --num_goals 3 --map_size 3 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name basline_ch_maze_size --random_goals --random_start --1reward --num_goals 3 --map_size 3 --encoding st

# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name all_algs_initial --random_goals --random_start --1reward --num_goals 3 --map_size 4 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name all_algs_initial --random_goals --random_start --1reward --num_goals 3 --map_size 4 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name all_algs_initial --random_goals --random_start --1reward --num_goals 3 --map_size 4 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl PG --name all_algs_initial --random_goals --random_start --1reward --num_goals 3 --map_size 4 --encoding st

# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name basline_ch_maze_size --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name basline_ch_maze_size --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name basline_ch_maze_size --random_goals --random_start --1reward --num_goals 3 --map_size 5 --encoding st

# /usr/bin/timeout 1800s python maze_experiments.py --rl PPO --name basline_ch_maze_size_u --random_goals --random_start --1reward --num_goals 3 --map_size 6 --encoding st
# /usr/bin/timeout 1800s python maze_experiments.py --rl A2C --name basline_ch_maze_size_u --random_goals --random_start --1reward --num_goals 3 --map_size 6 --encoding st
#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --name basline_ch_maze_size_u --random_goals --random_start --1reward --num_goals 3 --map_size 6 --encoding st


#/usr/bin/timeout 1800s python maze_experiments.py --rl DQN --steps 100000 --name DQN_full_parameter_grid --random_goals --random_start --1reward


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
# #####CHASER, EACH ALGORITHM
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 3
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 3
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 3

# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 4
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 4
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 4

# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 5
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 5
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 5

# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 6
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 6
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name chaser_st_encoding --random_goals --random_start --encoding st --map_size 6

# ######EVADER, EACH ALGORITHM
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_st_encoding --random_goals --random_start --encoding st --map_size 3 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_st_encoding --random_goals --random_start --encoding st --map_size 3 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name evader_st_encoding --random_goals --random_start --encoding st --map_size 3 --rl_evader

# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_st_encoding --random_goals --random_start --encoding st --map_size 4 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_st_encoding --random_goals --random_start --encoding st --map_size 4 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name evader_st_encoding --random_goals --random_start --encoding st --map_size 4 --rl_evader

# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_st_encoding --random_goals --random_start --encoding st --map_size 5 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_st_encoding --random_goals --random_start --encoding st --map_size 5 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name evader_st_encoding --random_goals --random_start --encoding st --map_size 5 --rl_evader

# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name evader_st_encoding --random_goals --random_start --encoding st --map_size 6 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl DQN --name evader_st_encoding --random_goals --random_start --encoding st --map_size 6 --rl_evader
# /usr/bin/timeout 1800s python chaser_evader_experiments.py --rl A2C --name evader_st_encoding --random_goals --random_start --encoding st --map_size 6 --rl_evader

#python reacher_experiments.py

#python chaser_evader_experiments.py
#python evader_experiments.py
#python chaser_vs_evader_experiments.py
