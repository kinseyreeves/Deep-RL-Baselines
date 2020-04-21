# Deep Reinforcement Learning Baseline Environments

Thesis project, implementing vairous gyms to test various Deep RL algorithms against as baselines.
Each environment is able to scale in complexity of either total state space size or the inherent difficulty of the problem. 


Kinsey Reeves
kreeves@student.unimelb.edu.au

**Requirements**
- OpenAI gym
- Pygame
- RLLib if testing environments


**Environments:**

Configurations are passed to the environments as `config` dictionaries. This is the format for RLLIB environments.

## N-jointed arm
- Environment consists of an arm of N-joints which must configure itself    to touch an objective

    - Action space : discrete (scalable) one hot, or continuous of number of free joints
    - State space array consists of:
        - At target 1|0
        - Joint position_x to objective position_x  (For all joints)
        - Joint position_y to objective position_y (For all joints)
        - distance x from centre to objective
        - distance y from centre to objective
        
    e.g. 2 joints will consist of array of size 7
###
Config:
```python
config = {
    #number of joints the arm has
    "num_joints" : 1,
    #Full state information used for jacobian, basic state has just joint (x,y) positions
    "full_state" : False,
}

```
    
 ## Grid World
 - Grid-Evader
    - Action space : discrete
    - State space : discrete (grid coordinates of evader and chaser)
    
Overall config

```python
config = {
    # Whether or not to randomize the start position and goal / enemy positions
    "randomize_start" : False,
    "randomize_goal" : False,
    #If we want to use the full state encoding, or just positions of interest
    "encoded_state" : False,
    #Do we want to use 1 rewards where available, e.g. if false -0.1 rewards used, as outlined in Sutton 2018
    "capture_reward" : False,
    #whether we want to slowdown for testing purposes / when evaluating
    "slowdown_step" : False
}

```

### Maze solver
    - Action space : discrete (scalable)
    - State space : discrete (grid coordinates of evader and chaser)
 
Goal is to pick up the rewards in as few steps as possible. Baseline is based on A* and then a brute force TSP implementation. 

#### Config
`
#number of goals in the maze to pickup
"num_goals" : 1
`

### Grid-Evader
 
Goal is to evade the chaser as long as possible
    
### Grid-Chaser
    - Action space : discrete
    - State space : discrete (grid coordinates of evader and chaser)


This is a work in progress.
