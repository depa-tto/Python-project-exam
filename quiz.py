"""
quiz.py

This module contains the logic for a quiz application.
It includes functions to ask questions, validate answers,
calculate scores, and display results to the user.
"""
import time # type: ignore
import random # type: ignore
import pandas as pd  # type: ignore
class QuizGame:
    """A class to represent a quiz game.

    This class handles the mechanics of a quiz game, including
    questions, answers, and scoring. It provides methods to start
    the game, present questions to the player, and calculate the
    final score.

    Attributes:
        dataset (pd.DataFrame): The dataset containing quiz information.
        score (int): The player's score throughout the game.
        difficulty_level (str): The difficulty level chosen by the player.
    """

    def __init__(self, dataset):
        """Initialize the QuizGame with a dataset.

        Args:
            dataset (pd.DataFrame): A pandas DataFrame containing the quiz data.
        """
        self.dataset = dataset
        self.score = 0
        self.difficulty_level = None

    def difficulty(self):
        """Set the difficulty level of the quiz.

        This method allows the player to choose a difficulty level and adjusts
        the dataset accordingly.

        Returns:
            tuple: A tuple containing the filtered dataset and the chosen difficulty level.
        """
        while True:
            dif = input('Choose the difficulty between easy, medium, and hard: ').strip().lower()
            
            if dif not in ['hard', 'medium', 'easy']:
                print("Please insert a proper difficulty between: 'hard', 'medium', 'easy'")
            else:
                if dif == 'hard':
                    self.dataset = self.dataset[(self.dataset['start_year'] <= 1966) & (~self.dataset['region'].isin(['US', 'CA']))]
                    print('Rules: +1 if correct, -1 if incorrect.')
                elif dif == 'medium':
                    self.dataset = self.dataset[(self.dataset['start_year'] >= 1967) & 
                                                (self.dataset['start_year'] <= 1987) & 
                                                (self.dataset['region'].isin(['US', 'CA']))]
                    print('Rules: +1 if correct, -0.5 if incorrect.')
                elif dif == 'easy':
                    self.dataset = self.dataset[(self.dataset['start_year'] >= 1988) & 
                                                (self.dataset['region'].isin(['US', 'CA'])) & 
                                                (self.dataset['first_profession'].isin(['actor', 'actress', 'writer', 'producer', 'director'])) &
                                                (~self.dataset['genre_1'].isin(['Documentary', 'Talk-Show', 'Game-Show', 
                                                                                  'Sci-Fi', 'News', 'History', 
                                                                                  'Reality-TV', 'Short', 'Adult']))]
                    print('Rules: +1 if correct, 0 otherwise.')
                
                self.difficulty_level = dif
                return self.dataset, dif

    def first_question(self):
        """Generate the first question for the quiz.

        Returns:
            tuple: A tuple containing the question and the correct answer.
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index) 
        title = self.dataset['title'].iloc[indices]
        region = self.dataset['region'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]
        
        correct_answer = self.dataset['start_year'].iloc[indices]
        question = f"In which year was '{title}' made in {region} of {name_surname} as a {role} produced?"
        
        return question, correct_answer

    def second_question(self):
        """Generate the second question for the quiz.

        Returns:
            tuple: A tuple containing the question and the correct answer.
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index) 
        title = self.dataset['title'].iloc[indices]
        region = self.dataset['region'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]
        
        correct_answer = self.dataset['genre_1'].iloc[indices]
        question = f"What genre is '{title}' made in {region} of {name_surname} as a {role}?"
        
        return question, correct_answer   

    def third_question(self):
        """Generate the third question for the quiz.

        Returns:
            tuple: A tuple containing the question and the correct answer.
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index) 
        movie_type = self.dataset['type'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]
        region = self.dataset['region'].iloc[indices]
        
        correct_answer = self.dataset['title'].iloc[indices]
        question = f"What was the title of the {movie_type} made in {region} with {name_surname} as a {role}?"
        
        return question, correct_answer

    def fourth_question(self):
        """Generate the fourth question for the quiz.

        Returns:
            tuple: A tuple containing the question and the correct answer.
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index) 
        movie_type = self.dataset['type'].iloc[indices]
        title = self.dataset['title'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]
        
        correct_answer = self.dataset['name_surname'].iloc[indices]
        question = f"Who was the {role} of the {movie_type} named '{title}'?"
        
        return question, correct_answer  

    def score_fun(self, my_answer, correct_answer):
        """Evaluate the player's answer and update the score.

        Args:
            my_answer (str): The player's answer.
            correct_answer (str): The correct answer.

        Returns:
            int: The updated score.
        """
        if my_answer == correct_answer:
            self.score += 1
            print(f'Your answer was {my_answer} and the correct one is {correct_answer}.')
        else:
            print(f'Your answer was {my_answer} but the correct one is {correct_answer}.')
            if self.difficulty_level == 'hard':
                self.score -= 1
            elif self.difficulty_level == 'medium':
                self.score -= 0.5

            if self.score < 0:
                self.score = 0

        print(f'Your current score is: {self.score}')
        return self.score

    def gen_answers(self, correct_answer):
        """Generate multiple-choice answers including the correct answer.

        Args:
            correct_answer (str/int): The correct answer to the question.

        Returns:
            list: A shuffled list of answer choices.
        """
        options = []  
        
        if correct_answer in self.dataset['start_year'].values:
            incorrect_ans = [correct_answer - random.choice([2, 4, 6, 8]), 
                            correct_answer - random.choice([1, 3, 5, 7, 9]), 
                            correct_answer - random.choice([10, 15, 20, 25, 30])]
            options = [correct_answer] + incorrect_ans
        elif correct_answer in self.dataset['genre_1'].values:
            incorrect_ans = random.sample(list(self.dataset['genre_1'].unique()), 3)
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(list(self.dataset['genre_1'].unique()), 3)
            options = [correct_answer] + incorrect_ans
        elif correct_answer in self.dataset['title'].values:
            incorrect_ans = random.sample(list(self.dataset['title'].unique()), 3)
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(list(self.dataset['title'].unique()), 3)
            options = [correct_answer] + incorrect_ans
        elif correct_answer in self.dataset['name_surname'].values:
            incorrect_ans = random.sample(list(self.dataset['name_surname'].unique()), 3)
            if correct_answer in incorrect_ans:
                while correct_answer in incorrect_ans:
                    incorrect_ans = random.sample(list(self.dataset['name_surname'].unique()), 3)
            options = [correct_answer] + incorrect_ans
        if not options:  
            options = [correct_answer]  

        random.shuffle(options)
        return options


    def ask_question(self, question, correct_answer, choices):
        """Display the question and answer choices to the player.

        Args:
            question (str): The question to be asked.
            correct_answer (str/int): The correct answer.
            choices (list): A list of possible answers.

        Returns:
            tuple: The chosen answer and the correct answer.
        """
        letters = ['A', 'B', 'C', 'D']
        print(question)
        for j, choice in zip(letters, choices):
            print(f"{j}. {choice}")

        while True:  
            my_answer = input('Enter your answer (A, B, C, or D): ').upper()  
            if my_answer in letters:  
                break
            print("Invalid input. Please enter A, B, C, or D.")

        chosen_index = letters.index(my_answer)
        chosen_answer = choices[chosen_index]

        return chosen_answer, correct_answer

    def quiz(self):
        """Start the quiz game, asking a set number of questions based on difficulty.

        This method manages the game loop, including difficulty selection,
        question generation, answer checking, and final scoring.
        """
        print('Welcome! Please enter the difficulty and how many rounds do you want to play')
        while True:
            self.dataset, self.difficulty_level = self.difficulty()
            x = int(input('How many rounds do you want to play? '))
            if x > 0:
                print(f'You are going to play for {x} rounds at {self.difficulty_level} level')
                start_time = time.time()
                question_funcs = [self.first_question, self.second_question, self.third_question, self.fourth_question]

                for round_number in range(x):
                    print('-------------------------------------------')
                    print(f'Round {round_number + 1}')
                    
                    question_func = question_funcs[round_number % len(question_funcs)]
                    question, correct_answer = question_func()
                    choices = self.gen_answers(correct_answer)
                    chosen_answer, correct_answer = self.ask_question(question, correct_answer, choices)
                    self.score = self.score_fun(chosen_answer, correct_answer)
                
                end_time = time.time()
                time_involved = end_time - start_time
                print('-------------------------------------------')
                print(f"It took you {time_involved:.2f} seconds to solve the quiz.")
                
                if self.score / x > 0.6:
                    print(f'Good job! Your final score is {self.score}/{x}') 
                else:
                    print(f'You can do better! Your final score is {self.score}/{x}')
                
                play_again = input("Thank you for playing, would you like to play again? Enter 'yes' or 'no': ").strip().lower()
                if play_again == 'no':
                    print('You are exiting the game. Thank you for playing!')
                    break
                elif play_again == 'yes':
                    self.score = 0
                    self.dataset = pd.read_csv('./merge_set.csv')
                    print('-------------------------------------------')
                else:
                    print('You are exiting the game. Thank you for playing!')
                    break

            else:
                print("Please enter a positive number of rounds.")