

from tkinter import *

from tkinter import messagebox as mb

from get_questions import get_questions, get_new_question
from PIL import Image, ImageTk
from queries import AVAILABLE_QUESTION_TYPES
from abc import ABC, abstractmethod


class BaseQuiz(Tk, ABC):
    def __init__(self, gui):
        self.gui = gui

        self.images = [None for i in range(4)]

        self.answer_image = None

        self.question_number = 0

        self.selected_option = IntVar()

        self.nb_correct = 0

        self.question_list, self.answers, self.option_list, self.question_types = [], [], [], []

        self.nb_questions = 0

        self.quit_button()

        self.next_button()

    def radio_buttons(self):
        option_list = []
        row = 2

        while len(option_list) < 4:
            radio_btn = Radiobutton(self.gui, text="", variable=self.selected_option,
                                    value=len(option_list)+1, font=('ariel', 14))

            option_list.append(radio_btn)

            if AVAILABLE_QUESTION_TYPES[self.question_types[self.question_number]].get('image'):
                radio_btn.grid(row=row - row %
                               2, column=1+row % 2, sticky="NW")
            else:
                radio_btn.grid(row=row, column=1, columnspan=2, sticky="NW")

            row += 1

        return option_list

    def next_button(self):
        next_btn = Button(self.gui, text="Question suivante", command=self.next_question,
                          bg="green", fg="white", font=('ariel', 16, 'bold'))

        next_btn.grid(row=6, column=1, sticky="W")

    def quit_button(self):
        quit_btn = Button(self.gui, text="Quitter", command=self.gui.destroy,
                          bg="red", fg="white", font=('ariel', 16, 'bold'))

        quit_btn.grid(row=6, column=2, sticky="W")

    def display_question(self):
        self.current_question.grid_remove()

        self.current_question = Label(self.gui, text=self.question_list[self.question_number],
                                      font=('ariel', 16, 'bold'), anchor='w')

        self.current_question.grid(row=1, column=1, columnspan=2, sticky="W")

    def display_options(self):
        i = 0
        self.selected_option.set(0)

        question_type = self.question_types[self.question_number]
        if AVAILABLE_QUESTION_TYPES[question_type].get('image'):
            for opt in self.option_list[self.question_number]:
                img = Image.open(opt)
                resized_img = img.resize((300, 150))
                flag_img = ImageTk.PhotoImage(resized_img)
                self.images[i] = flag_img
                self.radio_btns[i].config(
                    image=self.images[i])
                i += 1

        else:
            for opt in self.option_list[self.question_number]:
                self.radio_btns[i]['text'] = opt
                i += 1

    @abstractmethod
    def next_question(self):
        pass

    def check_answer(self, question_number):
        return self.option_list[self.question_number][self.selected_option.get()-1] == self.answers[question_number]

    @abstractmethod
    def summary(self):
        pass

    def reset_buttons(self):
        for btn in self.radio_btns:
            btn.destroy()
        self.radio_btns = self.radio_buttons()

    @abstractmethod
    def show_error_message(self):
        pass


class Quiz(Tk):
    def __init__(self, gui, nb_questions=10, question_types=None):
        self.gui = gui

        self.images = [None for i in range(4)]

        self.answer_image = None

        self.question_number = 0

        self.question_list, self.answers, self.option_list, self.question_types = get_questions(
            nb_questions, question_types=question_types)
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
            radio_btn = Radiobutton(self.gui, text="", variable=self.selected_option,
                                    value=len(option_list)+1, font=('ariel', 14))

            option_list.append(radio_btn)

            if AVAILABLE_QUESTION_TYPES[self.question_types[self.question_number]].get('image'):
                radio_btn.grid(row=row - row %
                               2, column=1+row % 2, sticky="NW")
            else:
                radio_btn.grid(row=row, column=1, columnspan=2, sticky="NW")

            row += 1

        return option_list

    def next_button(self):
        next_btn = Button(self.gui, text="Question suivante", command=self.next_question,
                          bg="green", fg="white", font=('ariel', 16, 'bold'))

        next_btn.grid(row=6, column=1, sticky="W")

    def quit_button(self):
        quit_btn = Button(self.gui, text="Quitter", command=self.gui.destroy,
                          bg="red", fg="white", font=('ariel', 16, 'bold'))

        quit_btn.grid(row=6, column=2, sticky="W")

    def display_question(self):
        self.current_question.grid_remove()

        self.current_question = Label(self.gui, text=self.question_list[self.question_number],
                                      font=('ariel', 16, 'bold'), anchor='w')

        self.current_question.grid(row=1, column=1, columnspan=2, sticky="W")

    def display_options(self):
        i = 0
        self.selected_option.set(0)

        question_type = self.question_types[self.question_number]
        if AVAILABLE_QUESTION_TYPES[question_type].get('image'):
            for opt in self.option_list[self.question_number]:
                img = Image.open(opt)
                resized_img = img.resize((300, 150))
                flag_img = ImageTk.PhotoImage(resized_img)
                self.images[i] = flag_img
                self.radio_btns[i].config(
                    image=self.images[i])
                i += 1

        else:
            for opt in self.option_list[self.question_number]:
                self.radio_btns[i]['text'] = opt
                i += 1

    def next_question(self):
        if self.selected_option.get() > 0:
            if self.check_answer(self.question_number):
                mb.showinfo("Correct", "Bonne réponse, poursuivez ainsi !")
                self.nb_correct += 1

            else:
                self.show_error_message()
            self.question_number += 1

            if self.question_number == self.nb_questions:
                self.summary()
                self.gui.destroy()

            else:
                self.reset_buttons()
                self.display_question()
                self.display_options()

    def check_answer(self, question_number):
        return self.option_list[self.question_number][self.selected_option.get()-1] == self.answers[question_number]

    def summary(self):
        mb.showinfo(
            'Résultats', message='Score : {}/{}'.format(self.nb_correct, self.nb_questions))

    def display_title(self):
        title = Label(self.gui, text='Quiz sur les départements français',
                      bg='green', fg='white', font=('ariel', 20, 'bold'))
        title.grid(row=0, column=0, columnspan=3, sticky="NSEW")

    def reset_buttons(self):
        for btn in self.radio_btns:
            btn.destroy()
        self.radio_btns = self.radio_buttons()

    def show_error_message(self):

        question_type = self.question_types[self.question_number]
        if AVAILABLE_QUESTION_TYPES[question_type].get('image'):
            image = Image.open(self.answers[self.question_number])
            image = image.resize((300, 150))
            image = ImageTk.PhotoImage(image)
            self.answer_image = image
            self.gui.display_error_window(self.answer_image)
        else:
            mb.showerror("Erreur", "Mauvaise réponse ! La réponse correcte était " +
                         str(self.answers[self.question_number]))


class StandardQuiz(BaseQuiz):
    def __init__(self, gui, nb_questions=10, question_types=None):
        super().__init__(gui)
        self.question_list, self.answers, self.option_list, self.question_types = get_questions(
            nb_questions, question_types=question_types)
        self.nb_questions = len(self.question_list)
        self.radio_btns = self.radio_buttons()

        self.current_question = Label(gui, text=self.question_list[self.question_number],
                                      font=('ariel', 16, 'bold'), anchor='w')

        self.display_question()

        self.display_options()

    def summary(self):
        mb.showinfo(
            'Résultats', message='Score : {}/{}'.format(self.nb_correct, self.nb_questions))

    def next_question(self):
        if self.selected_option.get() > 0:
            if self.check_answer(self.question_number):
                mb.showinfo("Correct", "Bonne réponse, poursuivez ainsi !")
                self.nb_correct += 1

            else:
                self.show_error_message()
            self.question_number += 1

            if self.question_number == self.nb_questions:
                self.summary()
                self.gui.destroy()

            else:
                self.reset_buttons()
                self.display_question()
                self.display_options()

    def show_error_message(self):

        question_type = self.question_types[self.question_number]
        if AVAILABLE_QUESTION_TYPES[question_type].get('image'):
            image = Image.open(self.answers[self.question_number])
            image = image.resize((300, 150))
            image = ImageTk.PhotoImage(image)
            self.answer_image = image
            self.gui.display_error_window(image=self.answer_image)
        else:
            self.gui.display_error_window(
                text_answer=self.answers[self.question_number])


class SurvivalQuiz(BaseQuiz):
    def __init__(self, gui, nb_lives=3, question_types=None):
        super().__init__(gui)
        self.nb_lives = nb_lives
        self.question_list, self.answers, self.option_list, self.question_types = get_new_question(
            question_types=question_types, already_asked=[])
        self.already_asked = [self.question_list[0]]

        self.radio_btns = self.radio_buttons()

        self.current_question = Label(gui, text=self.question_list[self.question_number],
                                      font=('ariel', 16, 'bold'), anchor='w')

        self.display_question()

        self.display_options()

    def next_question(self):
        if self.selected_option.get() > 0:
            if self.check_answer(self.question_number):
                mb.showinfo("Correct", "Bonne réponse, poursuivez ainsi !")
                self.nb_correct += 1

            else:
                self.nb_lives -= 1
                self.show_error_message()

            if self.nb_lives == 0:
                self.summary()
                self.gui.destroy()

            self.question_list, self.answers, self.option_list, self.question_types = get_new_question(
                question_types=None, already_asked=self.already_asked)

            self.reset_buttons()
            self.display_question()
            self.display_options()

    def summary(self):
        mb.showinfo(
            'Résultats', message='Score : {} bonnes réponses données'.format(self.nb_correct))

    def show_error_message(self):

        question_type = self.question_types[self.question_number]
        if AVAILABLE_QUESTION_TYPES[question_type].get('image'):
            image = Image.open(self.answers[self.question_number])
            image = image.resize((300, 150))
            image = ImageTk.PhotoImage(image)
            self.answer_image = image
            self.gui.display_error_window(
                image=self.answer_image, nb_lives=self.nb_lives)
        else:
            self.gui.display_error_window(
                text_answer=str(self.answers[self.question_number]), nb_lives=self.nb_lives)


class ErrorWindowWithImage(Toplevel):
    def __init__(self, master, image=None, nb_lives=None, text_answer=None):
        Toplevel.__init__(self, master)
        self.images = []

        label_message = None
        if nb_lives != None and nb_lives >= 0:
            first_part = first_part = f"Plus que {nb_lives} vies ! " if nb_lives else "Plus de vies ! "
        else:
            first_part = "Mauvaise réponse ! "

        if text_answer:
            label_message = Label(self, text=first_part + "La réponse correcte était : " + str(text_answer), font=(
                "TkDefaultFont", 16))
        elif image:
            label_message = Label(self, text=first_part + "La réponse correcte était : ", font=(
                "TkDefaultFont", 16), compound="bottom", image=image)
        self.images.append(image)
        label_message.image = self.images[0]
        label_message.pack()

        button = Button(self, text="OK", command=self.destroy)
        button.pack()


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("800x450")

        self.title("Quiz sur les départements français")

        self.config_grid()

        self.display_title()
        Label(self, text='Veuillez choisir un mode de jeu : ',
              font=('ariel', 16)).grid(row=1, column=1, columnspan=3, sticky="W")
        self.standard_btn = Button(
            self, text='Standard', command=lambda: self.launch_quiz(mode='standard'))
        self.standard_btn.grid(row=2, column=1, sticky="W")

        self.survival_btn = Button(
            self, text='Survie', command=lambda: self.launch_quiz(mode='survival'))
        self.survival_btn.grid(row=4, column=1, sticky="W")

    def config_grid(self):
        Grid.rowconfigure(self, 0, weight=4)
        Grid.columnconfigure(self, 0, weight=20)

        Grid.rowconfigure(self, 1, weight=8)
        Grid.columnconfigure(self, 1, weight=30)

        Grid.rowconfigure(self, 2, weight=4)
        Grid.columnconfigure(self, 2, weight=30)

        Grid.rowconfigure(self, 3, weight=4)
        Grid.rowconfigure(self, 4, weight=4)
        Grid.rowconfigure(self, 5, weight=4)
        Grid.rowconfigure(self, 6, weight=17)

    def display_title(self):
        title = Label(self, text='Quiz sur les départements français',
                      bg='green', fg='white', font=('ariel', 20, 'bold'))
        title.grid(row=0, column=0, columnspan=3, sticky="NSEW")

    def launch_quiz(self, mode='standard'):
        self.standard_btn.destroy()
        self.survival_btn.destroy()
        if mode == 'standard':
            StandardQuiz(self)
        elif mode == 'survival':
            SurvivalQuiz(self)
        else:
            raise Exception(
                'Please chose one of the following modes : \n standard\n survival')

    def display_error_window(self, image=None, nb_lives=None, text_answer=None):
        window = ErrorWindowWithImage(
            self, image=image, nb_lives=nb_lives, text_answer=text_answer)
        window.title("Erreur")
        window.geometry("800x450")
