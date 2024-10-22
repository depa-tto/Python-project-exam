                print('-------------------------------------------')
                print(f'Round {round_number + 1}')
                
                question_func = question_funcs[round_number % len(question_funcs)]
                question, correct_answer = question_func()
                choices = self.gen_answers(correct_answer)
                chosen_answer, correct_answer = self.ask_question(question, correct_answer, choices)
                self.score = self.score_fun(chosen_answer, correct_answer, dif)