#implementation of montecarlo policy gradient in python
#using tensorflow
#based on : https://github.com/simoninithomas/Deep_reinforcement_learning_Course/blob/master/Policy%20Gradients/Cartpole/Cartpole%20REINFORCE%20Monte%20Carlo%20Policy%20Gradients.ipynb

#TODO convert tf to keras https://gist.github.com/calclavia/cfcd41ad4e47d7b9b6ab8af15410747a


import tensorflow as tf
import numpy as np
import gym


env = gym.make('CartPole-v0')
env = env.unwrapped
env.seed(1)

state_size = 4
action_size = env.action_space.n

RENDER = False

MAX_EPISODES = 300
LEARNING_RATE = .01
GAMMA = 0.95

def discount_rewards(episode_rewards):
    disc_rewards = np.zeros_like(episode_rewards, dtype = float)
    cumulative = 0.0
    for i in reversed(range(len(episode_rewards))):
        cumulative = cumulative * GAMMA + episode_rewards[i]
        #print(cumulative)
        disc_rewards[i] = cumulative

    mean = np.mean(disc_rewards)
    std = np.std(disc_rewards)
    
    #TODO should we normalize here? some versions have some don't
    disc_rewards = (disc_rewards - mean) / (std)
    
    
    #TODO try without normalizing
    return disc_rewards


with tf.name_scope("inputs"):
    input_ = tf.placeholder(tf.float32, [None, state_size], name="input_")
    actions = tf.placeholder(tf.int32, [None, action_size], name="actions")
    discounted_episode_rewards_ = tf.placeholder(tf.float32, [None,], name="discounted_episode_rewards")
    
    # Add this placeholder for having this variable in tensorboard
    mean_reward_ = tf.placeholder(tf.float32 , name="mean_reward")

    with tf.name_scope("fc1"):
        fc1 = tf.contrib.layers.fully_connected(inputs = input_,
                                                num_outputs = 10,
                                                activation_fn=tf.nn.relu,
                                                weights_initializer=tf.contrib.layers.xavier_initializer())

    with tf.name_scope("fc2"):
        fc2 = tf.contrib.layers.fully_connected(inputs = fc1,
                                                num_outputs = action_size,
                                                activation_fn= tf.nn.relu,
                                                weights_initializer=tf.contrib.layers.xavier_initializer())
    
    with tf.name_scope("fc3"):
        fc3 = tf.contrib.layers.fully_connected(inputs = fc2,
                                                num_outputs = action_size,
                                                activation_fn= None,
                                                weights_initializer=tf.contrib.layers.xavier_initializer())

    with tf.name_scope("softmax"):
        action_distribution = tf.nn.softmax(fc3)

    with tf.name_scope("loss"):
        # tf.nn.softmax_cross_entropy_with_logits computes the cross entropy of the result after applying the softmax function
        # If you have single-class labels, where an object can only belong to one class, you might now consider using 
        # tf.nn.sparse_softmax_cross_entropy_with_logits so that you don't have to convert your labels to a dense one-hot array. 
        neg_log_prob = tf.nn.softmax_cross_entropy_with_logits_v2(logits = fc3, labels = actions)
        loss = tf.reduce_mean(neg_log_prob * discounted_episode_rewards_) 
        
    
    with tf.name_scope("train"):
        train_opt = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss)


def run():
    all_rewards = []
    total_rewards = 0
    max_reward_rec = 0
    episode = 0
    episode_states, episode_actions, episode_rewards = [], [], []
    

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for episode in range(MAX_EPISODES):
            episode_rewards_sum = 0
            state = env.reset()
            if(RENDER):
                env.render()
            #print("here")
            while True:
                #select action based on NN
                action_prob_dist = sess.run(action_distribution, feed_dict = {input_:state.reshape([1,4])})
                action = np.random.choice(action_prob_dist.shape[1], p = action_prob_dist[0])

                new_state, reward, done, info = env.step(action)

                episode_states.append(state)

                #Select action as 1-hot vector
                action_ = np.zeros(action_size)
                action_[action] = 1

                episode_actions.append(action_)
                episode_rewards.append(reward)

                if(done):
                    episode_rewards_sum = np.sum(episode_rewards)
                    all_rewards.append(episode_rewards_sum)
                    total_rewards = np.sum(all_rewards)
                    mean_reward = np.divide(total_rewards, episode+1)

                    max_reward_recorded = np.amax(all_rewards)

                    print("episode : ", episode)
                    print("reward : ", episode_rewards_sum)
                    print("max reward so far: ", max_reward_recorded)

                    discounted_rewards = discount_rewards(episode_rewards)

                    loss_, _ = sess.run([loss, train_opt], feed_dict={input_: np.vstack(np.array(episode_states)), actions: np.vstack(np.array(episode_actions)), discounted_episode_rewards_ : discounted_rewards})

                    episode_states, episode_actions, episode_rewards = [],[],[]
                    break
                state = new_state
                
                

run()