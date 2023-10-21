import os
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
import cv2
import webbrowser

photo_save_path = 'C:/Users/Andrew/PycharmProjects/photos/'  # Замените на свой путь

if not os.path.exists(photo_save_path):
    os.makedirs(photo_save_path)

def create_camera_window():
    global photo_saved_message, camera_label
    camera_window = Toplevel(root)
    camera_window.attributes('-topmost', True)  # Окно поверх всех других окон

    cap = cv2.VideoCapture(0)

    def take_photo():
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        photo_filename = f"photo_{timestamp}.jpg"
        full_path = os.path.join(photo_save_path, photo_filename)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(full_path, frame)
            photo_saved_message.set(f"Фото сохранено: {photo_filename}")

    camera_label = Label(camera_window)
    camera_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_camera_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (1920, 1080))  # Размер кадра совпадает с размерами экрана
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            camera_label.config(image=photo)
            camera_label.image = photo
            if camera_window.winfo_exists():
                camera_label.after(10, update_camera_frame)

    update_camera_frame()

    def close_camera_window():
        cap.release()
        camera_window.destroy()

    camera_window.protocol("WM_DELETE_WINDOW", close_camera_window)

    take_photo_button = Button(camera_window, text="Take Photo", font=("Arial", 20), command=take_photo)
    take_photo_button.place(relx=0.5, rely=0.95, anchor='s')
    take_photo_button.configure(bg='white', relief=SOLID, borderwidth=0)
    take_photo_button.configure(activebackground=take_photo_button.cget('background'))

root = Tk()
root.geometry('1920x1080')

background_image_path = 'C:/Users/Andrew/PycharmProjects/img/sonoma.jpg'  # Замените путь на свой файл с изображением
image = Image.open(background_image_path)
image = image.resize((1920, 1080))  # Растягиваем изображение на весь экран
photo = ImageTk.PhotoImage(image)
background_label = Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def search():
    google_url = 'https://www.google.com/search?q='
    webbrowser.open(google_url)

btn_search = Button(root, text="Search", font=("Arial", 20), command=search)
btn_search.pack()

btn_open_camera = Button(root, text="Open Camera", font=("Arial", 20), command=create_camera_window)
btn_open_camera.pack()

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    label_time.config(text=current_time)
    label_time.after(1000, update_time)

label_time = Label(root, text="time", font=("Arial", 40))
label_time.pack()

update_time()
root.mainloop()
