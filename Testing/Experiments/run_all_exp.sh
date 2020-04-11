#python maze_experiments.py --steps 1000000 --1reward --name 3goals_capture_reward_200max --num_goals 3
#Fixed goals, fixed start
python maze_experiments.py --steps 500 --name 3goals_1_reward_on_goal_200max --1reward --num_goals 3
#python maze_experiments.py --steps 500 --name 3goals_neg01_reward_on_goal_200max --num_goals 3

#random goals, random start
#python maze_experiments.py --steps 500 --name 3goals_1reward_on_goal_rgoal_rstart --1reward --random_goals --random_start --num_goals 3
# maze_experiments.py --steps 500 --name 3goals_neg01_reward_on_goal_rgoal_rstart --random_goals --random_start --num_goals 3



# python reacher_experiments.py

#python chaser_experiments.py
#python evader_experiments.py
#python chaser_vs_evader_experiments.py
