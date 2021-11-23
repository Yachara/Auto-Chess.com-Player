# Tutorial:
# https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test

# Chrome drivers - https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # The Keys class lets you emulate the stroke of keyboard keys, including special keys like “Shift” and “Return”.
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains # For clicking
from selenium.webdriver.support.ui import WebDriverWait # to wait for element to load
from selenium.webdriver.support import expected_conditions as EC # to wait for element to load
from selenium.webdriver.common.by import By # used to wait for element to load
from selenium.common.exceptions import StaleElementReferenceException # highlight elements changes while getting it. So the element becomes "stale", but I could still get data from it
from selenium.common.exceptions import TimeoutException

import numpy as np
import time
import re # to parse HTML classes
import os # Visual Studio Code has differently defined working directory. This is for debugging

# MY IMPORTS
from dqn.ChessAgent import ChessAgent
from dqn.Reward import Reward # Class used to calculate the reward and use different reward functions



class GameBoard:
    '''
    This class controls the interface with Chess.com, but doesn't control the decission making.
    '''

    def __init__(self, driver, player_input=False):
        '''
        <DESCRIPTION>


        PARAMS
            driver		        obj.selenium.driver 		The "browser" object, through which we get HTML, CSS, JS elemetnts and interactions.
            player_input        bool                        True if we want player to move figures, False otherwise.
            

        RETURNS
            None


        EXCEPTIONS
            None


        '''
        self.driver = driver
        self.player_input = player_input

        # /--  Browser stuff is asynchronous. Sometimes we need to wait for events to happen - element has loaded, element can be clicked, etc...
        wait_time = 20 # Waits for X seconds for element to appear
        self.wait_for_elem = WebDriverWait(self.driver, 
                                            wait_time, # Waits for element to appear. If it doesn't appear in wait_time we get exception (i think) 
                                            ignored_exceptions = [ StaleElementReferenceException ],
                                            )
        
        self.agent = ChessAgent(driver=driver)

        self.reward = Reward()
    

    def set_game_vs_computer(self,
                            opponent="Jimmy-Bot", # Name-Bot .., but I have to put here the actual name as in HTML..
                            color="random"):
        '''
        <DESCRIPTION>


        PARAMS
            opponent		str		Chess.com has Computer opponents of various difficulty. They have names
                Jimmy-Bot                   We play vs Jimmy-Bot
                (other botnames)

            color			str		We can choose the color we want to play as when setting up a game vs Computer
                white						We play as WHITE color
                black						We play as BLACK color
                random						Color we play as is choosen randomly
        

        RETURNS


        EXCEPTIONS


        '''
        self.choose_computer_opponent(opponent=opponent)
        self.choose_color(color=color)
        self.press_play()


    def choose_computer_opponent(self, opponent):
        '''
        Clicks the correct buttons to choose the specified opponent.


        PARAMS
            opponent		str			Chess.com has Computer opponents of various difficulty. They have names like Jimmy-Bot. The variable string must be same as the data-bot-name value in HTML div element, where we click

        RETURNS


        EXCEPTIONS


        '''
        # Clicks on the div of correct computer opponent.
        btn_opponent = self.wait_for_elem.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-bot-name="{opponent}"]'))) 
        btn_opponent.click()

        # Click the "Choose" button which selects the opponent
        btn_choose = self.wait_for_elem.until(EC.presence_of_element_located((By.XPATH, '//button[@title="Choose"]')))
        #input("ENTER to proceede: ")
        btn_choose.click()


    def choose_color(self, color):
        '''
        Clicks the correct buttons to choose the specified color we want to play as.


        PARAMS
            color		str()		We can play as WHITE, BLACK, RANDOM. Each color has its button, defined by specific class name.
                white		class name is mode-selection-white
                black		class name is mode-selection-random
                random		class name is mode-selection-random

        RETURNS


        EXCEPTIONS


        '''
        class_name = ""
        if color == "random":
            class_name = "mode-selection-random"
        elif color == "white":
            class_name = "mode-selection-white"
        elif color == "black":
            class_name = "mode-selection-black"
        btn = self.driver.find_element_by_class_name(class_name)
        btn.click()


    def press_play(self):
        '''
        When the game options are set, we press the play button.


        PARAMS
        

        RETURNS


        EXCEPTIONS


        '''
        # Click the Play button
        btn_play = self.wait_for_elem.until(EC.presence_of_element_located((By.XPATH, '//button[@title="Play"]')))
        print("Clicking Play button.")
        #input("ENTER to proceede")
        btn_play.click()


    def play_match(self):
        '''
        The game loop after we press PLAY button.

        Set all the variables needed (my color, chessbaord dict, etc..).
        Then a while loop, requesting a move from us when its our turn.
        
        TO-DO what happens when game is finished... Continue to next game, etc..

        PARAMS
        

        RETURNS


        EXCEPTIONS


        '''
        self.my_color = self.what_is_my_color()
        self.agent.set_my_color(self.my_color)
        self.create_chessboard_dict()

        while True:
            time.sleep(1)
            whose_move = self.is_my_move()
            if whose_move == "my_move":
                self.make_move()
                reward = self.reward.calc_reward()
            elif whose_move == "match_over":
                break

            
    def what_is_my_color(self):
        '''
        Determines the color we are playing (white or black).

        If we are white, the top row has first <text> element with value 8. If we are black the top row has first <text> element with value 1.
        This value can be found inside element:
        <chess-board ...>
            <svg ...>
                Here are multiple <text> elements which denote the rows (1 to 8) and columns (A to H).
            </svg>

        PARAMS
        

        RETURNS
            str(white)		if our color is WHITE
            str(black)		if our color is BLACK


        EXCEPTIONS
            TO-DO			should throw an error if it can't decide what color is ours.


        '''
        
        print("What is my color")
        
        texts = self.driver.find_elements_by_tag_name("text")
        inner_text = texts[0].text
        
        if inner_text == "8":
            print("My color is WHITE")
            return "white"
        elif inner_text == "1":
            print("My color is BLACK")
            return "black"
        else:
            print("Could not read what my color is. THIS SHOULD THROW AN ERROR")


    def create_chessboard_dict(self):
        '''
        Creates representation of game chess board. Need it to know where to click to move figures.
        Saves it in a 		self.chessboard_dict		variable.
            self.chessboard_dict			(dictionary)		FIELD	- the chessboard name of field (A1, B5, H8...)
                                                                X		- how many pixels to move courser to right, starting at the top left corner
                                                                Y		- how many pixel to move courser down, starting at the top left corner
                {
                    str(FIELD): {
                        "xoffset": int(X),
                        "yoffset": int(Y)
                    }
                }

        PARAMS
        

        RETURNS


        EXCEPTIONS


        '''
        chessboard = self.driver.find_element_by_xpath('//chess-board')

        board_width = chessboard.size["width"]
        board_height = chessboard.size["height"]
        
        self.chessboard_dict = {}
        #  Creating the position dictionary.
        for i in range(1,9):
            col = ""
            if i == 1:
                col = "A" if self.my_color=="white" else "H"
            elif i == 2:
                col = "B" if self.my_color=="white" else "G"
            elif i == 3:
                col = "C" if self.my_color=="white" else "F"
            elif i == 4:
                col = "D" if self.my_color=="white" else "E"
            elif i == 5:
                col = "E" if self.my_color=="white" else "D"
            elif i == 6:
                col = "F" if self.my_color=="white" else "C"
            elif i == 7:
                col = "G" if self.my_color=="white" else "B"
            elif i == 8:
                col = "H" if self.my_color=="white" else "A"

            for j in range(1,9):
                key = col+str(j)
                self.chessboard_dict[key] = {}

                # /- Mathematical equation to calculate on what point to move coursor to click inside the specific chessboard field.
                #	 ((board_width/8) / 2) represents the horizontal middle of field.
                #	 (board_width/8) * (i-1) represents how many fields we need to move. For D that would be 4, since we start in the middle of the first(A1) one.
                self.chessboard_dict[key]["xoffset"] = int(((board_width/8) / 2) + (board_width/8) * (i-1))
                
                #	 ((board_height/8) / 2) represents the vertical middle of field.
                #	 (board_height/8) * x represents how many fields we need to move. We again start in the middle of first(A1) one.
                x = (8-j) if self.my_color == "white" else (j-1)
                self.chessboard_dict[key]["yoffset"] = int(((board_height/8) / 2) + (board_height/8) * x)

    def is_my_move(self, debug=False):
        '''
        Checks if it is our turn to make a move.

        When a move is made (a figure is moved), two squares get highlighted. Starting square and ending square.
        The starting square is the square FROM which the figure moved.
        Ending square is the square TO which the figure moved.
        (Problem is, I don't know what square is the ending sqaure).

        The moved figure is in one of these two highlighted squares.
        We find out the color of the figure, which means the opposite color is now on move.

        The square names are inside element:
        <div ... class="highlight ...">
        Example: <div ... class="highlight square-86" ...>
        We now itterate through every figure, checking in which square it is. When we get a match we check the figures color.


        PROBLEMS can arise at the beggining of the game, when no moves have yet been made. So no square is highlighted.
        We check for existance of <div ... class="highligh ..." > elements. If there are none we check our color. 
        If we are white we need to make the first move. Otherwise, we just wait.

        Another PROBLEM can came, because these highlighted square elements keep changing. So the elements could become stale and we would get an error.
        The problem is "solved" so that, when we get this error, we simply check again for the highlighted squares.


        PARAMS
        

        RETURNS
            "my_move"		    if it is my move
            "opponents_move"    if it is opponents move
            "match_over"		if it match is over


        EXCEPTIONS


        '''
        

        if debug: print("Checking who's move it is.")
        while True:
            if self.is_match_over():
                print("End this match.")
                self.end_match()
                return "match_over"


            try: # Keep looking for "highlight" elements. There could be a StaleElementReferenceException, but after few seconds the elements should settle and i should be able to find them
                hl_sqs = self.driver.find_elements_by_class_name("highlight")
                if hl_sqs == []:
                    # In this case the game has just started and the first move needs to be made.
                    if self.my_color == "white":
                        print("We need to make the FIRST MOVE.")
                        return "my_move"
                    elif self.my_color == "black":
                        print("OPPONENT needs to make the FIRST MOVE.")
                        return "opponents_move"

                color_on_move = "" # Which color has to make a move
                for hl_sq in hl_sqs: # check both highlighted squares since figure  could be in either one.
                    if debug: print("HL_SQ: ", hl_sq.get_attribute("class"))
                    hl_sq_class = hl_sq.get_attribute("class")
                    sq = re.search(r"\d\d", hl_sq_class)[0]                    
                    pieces = self.driver.find_elements_by_class_name("piece")
                    for piece in pieces: # check what piece is inside the highlighted square
                        piece_class = piece.get_attribute("class")
                        piece_sq = re.search(r"\d\d", piece_class)[0]
                        if sq == piece_sq:
                            if debug: print(f"This piece {piece_sq} is in a highlighted square. Getting its color")
                            color_on_move = re.search(r"[w,b]\w", piece_class)[0][0]
                            if color_on_move == "b":
                                color_on_move = "white"
                            elif color_on_move == "w":
                                color_on_move = "black"
                            break

                print("It's", color_on_move.upper(), "turn.")
                if color_on_move == self.my_color:
                    return "my_move"
                else:
                    return "opponents_move"
                    
            except StaleElementReferenceException as e:
                print("StaleElementReferenceException while looking for highlighted elements.")
                print(e)
                

    def is_match_over(self):
        '''
        Checks if the game is over.

        We determine this by checking if element with classname "modal-game-over-header-title" exists.
        This element is created when the game is over and displays some information about the match (like the winner, etc..)

        PARAMS

        RETURNS
            True        bool        The match is over
            False       bool        The match is not yet over
            
        '''
        winner_container = self.driver.find_elements_by_class_name("modal-game-over-header-title")
        if winner_container: # It is not empty array
            print("GAME OVER!!!")
            print(f"Winner is: {winner_container[0].text}")
            return True

        return False

    def end_match(self):
        '''
        When the game is over, the winner is announced. Need to press x to cancle the winner and then we can mvoe on to another game.
        '''
        #x_button = self.driver.find_elements_by_class_name("modal-game-over-header-icon")
        x_button = self.wait_for_elem.until(EC.element_to_be_clickable((By.CLASS_NAME, "modal-game-over-header-icon")))

        #input(f"Press ENTER to click on X to close winner screen. I foud {len(x_button)} many X buttons.")
        x_button.click()

    def make_move(self,
                ):
        '''
        Calls the function to get what figure to move where and calls the function to execute clicks to make this move.
        It determines where to click to "pick up" figure and where to click next to "move figure to that field".

        PARAMS
        

        RETURNS


        EXCEPTIONS


        '''
        print("We are getting a move from agent")
        from_, to_, action = self.agent.get_move(player_input=self.player_input)
        self.reward.state_before_move = self.agent.get_board_state() # This is coded poorly, since I am calling on the agent to get the board state, but ok.
        self.move_from_to(from_=from_, to_=to_)
        self.reward.from_ = from_
        self.reward.to_ = to_
        self.reward.state_after_move = self.agent.get_board_state() # This is coded poorly, since I am calling on the agent to get the board state, but ok.


    def move_from_to(self, from_, to_, debug=True):
        '''
        Execute the necessery clicks to move the figure from its square to its new square.


        PARAMS
            from_		str()		Square name (like "B2") in which figure currently resides.
            to_			str()		Square name (like "B3") where we want to move the figure.
                Both can take values: 	A1, A2, A3, A4, A5, A6, A7, A8
                                        B1, B2, B3, B4, B5, B6, B7, B8
                                        C1, C2, C3, C4, C5, C6, C7, C8
                                        D1, D2, E3, D4, D5, D6, D7, D8
                                        E1, E2, D3, E4, E5, E6, E7, E8
                                        F1, F2, F3, F4, F5, F6, F7, F8
                                        G1, G2, G3, G4, G5, G6, G7, G8
                                        H1, H2, H3, H4, H5, H6, H7, H8

        RETURNS


        EXCEPTIONS


        '''
        if debug: print("Moving from ", from_, " to ", to_)

        chessboard = self.driver.find_element_by_xpath('//chess-board')

        # TO-DO..... Could incorporate some "human-like" pause between clicks maybe...
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(chessboard,
                                            self.chessboard_dict[from_]["xoffset"],
                                            self.chessboard_dict[from_]["yoffset"]
                                            ).click()
        actions.move_to_element_with_offset(chessboard,
                                            self.chessboard_dict[to_]["xoffset"],
                                            self.chessboard_dict[to_]["yoffset"]
                                            ).click()
        actions.perform()

    
    def click_new_game(self):
        '''
        Once the game is over I can click new game and set up another game...
        '''
        btn_new_game = self.driver.find_element_by_xpath('//button[@data-game-control-button="NewGame"]')
        #input("Clicking NEW_GAME button: <press ENTER>")
        btn_new_game.click()







if __name__ == "__main__":
    '''
    Simply starts the whole thing.


    PARAMS
    

    RETURNS


    EXCEPTIONS


    '''
    print("Working directory: ", os.getcwd())


    with webdriver.Chrome('./chromedriver_linux_96-0-4664-45') as driver:
        driver.maximize_window()

        driver.get("https://www.chess.com/play/computer") # Opens browser and goes to specified URL

        wait_time = 10 # Waits for 10 seconds for element to appear
        wait = WebDriverWait(driver, wait_time)
        
        div_cookie_banner = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="cookie-banner"]')))
        btn_agree_cookies = div_cookie_banner.find_elements_by_tag_name("button")[0]
        # Need to agree to cookies at start, otherwise other elements can't be clicked
        print("Clicking to AGREE to Cookies")
        #input("ENTER to proceede: ")
        btn_agree_cookies.click()

        # Getting rid of the info in the middle of screen
        x_icon = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="icon-font-chess x modal-seo-close-icon"]')))
        print("Clicking X to get rid of info")
        #input("ENTER to proceede: ")
        x_icon.click()

        game_board = GameBoard(driver, player_input=False)

        try:
            # /- GAME ON!!!
            for i in range(5):#while input("Press ENTER to play a match. Q to quit").lower() != "q":                
                game_board.set_game_vs_computer(color="random")
                game_board.play_match()
                game_board.click_new_game()
        except Exception as e:
            print("==========\t WE GOT AN EXCEPTION \t=========")
            print(type(e))
            print(e)
            input("Save the chess FEN code to replicate the state. Then press ENTER to exit: ")

