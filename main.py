import warnings
from interface import Quiz
from tkinter import *
warnings.filterwarnings("ignore")


def launch_quiz():
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

    quiz = Quiz(gui)

    gui.mainloop()


if __name__ == '__main__':
    launch_quiz()
