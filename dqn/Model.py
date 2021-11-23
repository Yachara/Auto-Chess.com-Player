from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import RMSprop

import numpy as np




class DQNModel:
    '''
    Class that manages the neural network of DQN agent.
    Through it the models parameters are controled:
        * number of layers
        * nodes in each layer
        * activation functions
        * optimizers
        * etc...
    '''

    def __init__(self):
        self.model = self.create_model(input_shape = (514,), action_space = 4096)


    def create_model(self, input_shape, action_space):
        '''
        Method used to create the model.
        
        PARAMS:
            input_shape    <integer>    the number of input neurons the network needs
            action_space   <integer>    number of output neuron the network needs
            
        RETURNS:
            models    <tensorflow neural network>    this holds the neural network model
            
        '''
        model = Sequential()
        
        model.add(Dense(514, input_shape=input_shape, activation="relu", kernel_initializer='he_uniform'))
        model.add(Dense(256, activation="relu", kernel_initializer='he_uniform'))
        model.add(Dense(64, activation="relu", kernel_initializer='he_uniform'))
        model.add(Dense(action_space, activation="linear", kernel_initializer='he_uniform'))
        
        model.compile(loss="mse", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=['accuracy'])

        model.summary()
        return model


    def predict(self, input_values, debug=False):
        if debug: print("We are making predictions. We are using input values: ", input_values.shape)
        if debug: print(input_values)
        input_values = np.reshape(input_values, (1, input_values.shape[0]))
        if debug: print("Input values needs to be reshaped: ", input_values.shape)

        predictions = self.model.predict(input_values)
        if debug: print("Prediction values: ", predictions.shape)
        if debug: print(predictions)

        return predictions.flatten() # We want shape: (4096,) but prediction returns (1, 4096)

    def fit(self, states, targets, debug=False):
        '''
        '''
        if debug:
            print("We are fitting our model.")
            print("States: ")
            print(states)
            print("Targets:")
            print(targets)

        
        self.model.fit(states, targets)
        




if __name__ == "__main__":
    print("Testing this script")
    model = DQNModel()
    input_values = np.random.randint(2, size=(514,))
    model.predict(input_values)