import sys
import os
import tkinter.messagebox
import webbrowser
from datetime import datetime
from tkinter import *
from pygame import *
import cv2
import keyboard
from PIL import Image, ImageTk
from tkcalendar import Calendar
from tkinter import filedialog
import subprocess
print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['C:\\Users\\Andrew\\PycharmProjects'])

def create_clock_window(root):

    clock_window = Toplevel(root)
    clock_window.geometry('200x100')
    clock_window.attributes('-topmost', True)
    clock_window["bg"] = "#2f3640"
    c1_label = Label(clock_window, text='00:00', font=("Arial", 15), bg="#2f3640", fg="#ffffff")
    c1_label.pack()
    c2_label = Label(clock_window, text='Kiev', font=("Arial", 15), bg="#2f3640", fg="#ffffff")
    c2_label.pack()

    def update_time():
        current_time = datetime.now().strftime("%H:%M:%S")
        c1_label.config(text=current_time)
        c1_label.after(1000, update_time)

    update_time()