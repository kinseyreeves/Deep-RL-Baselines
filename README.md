# Deep Reinforcement Learning Baseline Environments

Masters of computer science Masters project, implementing openai gyms to test various Deep RL algorithms against as baselines.
These environments are designed to have scalable action and state space complexity. i.e. we can increase the complexity of the problem while keeping the number of possible actions the same, or vice versa


Kinsey Reeves
kreeves@student.unimelb.edu.au

**Requirements**
- OpenAI gym
- Pygame


**Environments:**

- N-jointed arm
- Environment consists of an arm of N-joints which must configure itself    to touch an objective

    - Action space : discrete (scalable) one hot, or continuous of number of free joints
    - State space array consists of:
        - At target 1|0
        - Joint position_x to objective position_x  (For all joints)
        - Joint position_y to objective position_y (For all joints)
        - distance x from centre to objective
        - distance y from centre to objective
        
    e.g. 2 joints will consist of array of size 7

- N-Grid-Evaders
    - Action space : discrete (scalable)
    - State space : discrete (grid coordinates of evader and chaser)
    
- N-Grid-Chasers


- N-Maze solver


This is a work in progress.
