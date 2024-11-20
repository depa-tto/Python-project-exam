"""
game.py

This module is the main game execution file. Running this file launches 
the quiz game interface, where users can play and answer questions.
"""

import pandas as pd  # type: ignore
from quiz import QuizGame  # type: ignore

game_set = pd.read_csv("./game_set.csv")  # load the game_set dataset
game = QuizGame(game_set)  # initialize the QuizGame object with le loaded fataset
game.quiz()  # start the quiz
