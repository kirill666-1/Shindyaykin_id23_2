import math
from tkinter import *

root = Tk()
canvas = Canvas(root, width=600, height=600, bg='white')
canvas.pack()  # создал поле

canvas.create_oval(100, 100, 500, 500, outline='black')  # круг нарисовал

point = canvas.create_oval(295, 95, 305, 105, fill='blue', outline='black')  # создал точку

angle = 0  #


def move_point():
    global angle
    x = 300 + math.cos(math.radians(angle)) * 200
    y = 300 + math.sin(math.radians(angle)) * 200
    canvas.coords(point, x - 8, y - 8, x + 8, y + 8)  # размер в пикселях точка
    angle += 1  #
    root.after(16, move_point)  # временная задержка


move_point()

root.mainloop()
