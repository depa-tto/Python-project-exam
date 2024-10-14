import random

class Quizgame:
    """
    A class to represent a quiz game based on a dataset.

    This class allows users to play a quiz with questions related to titles, 
    genres, and professions, filtered by different difficulty levels (easy, 
    medium, hard). It generates multiple-choice questions and keeps track of the score.
    
    Attributes:
    ----------
    dataset : pandas.DataFrame
        A dataset containing titles, years, regions, and professions to create quiz questions.
    score : int
        The player's current score in the game.

    Methods:
    -------
    difficulty():
        Filters the dataset based on the selected difficulty level.
    first_question():
        Generates a question about the year a title was produced.
    second_question():
        Generates a question about the genre of a title.
    third_question():
        Generates a question about the title of a production.
    score_fun(my_answer, correct_answer):
        Updates the score based on whether the player's answer was correct.
    gen_answers(correct_answer, merge_set):
        Generates multiple-choice options, including the correct answer and three incorrect ones.
    ask_question(question, correct_answer, choices):
        Asks the player the question and returns their chosen answer.
    quiz(merge_set):
        Runs the quiz for the number of rounds the player selects.
    """

    def __init__(self, dataset):
        """
        Initializes the QuizGame class with a dataset and sets the initial score to 0.
        
        Parameters:
        ----------
        dataset : pandas.DataFrame
            The dataset containing the data to generate quiz questions.
        """
        self.dataset = dataset
        self.score = 0

    def difficulty(self):
        """
        Prompts the user to select a difficulty level and filters the dataset accordingly.
        
        Difficulty levels:
        - 'easy': Titles made after 1981 in the US.
        - 'medium': Titles made between 1961 and 1980 in the US.
        - 'hard': Titles made before 1960 and not in the US.
        """
        dif = str(input('Choose the difficulty (easy, medium, or hard): ')).lower()
        if dif == 'hard':
            self.dataset = self.dataset[(self.dataset['start_year'] < 1960) & (self.dataset['region'] != 'US')] 
        elif dif == 'medium':
            self.dataset = self.dataset[(self.dataset['start_year'] > 1961) & (self.dataset['start_year'] < 1980) & (self.dataset['region'] == 'US')]
        elif dif == 'easy':
            self.dataset = self.dataset[(self.dataset['start_year'] > 1981) & (self.dataset['region'] == 'US')]

    def first_question(self):
        """
        Generates a multiple-choice question asking the player to guess the year a title was produced.

        Returns:
        -------
        tuple:
            - question (str): The question to be asked.
            - correct_answer (int): The correct answer (year).
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        title = self.dataset['title'].iloc[indices]
        region = self.dataset['region'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]

        correct_answer = self.dataset['start_year'].iloc[indices]
        question = f"In which year was '{title}' made in {region} of '{name_surname}' as a {role} produced?"
        
        return question, correct_answer

    def second_question(self):
        """
        Generates a multiple-choice question asking the player to guess the genre of a title.

        Returns:
        -------
        tuple:
            - question (str): The question to be asked.
            - correct_answer (str): The correct answer (genre).
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        title = self.dataset['title'].iloc[indices]
        region = self.dataset['region'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]

        correct_answer = self.dataset['genre_1'].iloc[indices]
        question = f"What genre is '{title}' made in {region} of '{name_surname}' as a {role}?"

        return question, correct_answer

    def third_question(self):
        """
        Generates a multiple-choice question asking the player to guess the title of a production.

        Returns:
        -------
        tuple:
            - question (str): The question to be asked.
            - correct_answer (str): The correct answer (title).
        """
        self.dataset = self.dataset.reset_index(drop=True)
        indices = random.choice(self.dataset.index)
        movie_type = self.dataset['type'].iloc[indices]
        name_surname = self.dataset['name_surname'].iloc[indices]
        role = self.dataset['first_profession'].iloc[indices]

        correct_answer = self.dataset['title'].iloc[indices]
        question = f"What was the title of the {movie_type} with '{name_surname}' as a {role}?"
        
        return question, correct_answer

    def score_fun(self, my_answer, correct_answer):
        """
        Updates the score based on whether the player's answer was correct.
        
        Parameters:
        ----------
        my_answer : str or int
            The player's selected answer.
        correct_answer : str or int
            The correct answer for the question.
        """
        print(f'Your answer was: {my_answer}')
        print(f'The correct answer is: {correct_answer}')
        if my_answer == correct_answer:
            self.score += 1
            print(f'Your score is: {self.score}')
        else:
            print(f'Your score is: {self.score}')

    def gen_answers(self, correct_answer, merge_set):
        """
        Generates multiple-choice options for the current question, including the correct answer.

        Parameters:
        ----------
        correct_answer : str or int
            The correct answer for the question.
        merge_set : pandas.DataFrame
            A dataset used to generate incorrect answer options.

        Returns:
        -------
        list:
            A list of shuffled multiple-choice options (including correct and incorrect answers).
        """
        if correct_answer in merge_set['start_year'].values:
            incorrect_ans = [correct_answer - random.choice([2, 4, 6, 8]),
                             correct_answer - random.choice([1, 3, 5, 7, 9]),
                             correct_answer - random.choice([10, 15, 20, 25, 30])]
            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options
        elif correct_answer in merge_set['genre_1'].values:
            incorrect_ans = random.sample(list(merge_set['genre_1'].unique()), 3)
            while correct_answer in incorrect_ans:
                incorrect_ans = random.sample(list(merge_set['genre_1'].unique()), 3)

            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options
        elif correct_answer in merge_set['title'].values:
            incorrect_ans = random.sample(list(merge_set['title'].unique()), 3)
            while correct_answer in incorrect_ans:
                incorrect_ans = random.sample(list(merge_set['title'].unique()), 3)

            options = [correct_answer] + incorrect_ans
            random.shuffle(options)
            return options

    def ask_question(self, question, correct_answer, choices):
        """
        Displays the question and multiple-choice options to the player and asks for their input.

        Parameters:
        ----------
        question : str
            The question to be asked.
        correct_answer : str or int
            The correct answer for the question.
        choices : list
            The list of multiple-choice options for the player to select from.

        Returns:
        -------
        tuple:
            - chosen_answer (str or int): The player's selected answer.
            - correct_answer (str or int): The correct answer for the question.
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

    def quiz(self, merge_set):
        """
        Runs the quiz game for a user-specified number of rounds, updating the score after each question.

        Parameters:
        ----------
        merge_set : pandas.DataFrame
            A dataset used to generate multiple-choice answer options.
        """
        self.difficulty()
        counter = 0
        x = int(input('How many rounds do you want to play? '))
        while counter < x:

            question, correct_answer = self.first_question()
            choices = self.gen_answers(correct_answer, merge_set)
            chosen_answer, correct_answer = self.ask_question(question, correct_answer, choices)
            self.score_fun(chosen_answer, correct_answer)

            counter += 1
            print('-------------------------------------------')

            question, correct_answer = self.second_question()
            choices = self.gen_answers(correct_answer, merge_set)
            chosen_answer, correct_answer = self.ask_question(question, correct_answer, choices)
            self.score_fun(chosen_answer, correct_answer)

            counter += 1
            print('-------------------------------------------')

            question, correct_answer = self.third_question()
            choices = self.gen_answers(correct_answer, merge_set)
            chosen_answer, correct_answer = self.ask_question(question, correct_answer, choices)
            self.score_fun(chosen_answer, correct_answer)

            counter += 1
            print('-------------------------------------------')

        print('End')
        print(f'Your final score is: {self.score}')
