"""
game.py

This module contains the code for a simple game where the player
competes against the computer. The game logic includes handling
player inputs, calculating scores, and determining the winner.
"""
import pandas as pd # type: ignore
from quiz import QuizGame # type: ignore

game_set = pd.read_csv('./game_set.csv')
game = QuizGame(game_set)
game.quiz()
