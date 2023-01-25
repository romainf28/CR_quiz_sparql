from tkinter import *
from PIL import Image, ImageTk
gui = Tk()
gui.geometry("480x480")

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

var = IntVar()


class Quiz():
    def __init__(self):
        self.radio_btns = self.radio_buttons()
        self.images = self.get_images()

    def radio_buttons(self):
        option_list = []
        row = 2

        while len(option_list) < 4:
            radio_btn = Radiobutton(gui, text="default", variable=var,
                                    value=len(option_list)+1, font=('ariel', 14))

            option_list.append(radio_btn)

            radio_btn.grid(row=row, column=1, columnspan=2, sticky="NW")

            row += 1

        return option_list

    def display_options(self):
        i = 0
        while i < 3:
            self.radio_btns[i].config(
                image=self.images[i])
            i += 1

    def get_images(self):
        i = 0
        images = []
        while i < 4:
            img = Image.open('assets/flags/01.png')
            resized_img = img.resize((180, 60))
            images.append(ImageTk.PhotoImage(resized_img))
            i += 1
        return images


quiz = Quiz()
quiz.display_options()
gui.mainloop()
