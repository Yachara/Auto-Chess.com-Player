import unittest 

import pandas as pd
import numpy as np
import time

from dqn.ChessAgent import ChessAgent

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



class TestChessAgent(unittest.TestCase):
    def test_set_my_color(self):
        print("---------------- TESTING set_my_color function ----------------")
        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:

            for color in ["white", "black"]:
                agent = ChessAgent(driver=driver)
                agent.set_my_color(color)
                self.assertEqual(agent.my_color, color)


    def test_get_move(self):
        pass


    def test_get_player_input(self):
        print("---------------- TESTING get_player_input function ----------------")
        print("!!!!!!\t\t This test REQUIRES HUMAN SUPERVISION \t\t!!!!!!")

        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            agent = ChessAgent(driver=driver)
            print("Input B1C3: ")
            result = agent.get_player_input()
            self.assertEqual(result, ("B1", "C3"))

    def test_get_board_state(self):
        print("---------------- TESTING get_board_state function ----------------")
        link = "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"
        print("1. \t Setting up the enviornment.")
        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            agent = ChessAgent(driver=driver)

            driver.maximize_window()
            driver.get(link)
            game_board = main.GameBoard(driver, player_input=False)
            time.sleep(7)
            game_board.my_color = game_board.what_is_my_color()
            game_board.create_chessboard_dict()
            print("2. \t Enviornment has been set up. We should be in a middle of a match.")

            correct_result = pd.DataFrame(data=np.array([["wr", "wn", "wb", "ee", "wk", "ee", "wn", "wr"],
                                                        ["wp", "wp", "wp", "wp", "ee", "wp", "wp", "wp"],
                                                        ["ee", "ee", "ee", "ee", "wp", "wq", "ee", "ee"],
                                                        ["ee", "ee", "wb", "ee", "ee", "ee", "ee", "ee"],
                                                        ["ee", "ee", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                        ["bp", "bp", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                        ["br", "ee", "bp", "bp", "bp", "bp", "bp", "bp"],
                                                        ["ee", "bn", "bb", "bq", "bk", "bb", "bn", "br"]]), 
                                                        index=[1,2,3,4,5,6,7,8], 
                                                        columns=["A", "B", "C", "D", "E", "F", "G", "H"])
            result = agent.get_board_state()
            self.assertEqual(result.equals(correct_result), True)

    def test_get_prediction(self):
        print("---------------- TESTING get_prediction function ----------------")
        link = "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"
        print("1. \t Setting up the enviornment.")
        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            agent = ChessAgent(driver=driver)

            driver.maximize_window()
            driver.get(link)
            game_board = main.GameBoard(driver, player_input=False)
            time.sleep(7)
            game_board.my_color = game_board.what_is_my_color()
            game_board.create_chessboard_dict()
            board_state = agent.get_board_state()

            print("2. \t Enviornment has been set up. We should be in a middle of a match.")
            result = agent.get_prediction(board_state=board_state)
            self.assertEqual(result.shape, (4096,))

    def test_get_input_values(self):
        print("---------------- TESTING get_input_values function ----------------")
        link = "https://www.chess.com/play/computer?moveList=e2e3%20a7a6%20d1f3%20b7b6%20f1c4%20a8a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"
        correct_result = np.array([1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 
                                    0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 
                                    0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0])
        print("1. \t Setting up the enviornment.")
        with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
            agent = ChessAgent(driver=driver)

            driver.maximize_window()
            driver.get(link)
            game_board = main.GameBoard(driver, player_input=False)
            time.sleep(7)
            game_board.my_color = game_board.what_is_my_color()
            game_board.create_chessboard_dict()
            board_state = agent.get_board_state()

            print("2. \t Enviornment has been set up. We should be in a middle of a match.")
            result = agent.get_input_values(board_state=board_state)
            self.assertEqual(np.array_equal(result, correct_result), True, msg=f"The two numpy arrays do not match. result.shape: {result.shape}, correct_result.shape: {correct_result.shape}")


    def test_is_move_legal(self):
        print("---------------- TESTING is_move_legal function ----------------")
        link = "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"
        print("1. \t Setting up the enviornment.")
        for from_, to_, correct_result in [("B2", "F6", True),
                                            ("B2", "H8", False),
                                            ("E1", "E2", False)]:
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)

                driver.maximize_window()
                driver.get(link)
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(10)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                board_state = agent.get_board_state()

                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.is_move_legal(from_=from_, 
                                            to_=to_, 
                                            board_state=board_state)
                self.assertEqual(result, correct_result)

    def test_get_pawn_legal_moves(self):
        print("---------------- TESTING get_pawn_legal_moves function ----------------")
        print("1. \t Setting up the enviornment.")
        for from_, correct_result, link in [("A2", np.array(["A3"]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("B3", np.array(["B4"]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("C2", np.array(["C3", "C4"]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("H4", np.array(["H5", "G5"]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("H7", np.array([]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6%20f2f4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("G5", np.array(["G4", "H4", "F4"]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6%20f2f4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("E6", np.array(["E5"]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6%20f2f4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("C7", np.array(["C6", "C5"]), "https://www.chess.com/play/computer?moveList=e2e3%20b7b6%20g2g3%20c8a6%20b1c3%20g8h6%20c3a4%20d7d6%20b2b3%20g7g6%20h2h3%20f7f6%20c1b2%20g6g5%20h3h4%20e7e6%20f2f4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%20")]:
            print("Enviornment: ")
            print("From_: ", from_)
            print("Correct_result: ", correct_result)
            print("Link: ", link)
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)

                driver.maximize_window()
                driver.get(link)
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(10)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                board_state = agent.get_board_state()

                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.get_pawn_legal_moves(board_state = board_state,
                                                    from_ = from_, 
                                                    fig_color = board_state.loc[int(from_[-1]), from_[0]][0],
                                                    )
                for to_ in correct_result:
                    self.assertIn(to_, result,
                                   msg=f"{to_} cant be found in {result}")
    
    def test_get_rook_legal_moves(self):
        print("---------------- TESTING get_rook_legal_moves function ----------------")
        print("1. \t Setting up the enviornment.")
        for from_, correct_result, link in [("A1", np.array(["A2", "A3"]), "https://www.chess.com/play/computer?moveList=a2a4%20a7a5&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("A8", np.array(["A7", "A6"]), "https://www.chess.com/play/computer?moveList=a2a4%20a7a5%20a1a3&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("D3", np.array(["D4", "D5", "D6", "A3", "B3", "C3", "E3", "F3", "G3", "H3" ]), "https://www.chess.com/play/computer?moveList=a2a4%20a7a5%20a1a3%20a8a6%20a3d3%20d7d6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("A6", np.array(["A7", "A8", "B6", "C6"]), "https://www.chess.com/play/computer?moveList=a2a4%20a7a5%20a1a3%20a8a6%20a3d3%20d7d6%20g2g3&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("E2", np.array(["E3", "E4", "E5", "E6"]), "https://www.chess.com/play/computer?moveList=a2a4%20a7a5%20a1a3%20a8a6%20a3d3%20d7d6%20g2g3%20g7g6%20b2b3%20f8g7%20c1a3%20g7h6%20a3d6%20h6d2%20d3d2%20d8d6%20d2d3%20c7c6%20d3d2%20c8g4%20d1c1%20g4e2%20d2e2%20d6e6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ]:
            print("Enviornment: ")
            print("From_: ", from_)
            print("Correct_result: ", correct_result)
            print("Link: ", link)
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)

                driver.maximize_window()
                driver.get(link)
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(10)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                board_state = agent.get_board_state()

                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.get_rook_legal_moves(board_state = board_state,
                                                    from_ = from_, 
                                                    fig_color = board_state.loc[int(from_[-1]), from_[0]][0],
                                                    )
                for to_ in correct_result:
                    self.assertIn(to_, result,
                                   msg=f"{to_} cant be found in {result}")
                self.assertEqual(len(result), len(correct_result),
                                    msg = f"The lengths dont match. Result len {len(result)}; Correc size {len(correct_result)}")

    def test_get_knight_legal_moves(self):
        print("---------------- TESTING get_knight_legal_moves function ----------------")
        print("1. \t Setting up the enviornment.")
        for from_, correct_result, link in [("B1", np.array(["A3", "C3"]), "https://www.chess.com/play/computer?fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("G1", np.array(["F3", "H3"]), "https://www.chess.com/play/computer?fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("G8", np.array(["H6", "F6"]), "https://www.chess.com/play/computer?moveList=g1f3&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("B8", np.array(["C6", "A6"]), "https://www.chess.com/play/computer?moveList=g1f3&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("H4", np.array(["G6", "F5", "F3"]), "https://www.chess.com/play/computer?moveList=g1f3%20b8c6%20c2c4%20g7g6%20f3h4%20c6d4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("D5", np.array(["B4", "B6", "C3", "C7", "E3", "E7", "F4", "F6"]), "https://www.chess.com/play/computer?moveList=b1c3%20h7h6%20c3d5%20h6h5&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201")
                                            ]:
            print("Enviornment: ")
            print("From_: ", from_)
            print("Correct_result: ", correct_result)
            print("Link: ", link)
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)

                driver.maximize_window()
                driver.get(link)
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(10)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                board_state = agent.get_board_state()

                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.get_knight_legal_moves(board_state = board_state,
                                                    from_ = from_, 
                                                    fig_color = board_state.loc[int(from_[-1]), from_[0]][0],
                                                    )
                for to_ in correct_result:
                    self.assertIn(to_, result,
                                   msg=f"{to_} cant be found in {result}")
                self.assertEqual(len(set(result)), len(set(correct_result)),
                                    msg = f"The lengths dont match. Result len {len(set(result))}; Correc size {len(set(correct_result))}")

    def test_get_bishop_legal_moves(self):
        print("---------------- TESTING get_bishop_legal_moves function ----------------")
        print("1. \t Setting up the enviornment.")
        for from_, correct_result, link in [("C1", np.array(["D2", "E3", "F4", "G5", "H6"]), "https://www.chess.com/play/computer?moveList=g1f3%20b8c6%20c2c4%20g7g6%20f3h4%20c6d4%20d2d3%20b7b6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("F1", np.array([]), "https://www.chess.com/play/computer?moveList=g1f3%20b8c6%20c2c4%20g7g6%20f3h4%20c6d4%20d2d3%20b7b6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("B7", np.array(["C6", "D5", "E4", "F3", "G2", "C8", "A6"]), "https://www.chess.com/play/computer?moveList=g1f3%20b8c6%20c2c4%20g7g6%20f3h4%20c6d4%20d2d3%20b7b6%20c1e3%20c8b7%20e3d4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("D4", np.array(["C3", "C5", "B6", "E3", "E5", "F6", "G7", "H8"]), "https://www.chess.com/play/computer?moveList=g1f3%20b8c6%20c2c4%20g7g6%20f3h4%20c6d4%20d2d3%20b7b6%20c1e3%20c8b7%20e3d4%20e7e6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ]:
            print("Enviornment: ")
            print("From_: ", from_)
            print("Correct_result: ", correct_result)
            print("Link: ", link)
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)

                driver.maximize_window()
                driver.get(link)
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(10)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                board_state = agent.get_board_state()

                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.get_bishop_legal_moves(board_state = board_state,
                                                    from_ = from_, 
                                                    fig_color = board_state.loc[int(from_[-1]), from_[0]][0],
                                                    )
                for to_ in correct_result:
                    self.assertIn(to_, result,
                                   msg=f"{to_} cant be found in {result}")
                self.assertEqual(len(result), len(correct_result),
                                    msg = f"The lengths dont match. Result len {len(result)}; Correc size {len(correct_result)}")


    def test_get_queen_legal_moves(self):
        print("---------------- TESTING get_queen_legal_moves function ----------------")
        print("1. \t Setting up the enviornment.")
        
        for from_, correct_result, link in [("D1", np.array([]), "https://www.chess.com/play/computer?fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("G4", np.array(["D1", "E2", "F3", "F4", "E4", "D4", "C4", "B4", "A4", "F5", "E6", "G5", "H5", "H4", "H3", "G3"]), "https://www.chess.com/play/computer?moveList=e2e3%20e7e6%20d1g4%20g7g5&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("D8", np.array(["E7"]), "https://www.chess.com/play/computer?moveList=e2e3%20e7e6%20d1g4%20g7g5%20g4e6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("E7", np.array(["F8", "D8", "F6", "D6", "C5", "E6", "E5", "E4"]), "https://www.chess.com/play/computer?moveList=e2e3%20e7e6%20d1g4%20g7g5%20g4e6%20f8e7%20e6c4%20e7c5%20c4c5%20d8e7%20e3e4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ]:
            print("Enviornment: ")
            print("From_: ", from_)
            print("Correct_result: ", correct_result)
            print("Link: ", link)
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)

                driver.maximize_window()
                driver.get(link)
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(10)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                board_state = agent.get_board_state()

                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.get_queen_legal_moves(board_state = board_state,
                                                    from_ = from_, 
                                                    fig_color = board_state.loc[int(from_[-1]), from_[0]][0],
                                                    )
                for to_ in correct_result:
                    self.assertIn(to_, result,
                                   msg=f"{to_} cant be found in {result}")
                self.assertEqual(len(result), len(correct_result),
                                    msg = f"The lengths dont match. Result len {len(result)}; Correc size {len(correct_result)}")


    def test_get_king_legal_moves(self):
        print("---------------- TESTING get_king_legal_moves function ----------------")
        print("1. \t Setting up the enviornment.")
        for from_, correct_result, link in [("E8", np.array(["F8", "D8"]), "https://www.chess.com/play/computer?moveList=e2e3%20e7e6%20d1g4%20g7g5%20g4e6%20f8e7%20e6c4%20e7c5%20c4c5%20d8e7%20e3e4&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("E1", np.array(["D1", "E2"]), "https://www.chess.com/play/computer?moveList=e2e3%20e7e6%20d1g4%20g7g5%20g4e6%20f8e7%20e6c4%20e7c5%20c4c5%20d8e7%20e3e4%20d7d6&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("D8", np.array([]), "https://www.chess.com/play/computer?moveList=e2e3%20e7e6%20d1g4%20g7g5%20g4e6%20f8e7%20e6c4%20e7c5%20c4c5%20d8e7%20e3e4%20d7d6%20f1b5%20e8d8%20e1e2&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("F3", np.array(["G3"]), "https://www.chess.com/play/computer?moveList=e2e3%20e7e6%20d1g4%20g7g5%20g4e6%20f8e7%20e6c4%20e7c5%20c4c5%20d8e7%20e3e4%20d7d6%20f1b5%20e8d8%20e1e2%20e7e4%20c5e3%20e4c4%20e2f3%20c4b5%20b1c3%20b5d3&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ("D7", np.array(["E8", "E6"]), "https://www.chess.com/play/computer?moveList=b1c3%20d7d6%20c3b5%20e8d7%20b5a7&fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20w%20KQkq%20-%200%201"),
                                            ]:
            print("Enviornment: ")
            print("From_: ", from_)
            print("Correct_result: ", correct_result)
            print("Link: ", link)
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)

                driver.maximize_window()
                driver.get(link)
                game_board = main.GameBoard(driver, player_input=False)
                time.sleep(10)
                game_board.my_color = game_board.what_is_my_color()
                game_board.create_chessboard_dict()
                board_state = agent.get_board_state()

                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.get_king_legal_moves(board_state = board_state,
                                                    from_ = from_, 
                                                    fig_color = board_state.loc[int(from_[-1]), from_[0]][0],
                                                    )
                for to_ in correct_result:
                    self.assertIn(to_, result,
                                   msg=f"{to_} cant be found in {result}")
                self.assertEqual(len(result), len(correct_result),
                                    msg = f"The lengths dont match. Result len {len(result)}; Correc size {len(correct_result)}")

    def test_is_my_king_in_check(self):
        print("---------------- TESTING is_my_king_in_check function ----------------")
        print("1. \t Setting up the enviornment.")
        for fig_col, correct_result, board_state in [("w", True , pd.DataFrame(data=np.array([  ["wr", "wn", "wb", "wk", "ee", "ee", "wn", "wr"],
                                                                                                ["wp", "wp", "wp", "wp", "bb", "wp", "wp", "wp"],
                                                                                                ["ee", "ee", "ee", "ee", "wp", "wq", "ee", "ee"],
                                                                                                ["ee", "ee", "wb", "ee", "ee", "ee", "ee", "ee"],
                                                                                                ["ee", "ee", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                                ["bp", "bp", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                                ["br", "ee", "bp", "bp", "bp", "bp", "bp", "bp"],
                                                                                                ["ee", "bn", "bb", "bq", "bk", "ee", "bn", "br"]]), 
                                                                                                index=[1,2,3,4,5,6,7,8], 
                                                                                                columns=["A", "B", "C", "D", "E", "F", "G", "H"])),
                                                ("w" ,True, pd.DataFrame(data=np.array([["wr", "wn", "wb", "ee", "ee", "ee", "wn", "wr"],
                                                                                        ["wp", "wp", "wp", "wp", "ee", "wp", "wp", "wp"],
                                                                                        ["ee", "ee", "ee", "ee", "wp", "wq", "ee", "ee"],
                                                                                        ["ee", "ee", "wb", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["ee", "ee", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["bp", "bp", "ee", "ee", "ee", "ee", "wk", "ee"],
                                                                                        ["br", "ee", "bp", "bp", "bp", "bp", "bp", "bp"],
                                                                                        ["ee", "bn", "bb", "bq", "bk", "bb", "bn", "br"]]), 
                                                                                        index=[1,2,3,4,5,6,7,8], 
                                                                                        columns=["A", "B", "C", "D", "E", "F", "G", "H"])),
                                                ("w", False, pd.DataFrame(data=np.array([   ["wr", "wn", "wb", "ee", "wk", "ee", "wn", "wr"],
                                                                                            ["wp", "wp", "wp", "wp", "ee", "wp", "wp", "wp"],
                                                                                            ["ee", "ee", "ee", "ee", "wp", "wq", "ee", "ee"],
                                                                                            ["ee", "ee", "wb", "ee", "ee", "ee", "ee", "ee"],
                                                                                            ["ee", "ee", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                            ["bp", "bp", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                            ["br", "ee", "bp", "bp", "bp", "bp", "bp", "bp"],
                                                                                            ["ee", "bn", "bb", "bq", "bk", "bb", "bn", "br"]]), 
                                                                                            index=[1,2,3,4,5,6,7,8], 
                                                                                            columns=["A", "B", "C", "D", "E", "F", "G", "H"])),
                                                ("b", True, pd.DataFrame(data=np.array([["wr", "wn", "wb", "ee", "wk", "ee", "wn", "wr"],
                                                                                        ["wp", "wp", "wp", "wp", "ee", "wp", "wp", "wp"],
                                                                                        ["ee", "ee", "ee", "ee", "wp", "wq", "ee", "ee"],
                                                                                        ["ee", "ee", "wb", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["ee", "ee", "ee", "ee", "ee", "ee", "ee", "bk"],
                                                                                        ["bp", "bp", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["br", "ee", "bp", "bp", "bp", "bp", "bp", "bp"],
                                                                                        ["ee", "bn", "bb", "bq", "ee", "bb", "bn", "br"]]), 
                                                                                        index=[1,2,3,4,5,6,7,8], 
                                                                                        columns=["A", "B", "C", "D", "E", "F", "G", "H"])),
                                                ("b", False, pd.DataFrame(data=np.array([["wr", "wn", "wb", "ee", "wk", "ee", "wn", "wr"],
                                                                                        ["wp", "wp", "wp", "wp", "ee", "wp", "wp", "wp"],
                                                                                        ["ee", "ee", "ee", "ee", "wp", "wq", "ee", "ee"],
                                                                                        ["ee", "ee", "wb", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["ee", "ee", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["bp", "bp", "ee", "ee", "ee", "ee", "ee", "bk"],
                                                                                        ["br", "ee", "bp", "bp", "bp", "bp", "bp", "bp"],
                                                                                        ["ee", "bn", "bb", "bq", "ee", "bb", "bn", "br"]]), 
                                                                                        index=[1,2,3,4,5,6,7,8], 
                                                                                        columns=["A", "B", "C", "D", "E", "F", "G", "H"])),
                                                ("b", True, pd.DataFrame(data=np.array([["wr", "ee", "wb", "ee", "wk", "ee", "wn", "wr"],
                                                                                        ["wp", "wp", "wp", "wp", "ee", "wp", "wp", "wp"],
                                                                                        ["ee", "wn", "ee", "ee", "wp", "wq", "ee", "ee"],
                                                                                        ["ee", "ee", "wb", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["bk", "ee", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["bp", "bp", "ee", "ee", "ee", "ee", "ee", "ee"],
                                                                                        ["br", "ee", "bp", "bp", "bp", "bp", "bp", "bp"],
                                                                                        ["ee", "bn", "bb", "bq", "ee", "bb", "bn", "br"]]), 
                                                                                        index=[1,2,3,4,5,6,7,8], 
                                                                                        columns=["A", "B", "C", "D", "E", "F", "G", "H"])),
                                                ]:
            print("Enviornment: ")
            print("fig_col: ", fig_col)
            print("Correct_result: ", correct_result)
            print("board_state: ", board_state)
            with webdriver.Chrome('C:\\Mine\\Python\\AI\\Chess\\chromedriver.exe') as driver:
                agent = ChessAgent(driver=driver)
                print("2. \t Enviornment has been set up. We should be in a middle of a match.")
                result = agent.is_my_king_in_check(board_state = board_state,
                                                    fig_color = fig_col,
                                                    )
                self.assertEqual(result, correct_result)
