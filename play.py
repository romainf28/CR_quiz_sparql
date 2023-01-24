from query_handler import QueryHandler
import random

class Question():
    def __init__(self, element, to_ask, answer, options = []):
        self.element = element
        self.to_ask = to_ask
        self.answer = answer
        self.options = options
        self.options.append(answer)
        random.shuffle(self.options)
        self.question = self.to_ask + " of " + self.element + " ?"

    def ask(self):
        print(self.question)
        for i, option in enumerate(self.options):
            print("Option ", i+1, ": ", option)

    def get_answer(self):
        id = int(input("Write your answer:"))
        return self.options[id-1]

    def check_answer(self, input):
        return input == self.answer

class Quiz(object):
    def __init__(self, nb_questions = 10):
        self.score = 0
        self.end_game = False
        self.more_questions = False
        self.questions = []     
        self.handler =  QueryHandler()
        self.nb_questions = nb_questions

    def start(self):
        self.score = 0
        self.end_game = False
        self.more_questions = False
        
        for _ in range(self.nb_questions):
            element, answer_prop, answer, options = self.handler.generate_question()
            to_ask = answer_prop.removesuffix('.value')
            question = Question(element, to_ask, answer, options)
            self.questions.append(question)


    def get_additional_questions(self):
        for _ in range(self.nb_questions):
            element, answer_prop, answer, options = self.handler.generate_question()
            to_ask = answer_prop.removesuffix('.value')
            question = Question(element, to_ask, answer, options)
            self.questions.append(question)
        self.more_questions = False

    def ask_and_get_score(self):
        if len(self.questions) == 0:
            self.end_game = True
            return
        question = self.questions.pop()
        question.ask()
        answer = question.get_answer()
        if question.check_answer(answer):
            self.score += 1
            print("Bonne réponse !")
        else:
            print("Mauvaise réponse !")
        return self.score

    def play(self):
        self.start()
        while not self.end_game:
            self.ask_and_get_score()
        print("Final score: ", self.score,'/', self.nb_questions)
