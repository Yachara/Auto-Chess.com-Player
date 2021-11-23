import numpy as np


class Reward():

    def __init__(self):
        '''
        '''
        self.state_before_move = None # Variable used when calculating the reward
        self.state_after_move = None  # Variable used when calculating the reward
        self.from_ = None
        self.to_ = None

    def calc_reward(self, debug=True):
        '''
        Function used to calculate te reward after we make a move.
        '''
        if debug: 
            print("We are calculating the reward")
            print("The board state BEFORE we made a move:")
            print(self.state_before_move)
            print()
            print("The board state AFTER the move: ")
            print(self.state_after_move)
            print()
            fig_moved = self.state_before_move.loc[int(self.from_[-1]), self.from_[0]]
            print("Figure moved: ", fig_moved)
            print("From_ :", self.from_)
            print("To_: ", self.to_)

        reward = 0

        columns = self.state_before_move.columns
        reward = 10 * np.where(columns == self.from_[0])[0][0] # If figure we moved was closer to H, the bigger the reward

        print("Total reward is: ", reward)
        return reward