from query_handler import QueryHandler
import random

handler = QueryHandler()


def get_questions(question_type):
    match question_type:
        case 'dpt_code':
            return get_dpt_code_questions()
        case _:
            return


def get_dpt_code_questions(nb_questions=10):
    question_list = []
    option_list = []
    answer_list = []

    for _ in range(nb_questions):
        element, answer_prop, answer, options = handler.generate_question()

        if 'code_insee' == answer_prop.removesuffix('.value'):
            to_ask = 'Quel est le numéro du département nommé {} ?'.format(
                element)
        question_list.append(to_ask)
        options.append(answer)
        random.shuffle(options)
        answer_list.append(answer)
        option_list.append(options)

    return question_list, answer_list, option_list
