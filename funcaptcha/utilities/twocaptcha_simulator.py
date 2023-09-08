import tkinter
from tkinter import Tk, mainloop, Label

from PIL import ImageTk

from funcaptcha.utilities.databases.image_database import Grid

ref = []
i_s = []


def slave(grid: Grid, question: str):
    tk = Tk()
    x2d = tkinter.StringVar()
    Label(tk, text=question, font=('Verdana', 15))
    xd = ImageTk.PhotoImage(grid.img)
    ref.append(xd)
    label = Label(tk, image=xd)
    label.grid(row=3)
    xd3 = tkinter.Entry(tk, textvariable=x2d)
    xd3.grid(row=1)
    mainloop()
    while not x2d.get():
        pass
    print(x2d.get())
    return int(x2d.get())
