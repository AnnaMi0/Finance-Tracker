import tkinter as tk
from tkinter import *

import app

root = tk.Tk()

# Set the root window title, icon, size and background color
root.title('Finance Tracker') 
root.iconbitmap("icon.ico")
canvas = tk.Canvas(root, height = 600, width = 600, bg = "#3b3b3b")
canvas.pack()

#create top bar menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=app.donothing)
filemenu.add_command(label="Open", command=app.donothing)
filemenu.add_command(label="Save", command=app.donothing)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=app.donothing)
helpmenu.add_command(label="About...", command=app.donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

root.mainloop()