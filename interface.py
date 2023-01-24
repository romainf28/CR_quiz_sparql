

from tkinter import *

from tkinter import messagebox as mb

from get_questions import get_questions, handler


class Quiz:
    def __init__(self):
        self.question_type = 'dpt_code'

        self.question_number = 0

        self.question_list, self.answers, self.option_list = get_questions(
            self.question_type)

        self.selected_option = IntVar()

        self.nb_correct = 0

        self.nb_questions = len(self.question_list)

        self.display_title()

        self.quit_button()

        self.next_button()

        self.radio_btns = self.radio_buttons()

        self.display_question()

        self.display_options()

    def radio_buttons(self):
        option_list = []
        y_pos = 150

        while len(option_list) < 4:
            radio_btn = Radiobutton(gui, text=" ", variable=self.selected_option,
                                    value=len(option_list)+1, font=('ariel', 14))

            option_list.append(radio_btn)

            radio_btn.place(x=100, y=y_pos)
            y_pos += 40

        return option_list

    def next_button(self):
        next_btn = Button(gui, text="Question suivante", command=self.next_question,
                          width=20, bg="blue", fg="white", font=('ariel', 16, 'bold'))

        next_btn.place(x=350, y=380)

    def quit_button(self):
        quit_btn = Button(gui, text="Quitter", command=gui.destroy,
                          width=10, bg="black", fg="white", font=('ariel', 16, 'bold'))

        quit_btn.place(x=700, y=50)

    def display_question(self):
        question = Label(gui, text=self.question_list[self.question_number],
                         width=60, font=('ariel', 16, 'bold'), anchor='w')

        question.place(x=70, y=100)

    def display_options(self):
        i = 0
        self.selected_option.set(0)

        for opt in self.option_list[self.question_number]:
            self.radio_btns[i]['text'] = opt
            i += 1

    def next_question(self):
        if self.check_answer(self.question_number):
            self.nb_correct += 1

        self.question_number += 1

        if self.question_number == self.nb_questions:
            self.summary()
            gui.destroy()

        else:
            self.display_question()
            self.display_options()

    def check_answer(self, question_number):
        return self.option_list[self.question_number][self.selected_option.get()-1] == self.answers[question_number]

    def summary(self):
        mb.showinfo(
            'Résultats', message='Score : {}/{}'.format(self.nb_correct, self.nb_questions))

    def display_title(self):
        title = Label(gui, text='Quiz sur les départements français',
                      width=50, bg='green', fg='white', font=('ariel', 20, 'bold'))
        title.place(x=0, y=2)


gui = Tk()

gui.geometry("800x450")

gui.title("Quiz sur les départements français")

quiz = Quiz()

gui.mainloop()
