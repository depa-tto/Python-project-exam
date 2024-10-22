"""
quiz.py

This module contains the logic for a quiz application.
It includes functions to ask questions, validate answers,
calculate scores, and display results to the user.
"""
import time # type: ignore
import random # type: ignore
import pandas as pd # type: ignore

class QuizGame:
    def __init__(self, dataset):
        self.dataset = dataset
        self.score = 0
        self.difficulty_level = None

    def choose_difficulty(self):
        while True:
            dif = input('Choose the difficulty between easy, medium, and hard: ').strip().lower()

            if dif not in ['hard', 'medium', 'easy']:
                print("Please insert a proper difficulty: 'hard', 'medium', or 'easy'")
            else:
                self.difficulty_level = dif
                if dif == 'hard':
                    self.dataset = self.dataset[(self.dataset['start_year'] <= 1966) & (~self.dataset['region'].isin(['US', 'CA']))]
                    print('Rules: +1 if you are correct, -1 if incorrect.')
                elif dif == 'medium':
                    self.dataset = self.dataset[(self.dataset['start_year'] >= 1967) & (self.dataset['start_year'] <= 1987) & (self.dataset['region'].isin(['US', 'CA']))]
                    print('Rules: +1 if you are correct, -0.5 if incorrect.')
                elif dif == 'easy':
                    self.dataset = self.dataset[
                        (self.dataset['start_year'] >= 1988) & 
                        (self.dataset['region'].isin(['US', 'CA'])) & 
                        (self.dataset['first_profession'].isin(['actor', 'actress', 'writer', 'producer', 'director'])) &
                        (~self.dataset['genre_1'].isin(['Documentary', 'Talk-Show', 'Game-Show', 'Sci-Fi', 'News', 'History', 'Reality-TV', 'Short', 'Adult']))
                    ]
                    print('Rules: +1 if you are correct, 0 otherwise.')
                return

    def first_question(self):
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        title = self.dataset['title'].iloc[indices]
        region = self.dataset['region'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]

        correct_answer = self.dataset['start_year'].iloc[indices]
        question = f"In which year was '{title}' made in {region} by {name_surname} as a {role}?"
        
        return question, correct_answer

    def second_question(self):
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        title = self.dataset['title'].iloc[indices]
        region = self.dataset['region'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]

        correct_answer = self.dataset['genre_1'].iloc[indices]
        question = f"What genre is '{title}' made in {region} by {name_surname} as a {role}?"
        
        return question, correct_answer

    def third_question(self):
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
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        movie_type = self.dataset['type'].iloc[indices]
        title = self.dataset['title'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]

        correct_answer = self.dataset['name_surname'].iloc[indices]
        question = f"Who was the {role} of the {movie_type} named '{title}'?"

        return question, correct_answer

    def score_question(self, my_answer, correct_answer):
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

    def gen_answers(self, correct_answer):
        if correct_answer in self.dataset['start_year'].values:
            incorrect_ans = [correct_answer - random.choice([2, 4, 6, 8]),
                             correct_answer - random.choice([1, 3, 5, 7, 9]),
                             correct_answer - random.choice([10, 15, 20, 25, 30])]
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options
        elif correct_answer in self.dataset['genre_1'].values:
            incorrect_ans = random.sample(list(self.dataset['genre_1'].unique()), 3)
            while correct_answer in incorrect_ans:
                incorrect_ans = random.sample(list(self.dataset['genre_1'].unique()), 3)

            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options
        elif correct_answer in self.dataset['title'].values:
            incorrect_ans = random.sample(list(self.dataset['title'].unique()), 3)
            while correct_answer in incorrect_ans:
                incorrect_ans = random.sample(list(self.dataset['title'].unique()), 3)

            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options
        elif correct_answer in self.dataset['name_surname'].values:
            incorrect_ans = random.sample(list(self.dataset['name_surname'].unique()), 3)
            while correct_answer in incorrect_ans:
                incorrect_ans = random.sample(list(self.dataset['name_surname'].unique()), 3)

            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options

    def ask_question(self, question, correct_answer, choices):
        print(question)
        letters = ['A', 'B', 'C', 'D']
        for j, choice in zip(letters, choices):
            print(f"{j}. {choice}")

        while True:  
            my_answer = input('Enter your answer (A, B, C, or D): ').upper()  
            if my_answer in letters:  
                chosen_index = letters.index(my_answer)
                chosen_answer = choices[chosen_index]
                return chosen_answer, correct_answer  
            print("Invalid input. Please enter A, B, C, or D.")

    def rounds(self):
        while True:
            try: 
                n_round = int(input('How many rounds do you want to play? '))
                if n_round > 0:
                    return n_round
                else:
                    print('Please enter a positive number of rounds.')
            except ValueError:
                print('Please enter a positive number of rounds.')

    def play(self):
        print('Welcome! Please enter the difficulty and how many rounds you want to play.')
        while True:
            self.choose_difficulty()
            n_round = self.rounds()
            print(f'You are going to play for {n_round} rounds at {self.difficulty_level} level.')
            start_time = time.time()

            question_funcs = [self.first_question, self.second_question, self.third_question, self.fourth_question]

            for round_number in range(n_round):
                print('-------------------------------------------')
                print(f'Round {round_number + 1}')
                
                question_func = question_funcs[round_number % len(question_funcs)]
                question, correct_answer = question_func()
                choices = self.gen_answers(correct_answer)
                chosen_answer, correct_answer = self.ask_question(question, correct_answer, choices)
                self.score_question(chosen_answer, correct_answer)

            end_time = time.time()
            time_involved = end_time - start_time
            print('-------------------------------------------')
            print(f"It took you {time_involved:.2f} seconds to solve the quiz.")
            if self.score / n_round > 0.6:
                print(f'Good job! Your final score is {self.score}/{n_round}.') 
            else:
                print(f'You can do better! Your final score is {self.score}/{n_round}.')
            
            play_again = input("Thank you for playing! Would you like to play again? Enter 'yes' or 'no': ").strip().lower()
            if play_again == 'no':
                break
            elif play_again == 'yes':
                self.score = 0
                self.dataset = pd.read_csv('./merge_set.csv')
                print('-------------------------------------------')
            else:
                print('You are exiting the game.')
                break