import random
import numpy as np
import pandas as pd
from collections import deque

class DQNMemory:
    '''
    Class used to manage the DQN Memory.
    '''
    
    def __init__(self, 
                 good_memory,
                 max_good_episodes = 5, # how many good episodes can be in the good memory
                 max_bad_episodes = 5,
                 
                ):
        self.setup_memory(good_memory)
        self.max_good_episodes = max_good_episodes
        self.max_bad_episodes = max_bad_episodes
        
        self.moments_gathered = 0 # every moment we add, this gets +1. Its a stand-in for checking when to start training
    
    
    def setup_memory(self, good_memory=None, bad_memory=None):
        if good_memory != None:
            self.good_memory = good_memory         # Holds a few full episodes in which I won by hand
        elif good_memory == None:
            self.good_memory = {}
        
        if bad_memory != None:
            self.bad_memory = bad_memory
        elif bad_memory == None:
            self.bad_memory = {}
        
        self.random_memory = deque(maxlen=1000) # This will be the random memory from episodes
        self.episode_memory = []   # This holds the memory of 1 episode. So that I can save it if we WIN
        
        self.memory = np.empty(shape=(0,5))
    
    def add_memory(self, state, action, reward, next_state, done):
        '''
        Adds a new memory to the overall memory.
        
        PARAMS:
        
        RETURNS:
        '''
        self.random_memory.append(np.array([state, action, reward, next_state, done]))
        self.episode_memory.append(np.array([state, action, reward, next_state, done]))
        self.moments_gathered += 1
        
        
    def reset_episode_memory(self):
        self.episode_memory = []
    
    
    def add_good_episode_to_memory(self, ep_reward):
        good_episode = np.array(self.episode_memory)
        
        print()
        print("Good episodes: ", list(self.good_memory.keys()), "/", self.max_good_episodes)
        
        if len(self.good_memory.keys()) < self.max_good_episodes:
            self.good_memory[ep_reward] = good_episode
        elif ep_reward > min(self.good_memory.keys()):
            del self.good_memory[min(self.good_memory.keys())]
            self.good_memory[ep_reward] = good_episode # tko se nadomesti najmanjši reward z novim episodičnim spominom
            
    def add_bad_episode_to_memory(self, ep_reward):
        bad_episode = np.array(self.episode_memory)
        
        print("Bad episodes: ", list(self.bad_memory.keys()), "/", self.max_bad_episodes)

        if len(self.bad_memory.keys()) < self.max_bad_episodes:
            self.bad_memory[ep_reward] = bad_episode
        elif ep_reward < max(self.bad_memory.keys()):
            del self.bad_memory[max(self.bad_memory.keys())]
            self.bad_memory[ep_reward] = bad_episode # tko se nadomesti najmanjši reward z novim episodičnim spominom
            
            
    def get_minibatch(self, batch_size):
        '''
        Function that returns a minibatch from the overall memory.
        
        
        
        PARAMS:
            batch_size    <integer>    the size of the minibatch
            
        RETURNS:
            minibatch     <>
        '''
        
        # Select one of the good_episode from good_memory.
        # The higher the total_reward it got, the higher the chances to be choosen
        # From that good_episode, get the minibatch
        good_rewards = np.array(list(self.good_memory.keys())) # get the good rewards
        #normalize the good_rewards to fall between -1 and 1. If they are not normalized than extreme values will fuck with the math..
        # normalization can be done on a bigger interval, but -1 to 1 is probably good..
        
        norm_good_rewards = 2* ((good_rewards-np.min(good_rewards))/(np.max(good_rewards)-np.min(good_rewards))) - 1
        good_probabilities = np.exp(norm_good_rewards)/np.sum(np.exp(norm_good_rewards)) # e^x/sum(e^x)
        good_probabilities[-1] = 1-sum(good_probabilities[:-1])
        good_choice = np.random.choice(good_rewards, 1, p=good_probabilities)[0] # Function returns array, even if with only 1 number
        # Get moments from self.good_memory
        good_memory = np.empty(shape=(0, 5)) # should not be hardcoded like this
        for moment in self.good_memory[good_choice]:
            moment = np.reshape(moment, newshape=(1, moment.shape[0]))
            good_memory = np.append(good_memory, moment, axis=0)
            
        # Do the same probabilites for the bad memory
        bad_rewards = np.array(list(self.bad_memory.keys()))
        # normalize the bad rewards between -1 and 1
        norm_bad_rewards = 2* ((bad_rewards-np.min(bad_rewards))/(np.max(bad_rewards)-np.min(bad_rewards))) - 1
        bad_probabilities = np.exp(norm_bad_rewards)/np.sum(np.exp(norm_bad_rewards)) # we are taking the best bad_episode (-200, -300, -400) we would take -200.. not really what i wanted but ok. I wanted to take the worst (-400)
        bad_probabilities[-1] = 1-sum(bad_probabilities[:-1])
        bad_choice = np.random.choice(bad_rewards, 1, p=bad_probabilities)[0] # Function returns array, even if with only 1 number
        # Get moments from self.bad_memory
        bad_memory = np.empty(shape=(0, 5)) # should not be hardcoded like this
        for moment in self.bad_memory[bad_choice]:
            moment = np.reshape(moment, newshape=(1, moment.shape[0]))
            bad_memory = np.append(bad_memory, moment, axis=0)
        
        random_memory = np.empty(shape=(0, 5)) # should not be hardcoded like this
        random_memory = np.append(random_memory, self.random_memory, axis=0)
        
        minibatch = np.empty(shape=(0,5)) # should not be hardcoded
        
        np.random.shuffle(good_memory)
        minibatch = np.append(minibatch, good_memory[:int(batch_size/3)], axis=0)
        
        np.random.shuffle(bad_memory)
        minibatch = np.append(minibatch, bad_memory[:int(batch_size/3)], axis=0)
        
        np.random.shuffle(random_memory)
        
        minibatch = np.append(minibatch, random_memory[:int(batch_size/3)], axis=0) # We contantly go through good and bad episodes. But there is a WHOLE lot in between. Im guessing.. maybe I don't need this much moments from random memory
        
        return minibatch