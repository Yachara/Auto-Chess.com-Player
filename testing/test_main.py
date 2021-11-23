import unittest
import main

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

import pandas as pd
import numpy as np
import time


class TestMain(unittest.TestCase):
    def test_choose_computer_opponent(self):
        print("---------------- TESTING choose_computer_opponent function ----------------")

        for opponent in ["Jimmy-Bot", "Elani-Bot"]:
            print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")
            print("1. \t Setting up the enviornment.")
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                driver.maximize_window()
                driver.get("https://www.chess.com/play/computer")
                wait_time = 10
                wait = WebDriverWait(driver, wait_time)
                div_cookie_banner = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="cookie-banner"]')))
                btn_agree_cookies = div_cookie_banner.find_elements_by_tag_name("button")[0]
                btn_agree_cookies.click()
                x_icon = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="icon-font-chess x modal-seo-close-icon"]')))
                x_icon.click()
                game_board = main.GameBoard(driver, player_input=False)

                print("2. \t Enviornment has been set up. We should be in a menu where we select the computer opponent.")
                computer_opponent = opponent
                print(f"We are choosing {computer_opponent} as opponent.")
                input("Press ENTER to continue with testing: ")
                game_board.choose_computer_opponent(computer_opponent)

                print(f"The test has finished. We should'ev selected {computer_opponent} as our opponent and went to the next screen.")
                result = input("Was test successful? [Y / N]: ").lower()
                self.assertEqual(result, "y")

    def test_choose_color(self):
        print("---------------- TESTING choose_color function ----------------")

        for color in ["white", "black", "random"]:
            print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")
            print("1. \t Setting up the enviornment.")
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                driver.maximize_window()
                driver.get("https://www.chess.com/play/computer")
                wait_time = 10
                wait = WebDriverWait(driver, wait_time)
                div_cookie_banner = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="cookie-banner"]')))
                btn_agree_cookies = div_cookie_banner.find_elements_by_tag_name("button")[0]
                btn_agree_cookies.click()
                x_icon = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="icon-font-chess x modal-seo-close-icon"]')))
                x_icon.click()
                game_board = main.GameBoard(driver, player_input=False)
                game_board.choose_computer_opponent("Jimmy-Bot")

                print("2. \t Enviornment has been set up. We should be in a menu where we select the color we want to play as.")
                print(f"\t\t We are choosing {color} as our color.")
                input("Press ENTER to continue with testing: ")
                game_board.choose_color(color=color)
                print(f"The test has finished. We should'ev selected {color.upper()} as our color and went to the next screen.")
                result = input("Was test successful? [Y / N]: ").lower()
                self.assertEqual(result, "y")

    def test_press_play(self):
        print("---------------- TESTING press_play function ----------------")   
        print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")
        print("1. \t Setting up the enviornment.")
        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            driver.maximize_window()
            driver.get("https://www.chess.com/play/computer")
            wait_time = 10
            wait = WebDriverWait(driver, wait_time)
            div_cookie_banner = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="cookie-banner"]')))
            btn_agree_cookies = div_cookie_banner.find_elements_by_tag_name("button")[0]
            btn_agree_cookies.click()
            x_icon = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="icon-font-chess x modal-seo-close-icon"]')))
            x_icon.click()
            game_board = main.GameBoard(driver, player_input=False)
            game_board.choose_computer_opponent("Jimmy-Bot")
            game_board.choose_color(color="white")
            
            print("2. \t Enviornment has been set up. We should be in a menu where we need to PRESS PLAY.")
            input("Press ENTER to continue with testing: ")
            game_board.press_play()
            print(f"The test has finished. We should'ev selected PRESSED PLAY and went to the next screen.")
            result = input("Was test successful? [Y / N]: ").lower()
            self.assertEqual(result, "y")

    def test_what_is_my_color(self):
        print("---------------- TESTING what_is_my_color function ----------------") 
        print("1. \t Setting up the enviornment.")
        color = "white"

        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            driver.maximize_window()
            driver.get("https://www.chess.com/play/computer")
            wait_time = 10
            wait = WebDriverWait(driver, wait_time)
            div_cookie_banner = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="cookie-banner"]')))
            btn_agree_cookies = div_cookie_banner.find_elements_by_tag_name("button")[0]
            btn_agree_cookies.click()
            x_icon = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="icon-font-chess x modal-seo-close-icon"]')))
            x_icon.click()
            game_board = main.GameBoard(driver, player_input=False)
            game_board.choose_computer_opponent("Jimmy-Bot")
            game_board.choose_color(color=color)
            print("2. \t Enviornment has been set up.")
                
            game_board.press_play()
            result = game_board.what_is_my_color()
            self.assertEqual(result, color)

    def test_chessboard_dict(self):
        '''
        Checks if the chessboard_dict correctly represents the actual board.

        It will right click every field (highlighting it red), from A1, A2, A3, ..., B1, B2, B3, ... H6, H7, H8.
        At the end it will left-click E5, because the red highlight can confuse the program. Left-clicking the board gets rid of any red highlight.
        '''
        print("---------------- TESTING chessboard_dict function ----------------")    
        print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")

        for color in ["white", "black"]:
            print("1. \t Setting up the enviornment.")
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                driver.maximize_window()
                driver.get("https://www.chess.com/play/computer")
                wait_time = 10
                wait = WebDriverWait(driver, wait_time)
                div_cookie_banner = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="cookie-banner"]')))
                btn_agree_cookies = div_cookie_banner.find_elements_by_tag_name("button")[0]
                btn_agree_cookies.click()
                x_icon = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="icon-font-chess x modal-seo-close-icon"]')))
                x_icon.click()
                game_board = main.GameBoard(driver, player_input=False)
                game_board.choose_computer_opponent("Jimmy-Bot")
                game_board.choose_color(color=color)
                game_board.press_play()
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()

                print("2. \t Enviornment has been set up. We should be in a match.")
                print("\t\t Checking if positions are calibrated correctly.")
                print("\t\t Will right-click every position, coloring it red. The position we clicked will be printed out into console.")
                input("Press ENTER to continue with the test: ")
                chessboard = game_board.driver.find_element_by_xpath('//chess-board')

                for key in game_board.chessboard_dict.keys():
                    actions = ActionChains(game_board.driver)
                    print("Clicking ", key, game_board.chessboard_dict[key]["xoffset"], game_board.chessboard_dict[key]["yoffset"])
                    #input("Press ENTER: ")
                    actions.move_to_element_with_offset(chessboard,
                                                        game_board.chessboard_dict[key]["xoffset"],
                                                        game_board.chessboard_dict[key]["yoffset"]
                                                        ).context_click()
                    actions.pause(0.3)
                    actions.perform() # Executes all actions stored in the ActionChain
                    
                key = "E5" # At the end, left-click random key position to get rid of these red highlights, since it could mess up the program.
                actions = ActionChains(game_board.driver)
                actions.move_to_element_with_offset(chessboard,
                                                        game_board.chessboard_dict[key]["xoffset"],
                                                        game_board.chessboard_dict[key]["yoffset"]
                                                        ).click()
                actions.perform()
                print(f"The test has finished.")
                result = input("Was test successful? [Y / N]: ").lower()
                self.assertEqual(result, "y")

    def test_is_my_move(self):
        print("---------------- TESTING is_my_move function ----------------")
        print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")

        for correct_result, link in [("my_move", "https://www.chess.com/play/computer?moveList=d2d3%20g7g6%20g2g4%20g8f6%20e2e3%20f8h6%20f1g2%20b7b5%20d1f3&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"), 
                                    ("my_move", "https://www.chess.com/play/computer?moveList=d2d3%20g7g6%20g2g4%20g8f6%20e2e3%20f8h6%20f1g2%20b7b5%20d1f3%20c7c6%20b2b3%20c8a6%20d3d4%20d8c7%20c2c4%20b5c4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                    ("opponents_move", "https://www.chess.com/play/computer?moveList=d2d3%20g7g6%20g2g4%20g8f6%20e2e3%20f8h6%20f1g2%20b7b5%20d1f3%20c7c6%20b2b3%20c8a6%20d3d4%20d8c7%20c2c4%20b5c4%20f3c6%20c7g3%20h2g3%20a6c8%20c6f3%20g6g5&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201")]:
            print("1. \t Setting up the enviornment.")
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                driver.maximize_window()
                driver.get(link)
                
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(7)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                game_board.wait_for_elem.until(EC.presence_of_element_located((By.CSS_SELECTOR , f'.highlight')))
                
                if correct_result == "opponents_move":
                    game_board.move_from_to(from_="C1", to_="A3")
                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = game_board.is_my_move()
                input(f"Result is: {result}")
                self.assertEqual(result, correct_result)

    def test_is_match_over(self):
        print("---------------- TESTING is_match_over function ----------------")       
        print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")
        for correct_result, input_, link in [(True, "F3F7", "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            (False, "F3F6", "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201")]:
                
            print("1. \t Setting up the enviornment.")
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                driver.maximize_window()
                driver.get(link)
                
                game_board = main.GameBoard(driver, player_input=True)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                game_board.wait_for_elem.until(EC.presence_of_element_located((By.CSS_SELECTOR , f'.highlight')))
                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                
                from_ = input_[:2]
                to_ = input_[-2:]
                print(f"We will be making move from ", from_, " to ", to_)
                input("Press ENTER to cont. ")
                game_board.move_from_to(from_=from_, to_=to_)

                result = game_board.is_match_over()
                input(f"Result is: {result}")
                self.assertEqual(result, correct_result)

    def test_end_match(self):
        print("---------------- TESTING end_match function ----------------")       
        print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")
        link = "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"
        input_ = "F3F7"  
        
        print("1. \t Setting up the enviornment.")
        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            driver.maximize_window()
            driver.get(link)
            
            game_board = main.GameBoard(driver, player_input=True)
            game_board.my_color = game_board.what_is_my_color()
            game_board.create_chessboard_dict()
            game_board.wait_for_elem.until(EC.presence_of_element_located((By.CSS_SELECTOR , f'.highlight')))
            print("2. \t Enviornment has been set up. We should be in a middle of a match.")
            
            from_ = input_[:2]
            to_ = input_[-2:]
            print(f"We will be making move from ", from_, " to ", to_)
            input("Press ENTER to cont. ")
            game_board.move_from_to(from_=from_, to_=to_)
            
            if game_board.is_match_over():
                print("The game is over.")
            else:
                print("SOMETHING IS WRONG! The game should'ev been over.")
            
            print("Now we will test the end_match function. The <X> will be pressed and the displaying notification should be closed.")
            #input(f"Press ENTER to cont. ")
            game_board.end_match()
            
            print(f"The test has finished. We should'ev closed the winner notification screen.")
            result = input("Was test successful? [Y / N]: ").lower()
            self.assertEqual(result, "y")

    def test_move_from_to(self):
        print("---------------- TESTING move_from_to function ----------------")

        for input_, fig_moved, link in [("F3F6", "wq", "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                        ("A2A3", "wp", "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                        ("G7G6", "bp", "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7%20d2d3&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201")]:
            print("1. \t Setting up the enviornment.")
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                driver.maximize_window()
                driver.get(link)
                
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(7) # need to wait few seconds for the javascript to execute all the moves and rotate the chessboard correct.y
                game_board.my_color = game_board.what_is_my_color()              
                game_board.create_chessboard_dict()
                game_board.wait_for_elem.until(EC.presence_of_element_located((By.CSS_SELECTOR , f'.highlight')))
                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                from_ = input_[:2]
                to_ = input_[-2:]
                print(f"We will be making move from ", from_, " to ", to_)
                game_board.move_from_to(from_=from_, to_=to_)
                board_state = game_board.agent.get_board_state()
                result = board_state.loc[int(to_[-1]), to_[0]]
                self.assertEqual(result, fig_moved)

    def test_click_new_game(self):
        print("---------------- TESTING click_new_game function ----------------")
        print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")
        link = "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"
        input_ = "F3F7"  
        
        print("1. \t Setting up the enviornment.")
        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            driver.maximize_window()
            driver.get(link)
            
            game_board = main.GameBoard(driver, player_input=True)
            game_board.my_color = game_board.what_is_my_color()
            game_board.create_chessboard_dict()
            game_board.wait_for_elem.until(EC.presence_of_element_located((By.CSS_SELECTOR , f'.highlight')))
            print("2. \t Enviornment has been set up. We should be in a middle of a match.")
            
            from_ = input_[:2]
            to_ = input_[-2:]
            print(f"We will be making move from ", from_, " to ", to_)
            input("Press ENTER to cont. ")
            game_board.move_from_to(from_=from_, to_=to_)
            
            if game_board.is_match_over():
                game_board.end_match()
            else:
                print("SOMETHING IS WRONG. The match should be over.")

            input("Press ENTER to execute the test.")
            game_board.click_new_game()         
            print(f"The test has finished. We should'ev opened new game.")
            result = input("Was test successful? [Y / N]: ").lower()
            self.assertEqual(result, "y")