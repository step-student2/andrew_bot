from tkinter import *

from PIL import ImageGrab, Image, ImageTk

root = Tk()
root.geometry('1920x1080')

root2 = Tk()
root2.geometry('300x300')

active = False
background_image_path = 'C:/Users/Andrew/PycharmProjects/photos/p_black.png'
def share():
    global active
    if active:
        active = False
    else:
        active = True

    print(active)
    screen()

def screen():
    global background_image_path
    if not active:
        background_image_path = 'C:/Users/Andrew/PycharmProjects/photos/p_black.png'

    if active:
        screenshot = ImageGrab.grab()  # Захват экрана
        screenshot = screenshot.resize((1920, 1080))  # Изменение размера захваченного изображения
        photo = ImageTk.PhotoImage(screenshot)

        background_label.config(image=photo)
        background_label.image = photo
        root.after(1000, screen())




image = Image.open(background_image_path)
image = image.resize((1920, 1080))
photo = ImageTk.PhotoImage(image)
background_label = Label(root, image=photo)
background_label.image = photo

background_label.place(x=0, y=0, relwidth=1, relheight=1)

btn = Button(root2, text="Share screen", command=share)
btn.pack()


root.mainloop()
root2.mainloop()
