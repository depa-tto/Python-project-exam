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
    def __init__(self, data_set):
        self.data_set = data_set
        self.score = 0
        self.difficulty_level = None
        self.num_rounds = 0
        self.letters = ['A', 'B', 'C', 'D']

    def difficulty(self):
        while True:
            dif = input("Choose the difficulty (easy, medium, hard): ").strip().lower()
            
            if dif not in ['hard', 'medium', 'easy']:
                print("Please insert a proper difficulty: 'hard', 'medium', or 'easy'.")
            else: 
                self.difficulty_level = dif
                if dif == 'hard':
                    self.data_set = self.data_set[(self.data_set['start_year'] <= 1966) & (~self.data_set['region'].isin(['US', 'CA']))]
                    print('Rules: +1 if correct, -1 if incorrect.')
                elif dif == 'medium':
                    self.data_set = self.data_set[(self.data_set['start_year'].between(1967, 1987)) & (self.data_set['region'].isin(['US', 'CA']))]
                    print('Rules: +1 if correct, -0.5 if incorrect.')
                elif dif == 'easy':
                    self.data_set = self.data_set[(self.data_set['start_year'] >= 1988) & 
                                                   (self.data_set['region'].isin(['US', 'CA'])) & 
                                                   (self.data_set['first_profession'].isin(['actor', 'actress', 'writer', 'producer', 'director'])) & 
                                                   (~self.data_set['genre_1'].isin(['Documentary', 'Talk-Show', 'Game-Show', 'Sci-Fi', 'News', 'History', 'Reality-TV', 'Short', 'Adult']))]
                    print('Rules: +1 if correct, 0 otherwise.')
                
                return

    def set_rounds(self):
        while True:
            try: 
                self.num_rounds = int(input('How many rounds do you want to play? '))
                if self.num_rounds > 0:
                    return
                else:
                    print('Please enter a positive number of rounds.')
            except ValueError:
                print('Please enter a positive number of rounds.')

    def generate_question(self, question_type):
        self.data_set = self.data_set.reset_index(drop=True)
        indices = random.choice(self.data_set.index) 
        title = self.data_set['title'].iloc[indices]
        region = self.data_set['region'].iloc[indices]
        name_surname = self.data_set['name_surname'].iloc[indices]
        role = self.data_set['first_profession'].iloc[indices]
        
        if question_type == 'year':
            correct_answer = self.data_set['start_year'].iloc[indices]
            question = f"In which year was '{title}' made in {region} by {name_surname} as a {role}?"
        elif question_type == 'genre':
            correct_answer = self.data_set['genre_1'].iloc[indices]
            question = f"What genre is '{title}' made in {region} by {name_surname} as a {role}?"
        elif question_type == 'title':
            correct_answer = self.data_set['title'].iloc[indices]
            question = f"What was the title of the movie made in {region} with {name_surname} as a {role}?"
        else:  # 'who'
            correct_answer = self.data_set['name_surname'].iloc[indices]
            question = f"Who was the {role} of the movie named '{title}'?"

        return question, correct_answer

    def score_fun(self, my_answer, correct_answer):
        if my_answer == correct_answer:
            self.score += 1
            print(f'Your answer: {my_answer}, Correct answer: {correct_answer}')
        else:
            print(f'Your answer: {my_answer}, Correct answer: {correct_answer}')
            if self.difficulty_level == 'hard':
                self.score -= 1
            elif self.difficulty_level == 'medium':
                self.score -= 0.5
            self.score = max(0, self.score)
        
        print(f'Your current score: {self.score}')

    def gen_answers(self, correct_answer, merge_set):
        incorrect_ans = []
        if correct_answer in merge_set['start_year'].values:
            incorrect_ans = [correct_answer - random.choice([2, 4, 6, 8]), 
                             correct_answer - random.choice([1, 3, 5, 7, 9]), 
                             correct_answer - random.choice([10, 15, 20, 25, 30])]
        else:
            incorrect_ans = random.sample(list(merge_set[merge_set.columns[0]].unique()), 3)
            if correct_answer in incorrect_ans:
                incorrect_ans.remove(correct_answer)

        options = [correct_answer] + incorrect_ans
        random.shuffle(options)
        return options

    def ask_question(self, question, correct_answer, choices):
        print(question)
        for j, choice in zip(self.letters, choices):
            print(f"{j}. {choice}")

        while True:  
            my_answer = input('Enter your answer (A, B, C, or D): ').upper()  
            if my_answer in self.letters:  
                break
            print("Invalid input. Please enter A, B, C, or D.")

        chosen_index = self.letters.index(my_answer)
        chosen_answer = choices[chosen_index]

        return chosen_answer, correct_answer  

    def play_quiz(self):
        print('Welcome! Please enter the difficulty and the number of rounds you want to play.')
        self.difficulty()
        self.set_rounds()
        print(f'You are going to play for {self.num_rounds} rounds at {self.difficulty_level} level.')
        start_time = time.time()
        question_types = ['year', 'genre', 'title', 'who']

        for round_number in range(self.num_rounds):
            print('-------------------------------------------')
            print(f'Round {round_number + 1}')
            
            question_type = question_types[round_number % len(question_types)]
            question, correct_answer = self.generate_question(question_type)
            choices = self.gen_answers(correct_answer, self.data_set)
            chosen_answer, correct_answer = self.ask_question(question, correct_answer, choices)
            self.score_fun(chosen_answer, correct_answer)

        end_time = time.time()
        time_involved = end_time - start_time
        print('-------------------------------------------')
        print(f"It took you {time_involved:.2f} seconds to solve the quiz.")
        
        if self.score / self.num_rounds > 0.6:
            print(f'Good job! Your final score is {self.score}/{self.num_rounds}') 
        else:
            print(f'You can do better! Your final score is {self.score}/{self.num_rounds}')

        play_again = input("Thank you for playing! Would you like to play again? (yes/no): ").strip().lower()
        if play_again == 'yes':
            self.score = 0
            self.play_quiz()
        else:
            print('Exiting the game.')

