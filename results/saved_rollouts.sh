
#./rollout.py encoded_chaser_1r_rsrg_1ms/5x5/PPO_chaser_rstart_rgoal_1msteps-5x5-PPO/PPO_GridEvaderEnv_0_2020-04-17_17-53-51w_sxtxel/checkpoint_250/checkpoint-250 --run PPO --env chaser5x5 --steps 10000



#./rollout.py encoded_chaser_1r_rsrg_1ms/5x5/PPO_chaser_rstart_rgoal_1msteps-5x5-PPO/PPO_GridEvaderEnv_0_2020-04-17_17-53-51w_sxtxel/checkpoint_250/checkpoint-250 --run PPO --env chaser5x5 --steps 10000
#./rollout.py encoded_chaser_1r_rsrg_1ms/5x5/PPO_chaser_rstart_rgoal_1msteps-5x5-PPO/PPO_GridEvaderEnv_0_2020-04-17_17-53-51w_sxtxel/checkpoint_250/checkpoint-250 --run PPO --env chaser5x5 --steps 10000


#Maze 1m steps rsrg 5x5 PPO


#Maze 1m steps rsrg 5x5 PPO



#Grid Evader 1m steps rsrg training on 5x5 PPO
#./rollout.py /home/krer/Documents/Deep-RL-Baselines/results/wenc_evader_1r_rsrg_1m/5x5/PPO_evader_rstart_rgoal_1msteps-5x5-PPO/PPO_GridEvaderEnv_0_2020-04-21_16-10-202g55az4v/checkpoint_250/checkpoint-250 --run PPO --env evader5x5 --steps 10000


#Grid Evader 1m steps rsrg training on 5x5 DQN
#Evader gets stuck at local optima
#./rollout.py /home/krer/Documents/Deep-RL-Baselines/results/wenc_evader_1r_rsrg_1m/5x5/DQN_evader_rstart_rgoal_1msteps-5x5-DQN/DQN_GridEvaderEnv_0_2020-04-21_17-43-38czg1f96b/checkpoint_1000/checkpoint-1000 --run DQN --env evader5x5 --steps 10000


#Grid chaser 1m steps PPO
#/home/krer/Documents/Deep-RL-Baselines/results/wenc_chaser_1r_rsrg_1m/5x5/PPO_chaser_rstart_rgoal_1msteps-5x5-PPO/PPO_GridEvaderEnv_0_2020-04-21_11-52-58x5ftwiz7/checkpoint_250

#./rollout.py /home/krer/Documents/Deep-RL-Baselines/results/wenc_chaser_1r_rsrg_1m/5x5/PPO_chaser_rstart_rgoal_1msteps-5x5-PPO/PPO_GridEvaderEnv_0_2020-04-21_11-52-58x5ftwiz7/checkpoint_250/checkpoint-250 --run PPO --env chaser5x5 --steps 10000


#Reacher 2 joints TD3
./rollout.py /home/krer/Documents/Deep-RL-Baselines/results/report_results/reacher/reacher_rllib_allalgs/2joints/2-joints-DDPG/DDPG_NJointArm_49113e4a_0_lr=0.0001_2020-05-13_11-37-19m_5qmtjy/checkpoint_200/checkpoint-200 --run DDPG --env njarm2 --steps 10000
