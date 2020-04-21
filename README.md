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

###Maze solver
    - Action space : discrete (scalable)
    - State space : discrete (grid coordinates of evader and chaser)
 
Goal is to pick up the rewards in as few steps as possible. Baseline is based on A* and then a brute force TSP implementation. 

####Config



###Grid-Evader
 
Goal is to evasde
    
###Grid-Chaser
    - Action space : discrete
    - State space : discrete (grid coordinates of evader and chaser)


This is a work in progress.
