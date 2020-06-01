
#Chaser
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
/usr/bin/timeout 1800s python chaser_evader_experiments.py --rl PPO --name chaser_curriculum_cont --random_goals --random_start



