"""
game.py

This module contains the code for a simple game where the player
competes against the computer. The game logic includes handling
player inputs, calculating scores, and determining the winner.
"""
import pandas as pd # type: ignore
from quiz import QuizGame # type: ignore

<<<<<<< HEAD
game_set = pd.read_csv('./game_set.csv')
=======
game_set = pd.read_csv('./merge_set.csv')
game_set(['region'], axis=1, inplace=True)
game_set.drop_duplicates(inplace=True)
game_set.to_csv("game_set.csv")

>>>>>>> dd7dc99c7569ffa8fa3f68f86ac8306836bc5e8c
game = QuizGame(game_set)
game.quiz()
