import unittest

from testing.test_main import TestMain
from testing.test_chess_agent import TestChessAgent


if __name__ == "__main__":
    print("RUNNING TESTS")
    # To run a specific test, use the command:   python .\testing.py TestMain.<specific_test_method>
    # python .\testing.py TestMain.test_choose_color
    # python .\testing.py TestChessAgent.test_get_prediction
    unittest.main()


