from ray.rllib.agents import ppo, ddpg, a3c, dqn, pg

def get_trainer(arg):
    trainer = None
    if arg == 'DQN':
        trainer = dqn.DQNTrainer
    elif arg == 'PG':
        trainer = pg.PGTrainer
    elif arg == 'APEX-DQN':
        trainer = dqn.ApexTrainer
    elif arg == 'TD3':
        trainer = ddpg.TD3Trainer
    elif arg == 'A2C':
        trainer = a3c.A2CTrainer
    elif arg == 'PPO':
        trainer = ppo.PPOTrainer
    else:
        print("please enter valid trainer")
        exit(0)
    return trainer
