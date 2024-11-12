"""
quiz.py

This module contains the logic for a quiz application.
It includes functions to ask questions, validate answers, calculate scores, and display results to the user.
"""

import time  # type: ignore
import random  # type: ignore
import pandas as pd  # type: ignore
from termcolor import cprint  # type: ignore


class QuizGame:
    """
    A class to represent a quiz game with various questions and scoring.

    Attributes:
        dataset: A pandas DataFrame containing movie and TV series data, with details like
                 title, start_year, genre, etc.
        score: Tracks the user's score throughout the game.

    Methods:
        __init__(dataset): Initializes the quiz game with a given dataset.
        difficulty(): Prompts the user to choose a difficulty level (easy, medium, or hard),
                      and filters the dataset accordingly.
        first_question(): Generates the first question based on a random entry from the dataset.
        second_question(): Generates the second question based on a random entry from the dataset.
        third_question(): Generates the third question based on a random entry from the dataset.
        fourth_question(): Generates the fourth question based on a random entry from the dataset.
        score_fun(my_answer, correct_answer, dif): Calculates and updates the score based on the user's answer.
        gen_answers(correct_answer): Generates answer choices (including the correct one and 3 incorrect options).
        ask_question(question, correct_answer, choices): Displays the question and choices, and gets the user's answer.
        rounds(): Prompts the user for the number of rounds they want to play.
        quiz(): Main function to conduct the quiz game, handle rounds, and display results.
    """

    def __init__(self, dataset):
        """
        Initializes the quiz game with the provided dataset.

        Args:
            dataset: A pandas DataFrame containing the quiz dataset.
        """
        self.dataset = dataset
        self.score = 0

    def difficulty(self):
        """
        Prompts the user to choose a difficulty level and filters the dataset accordingly.

        The user selects between easy, medium, and hard difficulty.
        The dataset is then filtered based on the selected difficulty level.

        Returns:
            The filtered dataset and the chosen difficulty level.
        """
        while True:
            dif = (
                str(
                    input(
                        "🔸 Please choose the difficulty between easy, medium and hard: "
                    )
                )
                .strip()
                .lower()
            )
            if dif not in ["hard", "medium", "easy"]:
                print("🔸 Please insert a proper difficulty ")
            else:
                if dif == "hard":
                    self.dataset = self.dataset[(self.dataset["start_year"] <= 1974)]
                    print("🔸 Rules: +1 if you are correct, -1 otherwise")
                elif dif == "medium":
                    self.dataset = self.dataset[
                        (self.dataset["start_year"] >= 1975)
                        & (self.dataset["start_year"] <= 2004)
                        & (
                            self.dataset["first_profession"].isin(
                                ["actor", "actress", "writer", "producer", "director"]
                            )
                        )
                    ]
                    print("🔸 Rules: +1 if you are correct, -0.5 otherwise")
                elif dif == "easy":
                    self.dataset = self.dataset[
                        (self.dataset["start_year"] >= 2005)
                        & (
                            self.dataset["first_profession"].isin(
                                ["actor", "actress", "writer", "producer", "director"]
                            )
                        )
                        & (
                            ~self.dataset["genre_1"].isin(
                                [
                                    "Documentary",
                                    "Talk-Show",
                                    "Game-Show",
                                    "Sci-Fi",
                                    "News",
                                    "History",
                                    "Reality-TV",
                                    "Short",
                                    "Adult",
                                ]
                            )
                        )
                    ]
                    print("🔸 Rules: +1 if you are correct, 0 otherwise")
                return self.dataset, dif

    def first_question(self):
        """
        Generates the first question based on a random entry from the dataset.

        This question asks about the year of production of a movie.

        Returns:
            The question string and the correct answer (production year).
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        title = self.dataset["title"].iloc[indices]
        name_surname = self.dataset["name_surname"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        movie_type = self.dataset["type"].iloc[indices]
        correct_answer = self.dataset["start_year"].iloc[indices]
        question = f"In which year was the {movie_type} '{title}' of {name_surname} as a {role} component produced ?"
        return question, correct_answer

    def second_question(self):
        """
        Generates the second question based on a random entry from the dataset.

        This question asks about the genre of a movie.

        Returns:
            The question string and the correct answer (genre).
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        title = self.dataset["title"].iloc[indices]
        name_surname = self.dataset["name_surname"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        movie_type = self.dataset["type"].iloc[indices]
        year = self.dataset["start_year"].iloc[indices]
        correct_answer = self.dataset["genre_1"].iloc[indices]
        question = f"What genre is the {movie_type} '{title}' made in {year} of {name_surname} as a {role} component ?"
        return question, correct_answer

    def third_question(self):
        """
        Generates the third question based on a random entry from the dataset.

        This question asks about the title of a movie.

        Returns:
            The question string and the correct answer (movie title).
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        movie_type = self.dataset["type"].iloc[indices]
        name_surname = self.dataset["name_surname"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        year = self.dataset["start_year"].iloc[indices]
        correct_answer = self.dataset["title"].iloc[indices]
        question = f"What was the title of the {movie_type} made in {year} with {name_surname} as a {role} component ?"
        return question, correct_answer

    def fourth_question(self):
        """
        Generates the fourth question based on a random entry from the dataset.

        This question asks about the name of the person involved in a movie.

        Returns:
            The question string and the correct answer (person's name).
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        movie_type = self.dataset["type"].iloc[indices]
        title = self.dataset["title"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        year = self.dataset["start_year"].iloc[indices]
        correct_answer = self.dataset["name_surname"].iloc[indices]
        question = (
            f"Who was the {role} of the {movie_type} named '{title}' made in {year} ?"
        )
        return question, correct_answer

    def score_fun(self, my_answer, correct_answer, dif):
        """
        Calculates and updates the score based on the user's answer.

        The score is updated according to the correctness of the answer:
        - For correct answers: +1 point.
        - For incorrect answers: a penalty based on the difficulty level.

        Args:
            my_answer: The user's answer.
            correct_answer: The correct answer to the question.
            dif: The difficulty level of the quiz.

        Returns:
            The updated score.
        """
        if my_answer == correct_answer:
            self.score += 1
            cprint(
                f"✅ You are correct, '{correct_answer}' is the right answer", "green"
            )
            print(f"Your current score is: {self.score}")
        else:
            cprint(
                f"❌ Your answer was '{my_answer}' but the correct one is '{correct_answer}'",
                "red",
            )
            if dif == "hard":
                self.score -= 1
            elif dif == "medium":
                self.score -= 0.5

            if self.score < 0:
                self.score = 0
            print(f"Your current score is: {self.score}")
        return self.score

    def gen_answers(self, correct_answer):
        """
        Generates a list of answer choices including the correct answer and three incorrect answers.

        The incorrect answers are randomly selected based on the correct answer's type (year, genre, title, etc.).

        Args:
            correct_answer: The correct answer for the question.

        Returns:
            A list of four answer choices (one correct, three incorrect).
        """
        if correct_answer in self.dataset["start_year"].values:
            incorrect_ans = [
                correct_answer - random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]),
                correct_answer + random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]),
                correct_answer - random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50]),
            ]
            adjusted_incorrect_ans = []
            for i in incorrect_ans:
                while i >= time.localtime().tm_year:
                    i -= 1
                adjusted_incorrect_ans.append(i)
            options = [correct_answer] + adjusted_incorrect_ans
            random.shuffle(options)
            return options
        if correct_answer in self.dataset["genre_1"].values:
            incorrect_ans = random.sample(list(self.dataset["genre_1"].unique()), 3)
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(
                        list(self.dataset["genre_1"].unique()), 3
                    )
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options
        if correct_answer in self.dataset["title"].values:
            incorrect_ans = random.sample(list(self.dataset["title"].unique()), 3)
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(
                        list(self.dataset["title"].unique()), 3
                    )
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options
        if correct_answer in self.dataset["name_surname"].values:
            incorrect_ans = random.sample(
                list(self.dataset["name_surname"].unique()), 3
            )
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(
                        list(self.dataset["name_surname"].unique()), 3
                    )
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options

    def ask_question(self, question, correct_answer, choices):
        """
        Displays the question, answer choices, and prompts the user for an answer.

        Args:
            question: The question to be asked.
                - A string that represents the question to display.
            correct_answer: The correct answer to the question.
                - The correct answer is compared to the user's input.
            choices: A list of answer choices.
                - A list of possible answers to the question, including the correct answer.

        Returns:
            - The user's selected answer (chosen_answer).
            - The correct answer (correct_answer).
        """
        letters = ["A", "B", "C", "D"]
        print(question)
        for j, choice in zip(letters, choices):
            print(f"{j}. {choice}")
        while True:
            my_answer = input("Enter your answer (A, B, C, or D): ").upper()
            if my_answer in letters:
                break
            print("Invalid input. Please enter A, B, C, or D.")
        chosen_index = letters.index(my_answer)
        chosen_answer = choices[chosen_index]
        return chosen_answer, correct_answer

    def rounds(self):
        """Prompts the user for the number of rounds they wish to play.

        The user can select the number of rounds and then the quiz will proceed accordingly.

        Returns:
            The number of rounds to be played.
        """
        while True:
            try:
                n_round = int(input("🔸 How many rounds do you want to play? "))
                if n_round > 0:
                    return n_round
                else:
                    print("🔸 Please enter a positive number of rounds ")
            except ValueError:
                print("🔸 Please enter a positive number of rounds ")

    def quiz(self):
        """
        Main function to conduct the quiz game.

        This function handles the flow of the game, including selecting the difficulty,
        asking questions, and keeping track of the score.
        """
        cprint(
            "🎬 Welcome to the quiz game about movies and tv series!®️ ", attrs=["bold"]
        )
        self.score = 0
        while True:
            self.dataset, dif = self.difficulty()
            n_round = self.rounds()
            cprint(
                f"👉 You are going to play for {n_round} rounds at {dif} level",
                attrs=["bold"],
            )
            start_time = time.time()
            question_funcs = [
                self.first_question,
                self.second_question,
                self.third_question,
                self.fourth_question,
            ]
            random.shuffle(question_funcs)
            for round_number in range(n_round):
                cprint(
                    "*----------------------------------------------------------------------------------------------------*",
                    attrs=["bold"],
                )
                cprint(f"Round {round_number + 1}", attrs=["bold"])
                question_func = question_funcs[round_number % len(question_funcs)]
                question, correct_answer = question_func()
                choices = self.gen_answers(correct_answer)
                chosen_answer, correct_answer = self.ask_question(
                    question, correct_answer, choices
                )
                self.score = self.score_fun(chosen_answer, correct_answer, dif)
            end_time = time.time()
            time_involved = end_time - start_time
            cprint(
                "*----------------------------------------------------------------------------------------------------*",
                attrs=["bold"],
            )
            print(f"⌛ It took you {time_involved:.2f} seconds to solve the quiz")
            if self.score / n_round > 0.6 and time_involved / n_round < 10:
                print(
                    f"🥇 Good job! Your final score is {self.score}/{n_round} and you were preatty fast!"
                )
            elif self.score / n_round > 0.6 and time_involved / n_round > 10:
                print(
                    f"🥈 Good job! Your final score is {self.score}/{n_round}. Try again to complete the quiz faster!"
                )
            else:
                print(
                    f"🥉 You can do better! your final score is {self.score}/{n_round}"
                )
            play_again = str(
                input(
                    "🔸 Thank you for playing, would you like to play again ? Enter 'yes' or 'no': "
                )
            )
            if play_again == "no":
                cprint(
                    "👋 You are exiting the game, thank you for playing!",
                    attrs=["bold"],
                )
                break
            if play_again == "yes":
                self.score = 0
                self.dataset = pd.read_csv("./game_set.csv")
                cprint(
                    "*----------------------------------------------------------------------------------------------------*",
                    attrs=["bold"],
                )
            else:
                cprint(
                    "👋 You are exiting the game, thank you for playing!",
                    attrs=["bold"],
                )
                break
