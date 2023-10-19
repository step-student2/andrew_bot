import time
import tkinter.messagebox
from datetime import datetime
from tkinter import *

from PIL import Image, ImageTk

current_os_version = "-= MacOS 17.1 =-"


now = datetime.now()
current_time = now.strftime("%H:%M:%S")

text = None

current_country = "Ukraine"

root = Tk()
root.geometry('1920x1080')

root2 = Tk()
root2.geometry('400x500')

label = Label(root, text=" ")
label_ln = Label(root, text=" ", image=None)

label_ln.pack()
label.pack()




global cache, cache_save
cache_save = []

def none():
    print("button removed")
def show(pos1, pos2, text, size, cache):
    label.config(text=text, font=size)
    label.pack(pady=pos1, padx=pos2)

    if cache != cache_save:
        add_to_cache = cache_save.append(cache)

def load():
    show(50, 50, "MacOS", 0.5, None)
    show(50, 70, "", 0.5, "rc_ln")

    updater_c(cache_save)

global start_btn
start_btn = Button(root2, text='start', command=load)
start_btn.pack()


def draw_home_screen():
    label.config(text=" ")
    label_ln.config(text=" ")
    show(50, 50, "home screen", 0.5, None)

    image = Image.open('C:/Users/Andrew/PycharmProjects/img/sonoma.jpg')

    my_img = ImageTk.PhotoImage(image)

    label_ln.config(image=my_img)

def updater_c(cache):

    print(cache_save)
    if "rc_ln" in cache_save:
        label_ln.config(text="-")
        time.sleep(0.9)
        label_ln.config(text="--")
        time.sleep(0.9)
        label_ln.config(text="---")
        time.sleep(0.9)
        label_ln.config(text="----")
        draw_home_screen()
        cache_save.clear()
        start_btn.config(command=none)
        print(cache_save)












root.mainloop()
root2.mainloop()
