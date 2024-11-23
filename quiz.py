"""
quiz.py

This module contains the logic for a quiz application.
It includes functions to ask questions, validate answers, calculate scores, 
and display results to the user.
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
        self.dataset = dataset  # store the dataset as a class attribute
        self.score = 0  # initialize the score to 0

    def difficulty(self):
        """
        Prompts the user to choose a difficulty level and filters the dataset accordingly.

        The user selects between easy, medium, and hard difficulty.
        The dataset is then filtered based on the selected difficulty level.

        Returns:
            The filtered dataset and the chosen difficulty level.
        """
        while True:
            # ask the user to input a difficulty level (easy, medium, hard)
            dif = (
                str(
                    input(
                        "🔸 Please choose the difficulty between easy, medium and hard: "
                    )
                )
                .strip()
                .lower()
            )
            # ensure a valid difficulty level is entered
            if dif not in ["hard", "medium", "easy"]:  # validate the input
                print("🔸 Please insert a proper difficulty ")
            else:
                # filter the dataset based on the chosen difficulty level
                if dif == "hard":
                    # filter for older movies(older than 1974)
                    self.dataset = self.dataset[(self.dataset["start_year"] <= 1974)]
                    print("🔸 Rules: +1 if you are correct, -1 otherwise")
                elif dif == "medium":
                    # filter for medium difficulty movies(1975-2004) and most popular professions
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
                    # filter for recent movies(2005 and later) and most popular professions and genres
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
                return self.dataset, dif  # return filtered dataset and difficulty

    def first_question(self):
        """
        Generates the first question based on a random entry from the dataset.

        This question asks about the year of production of a movie.

        Returns:
            The question string and the correct answer (production year).
        """
        self.dataset = self.dataset.reset_index(
            drop=True
        )  # reset the index of the dataset
        indices = random.choice(self.dataset.index)  # select a random row
        title = self.dataset["title"].iloc[indices]
        name_surname = self.dataset["name_surname"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        movie_type = self.dataset["type"].iloc[indices]
        correct_answer = self.dataset["start_year"].iloc[
            indices
        ]  # correct answer: production year
        question = f"In which year was the {movie_type} '{title}' of {name_surname} as a {role} component produced ?"
        return (
            question,
            correct_answer,
        )  # return the generated question and the correct answer

    def second_question(self):
        """
        Generates the second question based on a random entry from the dataset.

        This question asks about the genre of a movie.

        Returns:
            The question string and the correct answer (genre).
        """
        self.dataset = self.dataset.reset_index(
            drop=True
        )  # reset the index of the dataset
        indices = random.choice(self.dataset.index)  # select a random row
        title = self.dataset["title"].iloc[indices]
        name_surname = self.dataset["name_surname"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        movie_type = self.dataset["type"].iloc[indices]
        year = self.dataset["start_year"].iloc[indices]
        correct_answer = self.dataset["genre_1"].iloc[indices]  # correct answer: genre
        question = f"What genre is the {movie_type} '{title}' made in {year} of {name_surname} as a {role} component ?"
        return (
            question,
            correct_answer,
        )  # return the generated question and the correct answer

    def third_question(self):
        """
        Generates the third question based on a random entry from the dataset.

        This question asks about the title of a movie.

        Returns:
            The question string and the correct answer (movie title).
        """
        self.dataset = self.dataset.reset_index(
            drop=True
        )  # reset the index of the dataset
        indices = random.choice(self.dataset.index)  # select a random row
        movie_type = self.dataset["type"].iloc[indices]
        name_surname = self.dataset["name_surname"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        year = self.dataset["start_year"].iloc[indices]
        correct_answer = self.dataset["title"].iloc[indices]  # correct answer: title
        question = f"What was the title of the {movie_type} made in {year} with {name_surname} as a {role} component ?"
        return (
            question,
            correct_answer,
        )  # return the generated question and the correct answer

    def fourth_question(self):
        """
        Generates the fourth question based on a random entry from the dataset.

        This question asks about the name of the person involved in a movie.

        Returns:
            The question string and the correct answer (person's name).
        """
        self.dataset = self.dataset.reset_index(
            drop=True
        )  # reset the index of the dataset
        indices = random.choice(self.dataset.index)  # select a random row
        movie_type = self.dataset["type"].iloc[indices]
        title = self.dataset["title"].iloc[indices]
        role = self.dataset["first_profession"].iloc[indices]
        year = self.dataset["start_year"].iloc[indices]
        correct_answer = self.dataset["name_surname"].iloc[
            indices
        ]  # correct answer: name of the person
        question = (
            f"Who was the {role} of the {movie_type} named '{title}' made in {year} ?"
        )
        return (
            question,
            correct_answer,
        )  # return the generated question and the correct answer

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
        # if the answer is correct
        if my_answer == correct_answer:
            self.score += 1  # increase the score by 1
            cprint(
                f"✅ You are correct, '{correct_answer}' is the right answer", "green"
            )
            print(f"Your current score is: {self.score}")
        else:
            cprint(
                f"❌ Your answer was '{my_answer}' but the correct one is '{correct_answer}'",
                "red",
            )
            # apply penalty based on difficulty level
            if dif == "hard":
                self.score -= 1  # penalize by 1 for incorrect answer on hard
            elif dif == "medium":
                self.score -= 0.5  # penalize by 0.5 for incorrect answer on medium

            if self.score < 0:
                self.score = 0  # ensure score doesn't go below 0
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
            # if the correct answer is a year, generate incorrect answers by slightly modifying the correct year
            incorrect_ans = [
                # adding random noise for incorrect answers(subtract or add small values)
                correct_answer - random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]),
                correct_answer + random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]),
                correct_answer - random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50]),
            ]
            adjusted_incorrect_ans = []
            for i in incorrect_ans:
                # ensuring that the option years do not exceed the current year
                while i >= time.localtime().tm_year:
                    i -= 1
                adjusted_incorrect_ans.append(i)
            options = [correct_answer] + adjusted_incorrect_ans
            random.shuffle(options)  # shuffle the choices to randomize thei order
            return options

        # if the correct answer is a genre, generate incorrect answers from other genres
        if correct_answer in self.dataset["genre_1"].values:
            incorrect_ans = random.sample(list(self.dataset["genre_1"].unique()), 3)
            # ensure the correct answer is not among the incorrect answers
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(
                        list(self.dataset["genre_1"].unique()), 3
                    )
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)  # shuffle the choices to randomize thei order
            return options

        # if the correct answer is a title, generate incorrect answers from other titles
        if correct_answer in self.dataset["title"].values:
            incorrect_ans = random.sample(list(self.dataset["title"].unique()), 3)
            # ensure the correct answer is not among the incorrect answers
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(
                        list(self.dataset["title"].unique()), 3
                    )
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)  # shuffle the choices to randomize thei order
            return options

        # if the correct answer is the name and surname, generate incorrect answers from other names and surnames
        if correct_answer in self.dataset["name_surname"].values:
            incorrect_ans = random.sample(
                list(self.dataset["name_surname"].unique()), 3
            )
            # ensure the correct answer is not among the incorrect answers
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(
                        list(self.dataset["name_surname"].unique()), 3
                    )
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)  # shuffle the choices to randomize thei order
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
        # display each choice with a corresponding letter (A, B, C, D)
        for j, choice in zip(letters, choices):
            print(f"{j}. {choice}")
        while True:
            # get user input, ensure they enter a valid option(A, B, C, or D)
            my_answer = input("Enter your answer (A, B, C, or D): ").upper()
            if my_answer in letters:
                break  # valid answer entered, exit the loop
            else:
                print("Invalid input. Please enter A, B, C, or D.")

        # find the index of the selected answer
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
                    return n_round  # return the valid number of rounds
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
        self.score = 0  # initialize score
        while True:
            # select difficulty and prepare dataset
            self.dataset, dif = self.difficulty()
            # get the number of rounds the user wants to play
            n_round = self.rounds()
            cprint(
                f"👉 You are going to play for {n_round} rounds at {dif} level",
                attrs=["bold"],
            )
            start_time = time.time()  # record start time for the quiz

            # shuffle question functions to randomize the types of questions asked
            question_funcs = [
                self.first_question,
                self.second_question,
                self.third_question,
                self.fourth_question,
            ]
            random.shuffle(question_funcs)

            # iterate over the number of rounds and ask questions
            for round_number in range(n_round):
                cprint(
                    "*----------------------------------------------------------------------------------------------------*",
                    attrs=["bold"],
                )
                cprint(f"Round {round_number + 1}", attrs=["bold"])
                question_func = question_funcs[round_number % len(question_funcs)]
                question, correct_answer = (
                    question_func()
                )  # get question and correct answer
                choices = self.gen_answers(correct_answer)  # generate answer choices
                chosen_answer, correct_answer = self.ask_question(
                    question, correct_answer, choices
                )  # ask the user for an answer
                self.score = self.score_fun(
                    chosen_answer, correct_answer, dif
                )  # update score
            end_time = time.time()  # Rrcord end time for the quiz
            time_involved = end_time - start_time  # calculate time spent
            cprint(
                "*----------------------------------------------------------------------------------------------------*",
                attrs=["bold"],
            )
            print(f"⌛ It took you {time_involved:.2f} seconds to solve the quiz")
            # provide feedback based on performance
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
                    f"🥉 You can do better! Your final score is {self.score}/{n_round}"
                )
            # ask the user if they want to play again
            play_again = str(
                input(
                    "🔸 Thank you for playing, would you like to play again ? Enter 'yes' or 'no': "
                )
                .strip()
                .lower()
            )
            if play_again == "no":
                cprint(
                    "👋 You are exiting the game, bye!",
                    attrs=["bold"],
                )
                break
            if play_again == "yes":
                self.score = 0  # reset score
                self.dataset = pd.read_csv("./game_set.csv")  # reload dataset
                cprint(
                    "*----------------------------------------------------------------------------------------------------*",
                    attrs=["bold"],
                )
            else:
                cprint(
                    "👋 You are exiting the game, bye!",
                    attrs=["bold"],
                )
                break
