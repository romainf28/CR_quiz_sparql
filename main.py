import warnings
from play import Quiz
warnings.filterwarnings("ignore")


def launch_quiz():
    quiz = Quiz(nb_questions= 10)
    quiz.play()


if __name__ == '__main__':
    launch_quiz()