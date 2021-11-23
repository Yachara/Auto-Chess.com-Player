import random
import numpy as np
import os
import pickle # for quick saving of memory


class DQNAgent:
    '''
    Class used to manage the DQN Agent.
    
    '''
    
    def __init__(self,
                 state_size,
                 action_size,
                 good_memory=None,      # I played some rounds to win and get the "good path"
                 gamma=0.95,         # reward discount rate
                 epsilon=1.0,        # exploration rate
                 epsilon_min=0.001,
                 epsilon_decay=0.999,
                 batch_size=64,
                 train_start=1000,   # when we have this many individual memories, the training can start
                 
                ):
        '''
        
        PARAMS:
            state_size    <integer>    Defines how many input neurons we need.
            action_size   <integer>    How many different actions we can make. Defines how many output neurons we need.
            gamma         <float>      The reward discount rate. Value is used in the newQ value calculation.
            epsilon       <float>      The exploration. If a random number is lower than epsilon we will make a random action.
            epsilon_min   <float>      The minimal value epsilon can take.
            epsilon_decay <float>      Value used when decaying the epsilon.
            batch_size    <integer>    The size of the minibatch we take from memory when training.
            train_start   <integer>    The amount of individual memories we want to have before we start training.
            
        RETURNS:
            
        '''
        
        self.state_size = state_size
        self.action_size = action_size
        
        self.EPISODES = EPISODES
        self.memory = DQNMemory(good_memory=good_memory)
        
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        
        self.batch_size = batch_size
        self.train_start = train_start

        # create main model
        self.model = DQNModel().create_model(input_shape=(self.state_size,), 
                              action_space = self.action_size)
        
        
    def load(self, path):
        '''
        Loads the pre-existing model. 
        (Does the model need to be the same architecture or can it be anything?)
        
        PARAMS:
            path   <string>    path to the model
        '''
        
        self.model = load_model(path)
        self.model.summary()


    def save(self, path, model_name=None):
        '''
        Save the neural network model.
        
        PARAMS:
            path    <string>    path where to save the model. The model name is added automaticaly
                                Example: path = "D/DQN/Models/"
        '''
        if model_name == None:
            model_name = DNQModel().name + "model.h5"  # create the model name
        
        path = os.path.join(path, model_name)
        print("Saving model under: ", path)
        self.model.save(path)
        
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.add_memory(state, action, reward, next_state, done)

        
    def update_exploring(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

                
    def get_action(self, state):
        state = np.reshape(state, newshape=(1, state.shape[0]))
        q_values = self.model.predict(state) # gets Q-values for each state-action pair
        actions = np.argsort(q_values) # Sorts the Q-values from lowest to highest and returns their indexes. 
        #Example: [3,2,4,1] means that the Q-value on index 3 is the lowest, next one is on index 2, etc.
        
        #print("Q-Values: ", q_values)
        if np.random.random() <= self.epsilon:
            # We are exploring by taking a second best action (not a random one)
            #return random.randrange(self.action_size) # this makes a random action. Which could also be the correct one
            
            actions = actions[:, :-1] # this gets all EXCEPT the best action.. since we want to explore
            #p = (0.2,0.3,0.5) # the distribution when we choose our action... we want the second best to be choosen the most, but we also want to be able to choose the worst one so that we actually do explore
            # p should not be so hard-coded
            # we want the first action (which has the word Q and is the worst action) to have the lowest probablity to be choosen
            # but we still want to choose it some times... 
            action = np.random.choice(actions.flatten(), 1)[0]
            #print("Worse choosen: ", action)
            return action
        else:
            action = actions[:, -1][0]
            #print("Best choosen:", action)
            return action # making the best action

        
    def train(self, graph):
        '''
        graph pove nej izrisuje minibatches, da se vid na kerih STATEs se uči
        '''
        if self.memory.moments_gathered < self.train_start:
            return
        self.memory.moments_gathered = self.train_start
        # Randomly sample minibatch from the memory
        minibatch = self.memory.get_minibatch(batch_size=self.batch_size)
        '''
        Napisat kako točn more minibatch zgledat kt struktura
        '''
        
        # Unpacking the minibatch so we can prepare for training
        state = np.empty(shape=(0, self.state_size))
        for s in minibatch[:, 0]:
            #print(s, s.shape, type(s))
            reshaped = np.reshape(s, newshape=(1, s.shape[0]))
            #print(reshaped, reshaped.shape)
            state = np.append(state, reshaped, axis=0)
        action = minibatch[:, 1]
        reward = minibatch[:, 2]
        next_state = np.empty(shape=(0,self.state_size))
        for s in minibatch[:, 3]: # I dont like this for looping. Stuff should be done on the tensor level...
            #print(s, s.shape, type(s))
            reshaped = np.reshape(s, newshape=(1, s.shape[0]))
            #print(reshaped, reshaped.shape)
            next_state = np.append(next_state, reshaped, axis=0)
        done = minibatch[:, 4]
        
        # do batch prediction to save speed
        target = self.model.predict(state, batch_size=state.shape[0])
        target_next = self.model.predict(next_state)
        '''
        predict() will go through all the data, batch by batch, predicting labels. 
        It thus internally does the splitting in batches and feeding one batch at a time.

        predict_on_batch(), on the other hand, assumes that the data you pass in is exactly 
        one batch and thus feeds it to the network. It won't try to split it (which, depending on 
        your setup, might prove problematic for your GPU memory if the array is very big)
        '''
        
        for i in range(reward.shape[0]):
            # correction on the Q value for the action used
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                # Standard - DQN
                # DQN chooses the max Q value among next actions
                # selection and evaluation of action is on the target Q Network
                # Q_max = max_a' Q_target(s', a')
                target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))
        
        if graph != None:
            graph_data = {
                (2,): {
                    "x": [x[0] for x in state],
                    "y": [x[1] for x in state],
                    "draw_mode": "scatter",
                    "x_label": "position",
                    "y_label": "velocity",
                }
            }
            graph.draw(graph_data)
        # Train the Neural Network with batches
        self.model.fit(state, target, batch_size=self.batch_size, verbose=0)
        
        
        def save_memory(self):
            with open("good_memory.pickle", "wb") as f:
                pickle.dump(self.memory.good_memory, f)
            with open("good_memory.pickle", "wb") as f:
                pickle.dump(self.memory.bad_memory, f)