# Masters-Project-KR

Masters of computer science Masters project, implementing openai gyms to test various Deep RL algorithms against as baselines.
These environments are designed to have scalable action and state space complexity. i.e. we can increase the complexity of the problem while keeping the number of possible actions the same, or vice versa


Kinsey Reeves
kreeves@student.unimelb.edu.au

Environments implemented:

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

- N-Evaders
    - Action space : discrete (scalable)
    - State space : continuous ()
TODO
- Traffic Lights
    - Action space : discrete (scalable)
    - State space : continuous ()

Algorithms implemented:

- DQN
- Monte Carlo Policy Gradients
- DDPG
- Cross Entropy
- A2C


- Deep Q Learning

Running the code:
Requirements : openai gym, pygame, pytorch

- Files for testing environments can be found in /Testing
- 


TODO 
    - DQN
        - Double Q-Learning
    - A2C
    - Double Q-Learning
    - PPO
    - TRPO?
    - 
