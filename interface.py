

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

        self.current_question = Label(gui, text=self.question_list[self.question_number],
                                      font=('ariel', 16, 'bold'), anchor='w')

        self.display_question()

        self.display_options()

    def radio_buttons(self):
        option_list = []
        row = 2

        while len(option_list) < 4:
            radio_btn = Radiobutton(gui, text=" ", variable=self.selected_option,
                                    value=len(option_list)+1, font=('ariel', 14))

            option_list.append(radio_btn)

            radio_btn.grid(row=row, column=1, columnspan=2, sticky="NW")

            row += 1

        return option_list

    def next_button(self):
        next_btn = Button(gui, text="Question suivante", command=self.next_question,
                          bg="green", fg="white", font=('ariel', 16, 'bold'))

        next_btn.grid(row=6, column=1, sticky="W")

    def quit_button(self):
        quit_btn = Button(gui, text="Quitter", command=gui.destroy,
                          bg="red", fg="white", font=('ariel', 16, 'bold'))

        quit_btn.grid(row=6, column=2, sticky="W")

    def display_question(self):
        self.current_question.grid_remove()

        self.current_question = Label(gui, text=self.question_list[self.question_number],
                                      font=('ariel', 16, 'bold'), anchor='w')

        self.current_question.grid(row=1, column=1, columnspan=2, sticky="W")

    def display_options(self):
        i = 0
        self.selected_option.set(0)

        for opt in self.option_list[self.question_number]:
            self.radio_btns[i]['text'] = opt
            i += 1

    def next_question(self):
        if self.selected_option.get() > 0:
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
                      bg='green', fg='white', font=('ariel', 20, 'bold'))
        title.grid(row=0, column=0, columnspan=3, sticky="NSEW")


gui = Tk()

gui.geometry("800x450")

gui.title("Quiz sur les départements français")

Grid.rowconfigure(gui, 0, weight=4)
Grid.columnconfigure(gui, 0, weight=20)

Grid.rowconfigure(gui, 1, weight=8)
Grid.columnconfigure(gui, 1, weight=5)

Grid.rowconfigure(gui, 2, weight=4)
Grid.columnconfigure(gui, 2, weight=55)

Grid.rowconfigure(gui, 3, weight=4)
Grid.rowconfigure(gui, 4, weight=4)
Grid.rowconfigure(gui, 5, weight=4)
Grid.rowconfigure(gui, 6, weight=17)

quiz = Quiz()

gui.mainloop()
