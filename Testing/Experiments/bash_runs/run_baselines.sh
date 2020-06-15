
#Final A2C

#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 1 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 2 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 4 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 6 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 8 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 10 --encoding st --map_size 5
#
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_maze_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 3
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_maze_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 4
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_maze_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_maze_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 6
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_maze_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 7
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_maze_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 8

#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 1 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 2 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 4 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 6 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 8 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_goal_changing --random_goals --random_start --1reward --num_goals 10 --encoding st --map_size 5
#
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name A2C_maze_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 3
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 4
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 5
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 6
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 7
#/usr/bin/timeout 1800s python ../maze_experiments.py --rl A2C --name PPO_goal_changing --random_goals --random_start --1reward --num_goals 3 --encoding st --map_size 8



#Final Reacher baseline

#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl DDPG --extra_joints 1
#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl DDPG --extra_joints 2
#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl DDPG --extra_joints 4

#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl TD3 --extra_joints 1
#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl TD3 --extra_joints 2
#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl TD3 --extra_joints 4
#
#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl PPO --extra_joints 1
#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl PPO --extra_joints 2
#/usr/bin/timeout 1800s python ../reacher_experiments.py --rl PPO --extra_joints 4

#Chaser evader
#Evader

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name evader_final --random_goals --random_start --rl_evader --map_size 3

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name evader_final --random_goals --random_start --rl_evader --map_size 5

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name evader_final --random_goals --random_start --rl_evader --map_size 7

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name evader_final --random_goals --random_start --rl_evader --map_size 9

#Chaser

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name chaser_final --random_goals --random_start --map_size 3

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name chaser_final --random_goals --random_start --map_size 5

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name chaser_final --random_goals --random_start --map_size 7

/usr/bin/timeout 1800s python ../chaser_evader_experiments.py --rl A2C --name chaser_final --random_goals --random_start --map_size 9



