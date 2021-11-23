
import numpy as np
import pandas as pd
import time
import re # HTML classes are not always in the same order. Need regex to parse the stuff out.

from selenium.common.exceptions import StaleElementReferenceException # piece elements changes while getting it. So the element becomes "stale", but I could still get data from it

from dqn.Model import DQNModel



class ChessAgent:

    def __init__(self,
                driver,
                my_color="white", #
                ):

        self.driver = driver # So i can get game state

        self.my_color = my_color
        self.figures = np.array(["r", "n", "b", "q", "k", "p"]) # Rook, Knight, Bishop, Queen, King, Pawn
        self.columns = np.array(["A", "B", "C", "D", "E", "F", "G", "H"])
        self.squares = np.array(["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
                                "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
                                "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",
                                "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
                                "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
                                "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
                                "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8",
                                "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"])

        # Same index represents same square.
        self.squares_class_values = np.array(["11", "12", "13", "14", "15", "16", "17", "18", # A
                                            "21", "22", "23", "24", "25", "26", "27", "28", # B
                                            "31", "32", "33", "34", "35", "36", "37", "38", # C
                                            "41", "42", "43", "44", "45", "46", "47", "48", # D
                                            "51", "52", "53", "54", "55", "56", "57", "58", # E
                                            "61", "62", "63", "64", "65", "66", "67", "68", # F
                                            "71", "72", "73", "74", "75", "76", "77", "78", # G
                                            "81", "82", "83", "84", "85", "86", "87", "88",])# H
        self.squares_board_values = np.array(["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
                                            "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
                                            "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",
                                            "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
                                            "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
                                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
                                            "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8",
                                            "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8",])

        self.dqn_model = DQNModel()


    def set_my_color(self, my_color):
        '''
        Since this will play multiple games, i need a function to easly change my color
        '''
        print("ChessAgent -> function set_my_color(). Setting my_color to ", my_color)
        self.my_color = my_color

    def get_move(self,
                player_input=False,
                debug=False):
        
        '''
        Determine in what field the figure we want to move is. And determine to what field we want to move it.


        PARAMS
        

        RETURNS
            from_		str()		Square name (like "B2") in which figure currently resides.
            to_			str()		Square name (like "B3") where we want to move the figure.
                Both can take values: 	A1, A2, A3, A4, A5, A6, A7, A8
                                        B1, B2, B3, B4, B5, B6, B7, B8
                                        C1, C2, C3, C4, C5, C6, C7, C8
                                        D1, D2, D3, D4, D5, D6, D7, D8
                                        E1, E2, E3, E4, E5, E6, E7, E8
                                        F1, F2, F3, F4, F5, F6, F7, F8
                                        G1, G2, G3, G4, G5, G6, G7, G8
                                        H1, H2, H3, H4, H5, H6, H7, H8


        EXCEPTIONS


        '''
        if debug: print("Deciding on the move to make.")


        board_state = self.get_board_state()
        self.print_board_state(board_state)
        #input("Getting a move from agent. Press ENTER to cont.")

        predictions = self.get_prediction(board_state) # Get PREDICTIONS 
        if debug: self.print_prediction(predictions)

        time.sleep(2) # Wait 2 seconds before making another move
        for i in np.argsort(predictions)[::-1]: # Keep choosing a move to make untill we can make a legitimate move.
            # It goes from the last max value to the smallest value
            if debug: print(f"Index of max value: {i} \t with value: {predictions[i]}")
            from_ = self.squares[i//64]
            to_ = self.squares[i%64]
            if debug: print(f"Thinking of moving: \t \t {from_}->{to_}  ")
            from_row = int(from_[-1])
            from_col = from_[0]

            

            if board_state.loc[from_row, from_col] == "ee":
                if debug: print("There isn't any figure in this square. This is an ILLEGALE move.")
                continue
            elif board_state.loc[from_row, from_col][0] != self.my_color[0]:
                if debug: print("This is not my figure. Moving it would be an ILLEGALE move.")
                continue

            if self.is_move_legal(from_, to_, board_state): # If move is legal, move it to that spot, else we need to choose another move.
                if debug: print(f"Move is LEGAL. {board_state.loc[from_row, from_col]} {from_}_{to_}")
                break


        if player_input:
            player_from_, player_to_ = self.get_player_input()
            if player_from_ is not None and player_to_ is not None:
                from_, to_ = player_from_, player_to_
                self.is_move_legal(from_, to_, board_state) # FOR EASIER DEBUGGING

        return from_, to_, i

    def get_player_input(self):
        '''
        Function used so that I can debug and make my moves.
        '''
        player_move = input("Make a move (Exp: B2B3) or Q to Quit or ENTER to let AI decide: ")
        print(f"You chose {player_move}")
        if player_move.lower() == "q":
            print("Quitting.")
            exit()
        elif player_move == "":
            print("You chose to let AI decide.")
            from_ = None
            to_ = None
        else:
            from_ = player_move[:2]
            to_ = player_move[-2:]

        return from_, to_

    def get_board_state(self):
        '''
        Function that gets the input layer... basically..

        Create DatFrame representation of the board

        '''
        board_state = pd.DataFrame("ee", index=[1,2,3,4,5,6,7,8], columns=["A", "B", "C", "D", "E", "F", "G", "H"]) # Creates empty DataFrame which will be used to hold figure positions and types
        
        try:
            pieces = self.driver.find_elements_by_class_name("piece")
            for piece in pieces:
                piece_class = piece.get_attribute("class") # Example:piece wb square-61    White Bishop 2 on square F1... CLASSES ARE NOT ALWAYS IN THE SAME ORDER!
                # FIGURE POSITION
                pos = re.search(r"\d\d", piece_class)[0]
                fig_pos_index = np.where(self.squares_class_values == pos)
                fig_pos = self.squares_board_values[fig_pos_index][0] # Now we have values like H5, etc

                board_state.loc[int(fig_pos[-1]) , fig_pos[0]] = re.search(r"[w,b]\w", piece_class)[0]
        except StaleElementReferenceException as e:
            print("StaleElementReferenceException while looking for piece elements.")
            print(e)
                    
        return board_state
        
    def print_board_state(self, board_state):
        '''
        Function for debugging. Prints the game state
        '''
        print("PRINTING GAME STATE")
        print("Shape: ", board_state.shape)
        print(board_state.to_string())
        
        
        
    def get_prediction(self, board_state, debug=False):
        '''
        In here comes the NEURAL NETWORK PREDICTION CODE
        '''

        if debug: print("Got the board state. Now we need to transform it into input_layer")
        input_values = self.get_input_values(board_state)
        if debug: self.print_input_values(input_values)

        # AI etc
        predictions = self.dqn_model.predict(input_values)
        print("Predictions: ", predictions.shape)
        print(predictions)
        # predictions

        return predictions

    def get_input_values(self, board_state):
        '''
        Transforms the board_state DataFrame into input values for NN
        '''
        print("Transforming game_state into input values.")

        input_values = np.zeros(shape=(2 + 8 * board_state.shape[0]*board_state.shape[1]), dtype=np.int8)
        input_values[0] = 1 if self.my_color == "white" else 0
        input_values[1] = 1 if self.my_color == "black" else 0

        for i, value in enumerate(board_state.values.flatten()):
            # we are itterating from A1, B1, C1, etc.. G8, H8
            mask = np.zeros(shape=(8,), dtype=np.int8)
            
            if value != "ee":
                mask[0] = 1 if value[0] == "w" else 0
                mask[1] = 1 if value[0] == "b" else 0

                figure_type_i = np.where(self.figures == value[-1])[0]
                mask[2 + figure_type_i] = 1

            slice_from = 2 + 8*i
            slice_to = slice_from + mask.shape[0]
            
            input_values[slice_from : slice_to] = mask


        return input_values


    def print_input_values(self, input_values):
        '''
        for debugging
        '''
        print("INPUT LAYER", input_values.shape)
        for value in input_values:
            print(value, end=", ")
        print()



    def print_prediction(self, predictions):
        '''
        for debugging
        '''
        print("PREDICTIONS shape: ", predictions.shape)
        for i in predictions:
            print(i, end=", ")
        print()


    def is_move_legal(self, 
                        from_, 
                        to_, 
                        board_state,
                        debug=False):
        '''
        pawn
            can move 1 forward, unless all the way across
            can move 2 forward, if in its starting position
            can move 1 sideways if it eats a figure
            can't move to square occupied by another same_color figure
            (some special move when you reach the end of the board)
            (some special move called en passant )

        rook
            can move any number forward/left/right/back, up to the next figure (if figure is same_color), or it can eat the figur)
            can't move to square occupied by another same_color figure
        
        knight
            take the squares 1 (front, left, right, back). From those squares, go diagonaly left and diagonaly right. Those 8 squares are his legal moves.
            can't move to square occupied by another same_color figure

        bishop
            can move diagonally for any number of squares up to the next figure (if figure is same_color), or it can eat the figure
            can't move to square occupied by another same_color figure

        queen
            basically combine the rules for rook and bishop
        
        king
            can move 1 square any direction.
            between him and opposing king there must be atleast 1 square
            can't move to squares that would put him in check
            can't move to squares that are occupied by same_color figure
            (some special moves regarding rooks)


        '''
        if debug: print(f"Checking if move {from_} to {to_} is legal.")
        
        figure = board_state.loc[int(from_[-1]), from_[0]]

        legal_moves = np.empty(shape=(0,)) # holds every possible legal move for the figure. Dont need this. Could just get the actual array fromn sunction       
        # Checking type of figure since different rules apply to different figures
        if figure[1] == "r":
            if debug: print("We are looking at ROOK ruleset.")
            legal_moves = np.append(legal_moves, self.get_rook_legal_moves(board_state, from_, fig_color=figure[0]))
        elif figure[1] == "n":
            if debug: print("We are looking at KNIGHT ruleset.")
            legal_moves = np.append(legal_moves, self.get_knight_legal_moves(board_state, from_, fig_color=figure[0]))
        elif figure[1] == "b":
            if debug: print("We are looking at BISHOP ruleset.")
            legal_moves = np.append(legal_moves, self.get_bishop_legal_moves(board_state, from_, fig_color=figure[0]))
        elif figure[1] == "q":
            if debug: print("We are looking at QUEEN ruleset.")
            legal_moves = np.append(legal_moves, self.get_queen_legal_moves(board_state, from_, fig_color=figure[0]))
        elif figure[1] == "k":
            if debug: print("We are looking at KING ruleset.")
            legal_moves = np.append(legal_moves, self.get_king_legal_moves(board_state, from_, fig_color=figure[0]))
        elif figure[1] == "p":
            if debug: print("We are looking at PAWN ruleset.")
            legal_moves = np.append(legal_moves, self.get_pawn_legal_moves(board_state, from_, fig_color=figure[0]))


        if True: 
            if debug: print(f"All LEGAL MOVES for {figure} from {from_}")
            for lm in legal_moves:
                if debug: print(f"--> {lm}")

        #input("Check if legal moves are OK. <press ENTER to cont.>")
        if debug: print("Checking if our move is legal.:")        
        if to_ in legal_moves:
            if debug: print("This is LEGAL MOVE")
            return True
        else:
            if debug: print("This is ILLEGAL MOVE. Pick another")
            return False


    def get_pawn_legal_moves(self, board_state, from_, fig_color, debug=False):
        '''
        specifically looking at PAWN legal moves

        Most of the rules can be 
        '''
        legal_moves = np.empty(shape=(0,))

        pawn_row = int(from_[-1])
        pawn_col = from_[0]
        pawn_col_i = np.where(self.columns == pawn_col)[0][0]

        if debug: print("Pawn row: ", pawn_row)
        if debug: print("pawn_col", pawn_col)
        if debug: print("Pawn color: ", fig_color)

        if fig_color == "w":                                                            # Can move 1 forward
            if pawn_row+1 <= 8:                                                            # if not on the last row
                if board_state.loc[pawn_row+1, pawn_col] == "ee":                       # or if there isn't any figure blocking the way
                    legal_moves = np.append(legal_moves, f"{pawn_col}{pawn_row+1}")
                    if debug: print(f"Pawn can move to {pawn_col}{pawn_row+1}")
                                                                                        # It can also eat figures
                for c in [-1, +1]:                                                      # It can eat figure left-up and right-up
                    if pawn_col_i+c < 0 or pawn_col_i+c > 7: # We are out of bounds
                        continue
                    else:
                        if board_state.loc[pawn_row+1, self.columns[pawn_col_i+c]][0] == "b":
                            legal_moves = np.append(legal_moves, f"{self.columns[pawn_col_i+c]}{pawn_row+1}")
                            if debug: print(f"Pawn can eat figure at {self.columns[pawn_col_i+c]}{pawn_row+1}")

            if pawn_row == 2:                                                               # Can move 2 forward if in starting position
                if (board_state.loc[pawn_row+1, self.columns[pawn_col_i]][0] == "e") and (board_state.loc[pawn_row+2, self.columns[pawn_col_i]][0] == "e"):
                    legal_moves = np.append(legal_moves, f"{pawn_col}{pawn_row+2}")
                    if debug: print(f"Pawn can move 2 forward to {pawn_col}{pawn_row+2}")

        if fig_color == "b":                                                            # Can move 1 forward
            if pawn_row-1 >= 1:                                                         # if not on the last row
                if board_state.loc[pawn_row-1, pawn_col] == "ee":                       # or if there isn't any figure blocking the way
                    legal_moves = np.append(legal_moves, f"{pawn_col}{pawn_row-1}")
                    if debug: print(f"Pawn can move to {pawn_col}{pawn_row-1}")
                                                                                        # It can also eat figures
                for c in [-1, +1]:                                                      # It can eat figure left-up and right-up
                    if pawn_col_i+c < 0 or pawn_col_i+c > 7: # We are out of bounds
                        continue
                    else:
                        if board_state.loc[pawn_row-1, self.columns[pawn_col_i+c]][0] == "w":
                            legal_moves = np.append(legal_moves, f"{self.columns[pawn_col_i+c]}{pawn_row-1}")
                            if debug: print(f"Pawn can eat figure at {self.columns[pawn_col_i+c]}{pawn_row-1}")

            if pawn_row == 7:                                                               # Can move 2 forward if in starting position
                if (board_state.loc[pawn_row-1, self.columns[pawn_col_i]][0] == "e") and (board_state.loc[pawn_row-2, self.columns[pawn_col_i]][0] == "e"):
                    legal_moves = np.append(legal_moves, f"{pawn_col}{pawn_row-2}")
                    if debug: print(f"Pawn can move 2 forward to {pawn_col}{pawn_row-2}")
        
        legal_moves_checked = np.empty(shape=(0,))
        for lm in legal_moves:
            hypothetical_board_state = board_state.copy()
            hypothetical_board_state.loc[pawn_row, pawn_col] = "ee"
            hypothetical_board_state.loc[int(lm[-1]), lm[0]] = f"{fig_color}p"

            if self.is_my_king_in_check(hypothetical_board_state, fig_color):
                if debug: print(f"Move to {lm} puts KING IN CHECK.")
            else:
                legal_moves_checked = np.append(legal_moves_checked, lm)


        return legal_moves_checked

    def get_rook_legal_moves(self, board_state, from_, fig_color, debug=False): 
        '''
        legal moves for ROOK

        Can move to the left, right, up or down...
        '''
        legal_moves = np.empty(shape=(0,))

        rook_row = int(from_[-1])
        rook_col = from_[0]
        rook_col_i = np.where(self.columns == rook_col)[0][0]

        # Checking UP
        for i in range(rook_row+1,9): # rook_row +1 because otherwise it would count "moving to the row you are in" as a legal move
            if board_state.loc[i, rook_col] == "ee":
                if debug: print(f"Rook can move to {rook_col}{i}")
                legal_moves = np.append(legal_moves, f"{rook_col}{i}")
            elif board_state.loc[i, rook_col][0] == fig_color:
                if debug: print(f"Rook cant UP here because {board_state.loc[i, rook_col]} is blocking my path.")
                break # Cant move past this figure of same color
            else:
                if debug: print(f"We can eat figure UP at {rook_col}{i}")
                legal_moves = np.append(legal_moves, f"{rook_col}{i}") # we can eat this figure
                break

        # Checking DOWN
        for i in range(rook_row-1,0, -1): # rook_row +1 because otherwise it would count "moving to the row you are in" as a legal move
            if board_state.loc[i, rook_col] == "ee":
                if debug: print(f"Rook can move to {rook_col}{i}")
                legal_moves = np.append(legal_moves, f"{rook_col}{i}")
            elif board_state.loc[i, rook_col][0] == fig_color:
                if debug: print(f"Rook cant move DOWN because {board_state.loc[i, rook_col]} is blocking my path.")
                break # Cant move past this figure of same color
            else:
                if debug: print(f"We can eat figure DOWN at {rook_col}{i}")
                legal_moves = np.append(legal_moves, f"{rook_col}{i}") # we can eat this figure
                break

        # Checking RIGHT
        for i in range(rook_col_i+1, len(self.columns)): # +1 because we can't move to column we are already in..
            if board_state.loc[rook_row, self.columns[i]] == "ee":
                if debug: print(f"Rook can move to {self.columns[i]}{rook_row}")
                legal_moves = np.append(legal_moves, f"{self.columns[i]}{rook_row}")
            elif board_state.loc[rook_row, self.columns[i]][0] == fig_color:
                if debug: print(f"Rook cant move RIGHT to {self.columns[i]}{rook_row} because {board_state.loc[rook_row, self.columns[i]]} is blocking the way.")
                break
            else:
                if debug: print(f"Rook can eat figure RIGHT at {self.columns[i]}{rook_row}")
                legal_moves = np.append(legal_moves, f"{self.columns[i]}{rook_row}")
                break

        # Checking LEFT
        for i in range(rook_col_i-1, -1, -1): # +1 because we can't move to column we are already in..
            if board_state.loc[rook_row, self.columns[i]] == "ee":
                if debug: print(f"Rook can move to {self.columns[i]}{rook_row}")
                legal_moves = np.append(legal_moves, f"{self.columns[i]}{rook_row}")
            elif board_state.loc[rook_row, self.columns[i]][0] == fig_color:
                if debug: print(f"Rook cant move LEFT to {self.columns[i]}{rook_row} because {board_state.loc[rook_row, self.columns[i]]} is blocking the way.")
                break
            else:
                if debug: print(f"Rook can eat figure LEFT at {self.columns[i]}{rook_row}")
                legal_moves = np.append(legal_moves, f"{self.columns[i]}{rook_row}")
                break

        legal_moves_checked = np.empty(shape=(0,))
        for lm in legal_moves:
            hypothetical_board_state = board_state.copy()
            hypothetical_board_state.loc[rook_row, rook_col] = "ee"
            hypothetical_board_state.loc[int(lm[-1]), lm[0]] = f"{fig_color}r"

            if self.is_my_king_in_check(hypothetical_board_state, fig_color):
                if debug: print(f"Move to {lm} puts KING IN CHECK.")
            else:
                legal_moves_checked = np.append(legal_moves_checked, lm)


        return legal_moves_checked

    def get_knight_legal_moves(self, board_state, from_, fig_color, debug=False): 
        '''
        legal moves for KNIGHT

        Only has like 8 legal moves
        '''
        legal_moves = np.empty(shape=(0,))

        knight_row = int(from_[-1])
        knight_col = from_[0]
        knight_col_i = np.where(self.columns == knight_col)[0][0]

        for r, c in [(1,-2), (2,-1), (2, +1), (1, +2)]: # (r,c)... r tells us how much the rows change (always + and -), c tells us how much columns change (-2, -1, +1, +2)
            if (knight_col_i + c > 7) or (knight_col_i + c < 0):
                continue # Skip since these squares would be out of bounds
            
            if (knight_row + r <= 8):
                if board_state.loc[knight_row+r, self.columns[knight_col_i+c]][0] != fig_color:
                    if debug: print(f"Knight can move to {self.columns[knight_col_i+c]}{knight_row+r}")
                    legal_moves = np.append(legal_moves, f"{self.columns[knight_col_i+c]}{knight_row+r}")

            if (knight_row - r >= 1):
                if board_state.loc[knight_row-r, self.columns[knight_col_i+c]][0] != fig_color:
                    if debug: print(f"Knight can move to {self.columns[knight_col_i+c]}{knight_row-r}")
                    legal_moves = np.append(legal_moves, f"{self.columns[knight_col_i+c]}{knight_row-r}")

        legal_moves_checked = np.empty(shape=(0,))
        for lm in legal_moves:
            hypothetical_board_state = board_state.copy()
            hypothetical_board_state.loc[knight_row, knight_col] = "ee"
            hypothetical_board_state.loc[int(lm[-1]), lm[0]] = f"{fig_color}n"

            if self.is_my_king_in_check(hypothetical_board_state, fig_color):
                if debug: print(f"Move to {lm} puts KING IN CHECK.")
            else:
                legal_moves_checked = np.append(legal_moves_checked, lm)


        return legal_moves_checked

    def get_bishop_legal_moves(self, board_state, from_, fig_color, debug=False): 
        '''
        legal moves for BISHOP

        Similar to ROOK
        '''
        legal_moves = np.empty(shape=(0,))

        bishop_row = int(from_[-1])
        bishop_col = from_[0]
        bishop_col_i = np.where(self.columns == bishop_col)[0][0]

        # Checking left-down
        r = -1
        c = -1
        for i in range(1,9):
            if (bishop_row + r*i < 1) or (bishop_col_i + c*i < 0):
                break # We are out of bounds
            if board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]] == "ee":
                if debug: print(f"Bishop can move to {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
            elif board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]][0] != fig_color:
                if debug: print(f"Bishops can eat figure at {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                break
            else:
                if debug: print(f"Bishop can't move {self.columns[bishop_col_i + c*i]}{bishop_row + r*i} because our figure is blocking the way")
                break # We hit our own figure

        # Checking left-up
        r = +1
        c = -1
        for i in range(1,9):
            if (bishop_row + r*i > 8) or (bishop_col_i + c*i < 0):
                break # We are out of bounds
            if board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]] == "ee":
                if debug: print(f"Bishop can move to {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
            elif board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]][0] != fig_color:
                if debug: print(f"Bishops can eat figure at {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                break
            else:
                if debug: print(f"Bishop can't move {self.columns[bishop_col_i + c*i]}{bishop_row + r*i} because our figure is blocking the way")
                break # We hit our own figure

        # Checking right-up
        r = +1
        c = +1
        for i in range(1,9):
            if (bishop_row + r*i > 8) or (bishop_col_i + c*i > 7):
                break # We are out of bounds
            if board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]] == "ee":
                if debug: print(f"Bishop can move to {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
            elif board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]][0] != fig_color:
                if debug: print(f"Bishops can eat figure at {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                break
            else:
                if debug: print(f"Bishop can't move {self.columns[bishop_col_i + c*i]}{bishop_row + r*i} because our figure is blocking the way")
                break # We hit our own figure

        # Checking right-down
        r = -1
        c = +1
        for i in range(1,9):
            if (bishop_row + r*i < 1) or (bishop_col_i + c*i > 7):
                break # We are out of bounds
            if board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]] == "ee":
                if debug: print(f"Bishop can move to {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
            elif board_state.loc[bishop_row + r*i, self.columns[bishop_col_i + c*i]][0] != fig_color:
                if debug: print(f"Bishops can eat figure at {self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                legal_moves = np.append(legal_moves, f"{self.columns[bishop_col_i + c*i]}{bishop_row + r*i}")
                break
            else:
                if debug: print(f"Bishop can't move {self.columns[bishop_col_i + c*i]}{bishop_row + r*i} because our figure is blocking the way")
                break # We hit our own figure


        legal_moves_checked = np.empty(shape=(0,))
        for lm in legal_moves:
            hypothetical_board_state = board_state.copy()
            hypothetical_board_state.loc[bishop_row, bishop_col] = "ee"
            hypothetical_board_state.loc[int(lm[-1]), lm[0]] = f"{fig_color}b"

            if self.is_my_king_in_check(hypothetical_board_state, fig_color):
                if debug: print(f"Move to {lm} puts KING IN CHECK.")
            else:
                legal_moves_checked = np.append(legal_moves_checked, lm)


        return legal_moves_checked

    def get_queen_legal_moves(self, board_state, from_, fig_color, debug=False): 
        '''
        legal moves for QUEEN

        Just take ROOK and BISHOP moves
        '''
        legal_moves = np.empty(shape=(0,))

        queen_row = int(from_[-1])
        queen_col = from_[0]
        queen_col_i = np.where(self.columns == queen_col)[0][0]

        rook_moves = self.get_rook_legal_moves(board_state, from_, fig_color)
        legal_moves = np.append(legal_moves, rook_moves)

        bishop_moves = self.get_bishop_legal_moves(board_state, from_, fig_color)
        legal_moves = np.append(legal_moves, bishop_moves)

        legal_moves_checked = np.empty(shape=(0,))
        for lm in legal_moves:
            hypothetical_board_state = board_state.copy()
            hypothetical_board_state.loc[queen_row, queen_col] = "ee"
            hypothetical_board_state.loc[int(lm[-1]), lm[0]] = f"{fig_color}q"

            if self.is_my_king_in_check(hypothetical_board_state, fig_color):
                if debug: print(f"Move to {lm} puts KING IN CHECK.")
            else:
                legal_moves_checked = np.append(legal_moves_checked, lm)


        return legal_moves_checked

       
    def get_king_legal_moves(self, board_state, from_, fig_color, debug=False): 
        '''
        Can move for 1 in each direction as long as it doesn't put him in check.
        And opposite king must always be 2 squares away
        '''
        legal_moves = np.empty(shape=(0,))

        king_row = int(from_[-1])
        king_col = from_[0]
        king_col_i = np.where(self.columns == king_col)[0][0]
        
        
        if fig_color == "w":
            for r in [-1,0,+1]:
                if (king_row + r < 1) or (king_row + r > 8):#  out of bounds
                    continue
                for c in [-1, 0, +1]:
                    if r == 0 and c == 0:
                        continue # r==0 and c==0 would mean we stand still
                    if (king_col_i + c < 0) or (king_col_i + c > 7): # out of bounds
                        continue
                    
                    # We will move a king for 1 into some direction into a new_square. Next we need to check if opposing king is too close
                    # We check all the squares (row +1, row-1, col+1, col-1) around the new_square if opposing king is in them. 
                    # But for that we AGAIN need to make a check if the searching grid is out of bounds
                    r_offset_minus = -1 if king_row+r > 1 else 0
                    r_offset_plus = 1 if king_row+r < 8 else 0
                    c_offset_minus = -1 if king_col_i+c > 0 else 0
                    c_offset_plus = 1 if king_col_i+c < 7 else 0
                    if "bk" in board_state.loc[king_row+r + r_offset_minus : king_row+r + r_offset_plus, self.columns[king_col_i+c + c_offset_minus] : self.columns[king_col_i+c + c_offset_plus]].values:
                        if debug: print(f"Can't move to {self.columns[king_col_i+c]}{king_row+r}. Black KING is too close.")
                        continue
                    
                    elif board_state.loc[king_row+r, self.columns[king_col_i+c]][0] != fig_color:
                        if debug: print(f"We can move KING to {self.columns[king_col_i+c]}{king_row+r}")
                        legal_moves = np.append(legal_moves, f"{self.columns[king_col_i+c]}{king_row+r}")


        if fig_color == "b":
            for r in [-1,0,+1]:
                if (king_row + r < 1) or (king_row + r > 8):#  out of bounds
                    continue
                for c in [-1, 0, +1]:
                    if r == 0 and c == 0:
                        continue # r==0 and c==0 would mean we stand still
                    if (king_col_i + c < 0) or (king_col_i + c > 7): # out of bounds
                        continue
                
                    # We will move a king for 1 into some direction into a new_square. Next we need to check if opposing king is too close
                    # We check all the squares (row +1, row-1, col+1, col-1) around the new_square if opposing king is in them. 
                    # But for that we AGAIN need to make a check if the searching grid is out of bounds
                    r_offset_minus = -1 if king_row+r > 1 else 0
                    r_offset_plus = 1 if king_row+r < 8 else 0
                    c_offset_minus = -1 if king_col_i+c > 0 else 0
                    c_offset_plus = 1 if king_col_i+c < 7 else 0
                    if "wk" in board_state.loc[king_row+r + r_offset_minus : king_row+r + r_offset_plus, self.columns[king_col_i+c + c_offset_minus] : self.columns[king_col_i+c + c_offset_plus]].values:
                        if debug: print(f"Can't move to {self.columns[king_col_i+c]}{king_row+r}. White KING is too close.")
                        continue
                    
                    elif board_state.loc[king_row+r, self.columns[king_col_i+c]][0] != fig_color:
                        if debug: print(f"We can move KING to {self.columns[king_col_i+c]}{king_row+r}")
                        legal_moves = np.append(legal_moves, f"{self.columns[king_col_i+c]}{king_row+r}")

        legal_moves_checked = np.empty(shape=(0,))
        for lm in legal_moves:
            hypothetical_board_state = board_state.copy()
            hypothetical_board_state.loc[king_row, king_col] = "ee"
            hypothetical_board_state.loc[int(lm[-1]), lm[0]] = f"{fig_color}k"

            if self.is_my_king_in_check(hypothetical_board_state, fig_color):
                if debug: print(f"Move to {lm} puts KING IN CHECK.")
            else:
                legal_moves_checked = np.append(legal_moves_checked, lm)


        return legal_moves_checked

    def is_my_king_in_check(self, board_state, fig_color, debug=False):
        '''
        Checks if king would be in check in this hypothetical board_state... This way I can also call this function
        with board_states that would be if figure would be moved.. 
        this way figure can't move if it would cuase king to get in check OR figure must move to stop the check

        
        '''        
        if debug: print("Checking if my king is in check")
        if debug: print("Hypothetical BOARD STATE:")
        if debug: print(board_state)
        if debug: print("Fig_color, ", fig_color)
        
        king_pos = np.where(board_state.values == f"{fig_color}k")
        if debug: print("King_pos: ", king_pos)
        if debug: print(f"King is on position {self.columns[king_pos[1][0]]}{king_pos[0][0] + 1}")

        king_row = king_pos[0][0] + 1
        king_col = self.columns[king_pos[1][0]]
        king_col_i = np.where(self.columns == king_col)[0][0]
        
        # Checking left-down for bishops
        r = -1
        c = -1
        for i in range(1,9):
            if (king_row + r*i < 1) or (king_col_i + c*i < 0):
                break # We are out of bounds
            if board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == "e": # Empty square
                continue
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == fig_color: # Our figure is protecting us
                break
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] != fig_color: # There is an opponents figure
                if (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "b") or (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "q"): # There is an opponents figure and its BISHOP or QUEEN
                    if debug: print("Opponents BISHOP or QUEEN is ATTACKING our king from LEFT-DOWN")
                    return True
                else:
                    break # The opponents figure is blocking the way
            
        # Checking left-up
        r = +1
        c = -1
        for i in range(1,9):
            if (king_row + r*i > 8) or (king_col_i + c*i < 0):
                break # We are out of bounds
            if board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == "e": # Empty square
                continue
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == fig_color: # Our figure is protecting us
                break
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] != fig_color: # There is an opponents figure
                if (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "b") or (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "q"): # There is an opponents figure and its BISHOP or QUEEN
                    if debug: print("Opponents BISHOP or QUEEN is ATTACKING our king from LEFT-DOWN")
                    return True
                else:
                    break # The opponents figure is blocking the way

        # Checking right-up
        r = +1
        c = +1
        for i in range(1,9):
            if (king_row + r*i > 8) or (king_col_i + c*i > 7):
                break # We are out of bounds
            if board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == "e": # Empty square
                continue
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == fig_color: # Our figure is protecting us
                break
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] != fig_color: # There is an opponents figure
                if (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "b") or (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "q"): # There is an opponents figure and its BISHOP or QUEEN
                    if debug: print("Opponents BISHOP or QUEEN is ATTACKING our king from LEFT-DOWN")
                    return True
                else:
                    break # The opponents figure is blocking the way

        # Checking right-down
        r = -1
        c = +1
        for i in range(1,9):
            if (king_row + r*i < 1) or (king_col_i + c*i > 7):
                break # We are out of bounds
            if board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == "e": # Empty square
                continue
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] == fig_color: # Our figure is protecting us
                break
            elif board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][0] != fig_color: # There is an opponents figure
                if (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "b") or (board_state.loc[king_row + r*i, self.columns[king_col_i + c*i]][1] == "q"): # There is an opponents figure and its BISHOP or QUEEN
                    if debug: print("Opponents BISHOP or QUEEN is ATTACKING our king from LEFT-DOWN")
                    return True
                else:
                    break # The opponents figure is blocking the way


        # ROOK pathways
        # Checking UP
        for i in range(king_row+1,9):
            if board_state.loc[i, king_col] == "ee":
                continue
            elif board_state.loc[i, king_col][0] == fig_color:
                break # Cant move past this figure of same color
            elif board_state.loc[i, king_col][0] != fig_color:
                if (board_state.loc[i, king_col][1] == "r") or (board_state.loc[i, king_col][1] == "q"):
                    if debug: print(f"Position {king_col}{i} puts king IN CHECK by ROOK or QUEEN")
                    return True
                else:
                    break # The opponents figure is blocking the way

        # Checking DOWN
        for i in range(king_row-1, 0, -1): # rook_row +1 because otherwise it would count "moving to the row you are in" as a legal move
            if board_state.loc[i, king_col] == "ee":
                continue
            elif board_state.loc[i, king_col][0] == fig_color:
                break # Cant move past this figure of same color
            elif board_state.loc[i, king_col][0] != fig_color:
                if (board_state.loc[i, king_col][1] == "r") or (board_state.loc[i, king_col][1] == "q"):
                    if debug: print(f"Position {king_col}{i} puts king IN CHECK by ROOK or QUEEN")
                    return True
                else:
                    break
            

        # Checking RIGHT
        for i in range(king_col_i+1, len(self.columns)): # +1 because we can't move to column we are already in..
            if board_state.loc[king_row, self.columns[i]] == "ee":
                continue
            elif board_state.loc[king_row, self.columns[i]][0] == fig_color:
                break
            elif board_state.loc[king_row, self.columns[i]][0] != fig_color:
                if (board_state.loc[king_row, self.columns[i]][1] == "r") or (board_state.loc[king_row, self.columns[i]][1] == "q"):
                    if debug: print(f"Position {i}{king_row} puts king IN CHECK by ROOK or QUEEN")
                    return True
                else:
                    break

        # Checking LEFT
        for i in range(king_col_i-1, -1, -1): # +1 because we can't move to column we are already in..
            if board_state.loc[king_row, self.columns[i]] == "ee":
                continue
            elif board_state.loc[king_row, self.columns[i]][0] == fig_color:
                break
            elif board_state.loc[king_row, self.columns[i]][0] != fig_color:
                if (board_state.loc[king_row, self.columns[i]][1] == "r") or (board_state.loc[king_row, self.columns[i]][1] == "q"):
                    if debug: print(f"Position {i}{king_row} puts king IN CHECK by ROOK or QUEEN")
                    return True
                else:
                    break


        # Checking KNIGHT moveset
        if debug: print("Checking if Knight is MATING")

        for r, c in [(1,-2), (2,-1), (2, +1), (1, +2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]: # (r,c)... r tells us how much the rows change (always + and -), c tells us how much columns change (-2, -1, +1, +2)
            if (king_col_i + c > 7) or (king_col_i + c < 0) or (king_row + r > 8) or (king_row + r < 1):
                continue # Skip since these squares would be out of bounds

            if board_state.loc[king_row+r, self.columns[king_col_i+c]] == "ee":
                continue
            elif board_state.loc[king_row+r, self.columns[king_col_i+c]][0] != fig_color:
                if board_state.loc[king_row+r, self.columns[king_col_i+c]][1] == "n":
                    if debug: print(f"Position {king_col_i+c}{king_row+r} puts king IN CHECK by KNIGHT")
                    return True


        # Checking PAWN moveset
        if (fig_color == "w") and (king_row < 8) :
            for c in [-1, +1]:
                if (king_col_i + c > 7) or (king_col_i + c < 0):
                    continue
                if board_state.loc[king_row+1, self.columns[king_col_i + c]] == "bp":
                    if debug: print(f"Position {self.columns[king_col_i + c]}{king_row+1} puts king IN CHECK by PAWN")
                    return True

        if (fig_color == "b") and (king_row > 1) :
            for c in [-1, +1]:
                if (king_col_i + c > 7) or (king_col_i + c < 0):
                    continue
                if board_state.loc[king_row-1, self.columns[king_col_i + c]] == "wp":
                    if debug: print(f"Position {self.columns[king_col_i + c]}{king_row-1} puts king IN CHECK by PAWN")
                    return True

        if debug: print("It doesnt put him in check")
        return False
     

