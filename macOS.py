import os
import random
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
from instruments_for_os_project import music_player, clock
import pyexecutor

# Импортировать Calendar из tkcalendar

mixer.init()

notes_opened = False
music_player_opened = False
calendar_opened = False
photo_viewer_opened = False
camera_opened = False
explorer_opened = False

photo_save_path = 'C:/Users/Andrew/PycharmProjects/photos/'  # Замените на свой путь

if not os.path.exists(photo_save_path):
    os.makedirs(photo_save_path)

background_image_path = 'путь_к_фоновому_изображению.jpg'  # Замените на путь к своему фоновому изображению


def create_music_player():
    music_player.create_music_player_init(root)


music_order = []
photo_order = []
notes_order = []
path = []


def create_file_explorer(item_path):
    global explorer_opened, music_order, photo_order, notes_order

    file_explorer = Toplevel(root)
    file_explorer.geometry('800x600')
    file_explorer.attributes('-topmost', True)
    file_explorer.title("Проводник")

    # Создайте список файлов и папок в выбранной директории
    if item_path is None:
        directory_path = 'C:/Users/Andrew/PycharmProjects/'  # Замените на свой путь

    else:
        directory_path = item_path

    files_and_folders = os.listdir(directory_path)

    listbox = Listbox(file_explorer, selectmode=SINGLE, font=("Arial", 16), background='#49515e')
    listbox.pack(expand=YES, fill=BOTH)

    # Заполните список файлов и папок в окне "Проводника"
    for item in files_and_folders:
        listbox.insert(END, item)

    def open_selected_item(*args):
        selected_item = listbox.get(listbox.curselection())
        selected_item = listbox.get(listbox.curselection())
        item_path = os.path.join(directory_path, selected_item)
        print(item_path)
        path.append(item_path)

        if os.path.isfile(item_path):
            if item_path.endswith('.txt'):
                notes_order.append(selected_item)
                create_notes_window()
            elif item_path.endswith(('.mp3', '.wav', '.mp4', '.ogg')):
                music_order.append(selected_item)
                create_music_player()
            elif item_path.endswith(('.png', '.jpg')):
                photo_order.append(selected_item)
                create_photo_viewer()
            elif item_path.endswith(('.py')):
                try:
                    subprocess.run(["python3",
                                    f"{selected_item}"])  # Замените "python3" на "python" или другую команду, если нужно
                except Exception as e:
                    tkinter.messagebox.ERROR("Ошибка при запуске .py:", str(e))

            elif not item_path.endswith(('.txt', '.mp3', '.wav', '.mp4', '.ogg', '.png', '.jpg', '.py')):
                tkinter.messagebox.showerror(title="Format error",
                                             message="Unsupported format! Try '.txt', '.mp3', '.wav', '.mp4', '.ogg', '.png', '.jpg'")

        elif os.path.isdir(item_path):
            create_file_explorer(item_path)

    btn_open_dir = Button(file_explorer, text="Open", command=open_selected_item)
    btn_open_dir.pack()

    explorer_opened = True


def create_calendar_window():
    global calendar_opened
    calendar_window = Toplevel(root)
    calendar_window.geometry('400x400')
    calendar_window.attributes('-topmost', True)

    calendar = Calendar(calendar_window, selectmode="day", year=2023, month=10, day=14)
    calendar.pack(fill="both", expand=True)


notes_listbox = None


def create_notes_window():
    global notes_listbox  # Use the global variable
    notes_window = Toplevel(root)
    notes_window.geometry('800x600')
    notes_window.attributes('-topmost', True)
    notes_window.title("Заметки")

    notes_listbox = Listbox(notes_window, selectmode=SINGLE, font=("Arial", 16), background='#49515e')
    notes_listbox.pack(expand=YES, fill=BOTH)

    notes_text = Text(notes_window, wrap=WORD, font=("Arial", 16), background='#49515e')
    notes_text.pack(expand=YES, fill=BOTH)

    # Поле для ввода нового имени заметки
    new_name_entry = Entry(notes_window, font=("Arial", 16), background='#49515e')
    new_name_entry.pack(fill=X)

    def save_notes():
        notes = notes_text.get("1.0", "end-1c")  # Получаем текст из текстового поля
        print(len(os.path.join('C:/Users/Andrew/PycharmProjects/notes')))
        notes_filename = f"note{len(os.path.join('C:/Users/Andrew/PycharmProjects/notes')) + 1}"
        notes_file = os.path.join('C:/Users/Andrew/PycharmProjects/notes', notes_filename + ".txt")
        with open(notes_file, "w") as f:
            f.write(notes)
        tkinter.messagebox.showinfo("Заметки", "Заметки успешно сохранены.")
        update_notes_list()

    def update_notes_name():
        selected_note = notes_listbox.get(notes_listbox.curselection())
        new_name = new_name_entry.get()
        if selected_note and new_name:
            new_note_path = os.path.join('C:/Users/Andrew/PycharmProjects/notes', new_name)
            if os.path.exists(new_note_path):
                tkinter.messagebox.showerror("Ошибка", "Заметка с таким именем уже существует.")
            else:
                old_note_path = os.path.join('C:/Users/Andrew/PycharmProjects/notes', selected_note)
                os.rename(old_note_path, new_note_path)
                update_notes_list()

    def delete_selected_note():
        selected_note = notes_listbox.get(notes_listbox.curselection())
        if selected_note:
            note_path = os.path.join('C:/Users/Andrew/PycharmProjects/notes', selected_note)
            os.remove(note_path)
            update_notes_list()

    def update_notes_list():
        if notes_listbox:  # Check if the notes_listbox exists
            notes = [file for file in os.listdir('C:/Users/Andrew/PycharmProjects/notes') if file.endswith('.txt')]
            notes_listbox.delete(0, END)
            for note in notes:
                notes_listbox.insert(END, note)

    def select_note(event):
        selected_note = notes_listbox.get(notes_listbox.curselection())
        with open(os.path.join('C:/Users/Andrew/PycharmProjects/notes', selected_note), 'r') as f:
            note_contents = f.read()
            notes_text.delete("1.0", "end")
            notes_text.insert("1.0", note_contents)
            new_name_entry.delete(0, END)
            new_name_entry.insert(0, selected_note)

    save_button = Button(notes_window, text="Сохранить", font=("Arial", 16), command=save_notes)
    save_button.pack()

    # Кнопка для обновления имени заметки
    update_name_button = Button(notes_window, text="Изменить имя", font=("Arial", 16), command=update_notes_name)
    update_name_button.pack()

    # Кнопка для удаления выбранной заметки
    delete_button = Button(notes_window, text="Удалить заметку", font=("Arial", 16), command=delete_selected_note)
    delete_button.pack()

    update_notes_list()
    notes_listbox.bind('<<ListboxSelect>>', select_note)

    return notes_listbox


def create_clock_window():
    clock.create_clock_window(root)


def create_camera_window():
    global photo_saved_message, camera_label
    camera_window = Toplevel(root)
    camera_window.geometry('1100x1000')
    camera_window.attributes('-topmost', True)

    cap = cv2.VideoCapture(0)

    def take_photo():
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-d_%H-%M-%S")
        photo_filename = f"photo_{timestamp}.png"
        full_path = os.path.join(photo_save_path, photo_filename)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(full_path, frame)
            try:
                photo_saved_message.set(f"Фото сохранено: {photo_filename}")
            except Exception:
                pass

    camera_label = Label(camera_window)
    camera_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_camera_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (1920, 1080))
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
root.attributes('-fullscreen', True)
background_image_path = 'C:/Users/Andrew/PycharmProjects/img/sonoma.jpg'
image = Image.open(background_image_path)
image = image.resize((1920, 1080))
photo = ImageTk.PhotoImage(image)
background_label = Label(root, image=photo)
background_label.image = photo

background_label.place(x=0, y=0, relwidth=1, relheight=1)

photo_label = None
current_photo_index = 0

photo_directory = 'C:/Users/Andrew/PycharmProjects/photos/'

file_paths = [os.path.join(photo_directory, filename) for filename in os.listdir(photo_directory)]


def create_photo_viewer():
    global photo_label, current_photo_index, photo_order, selected_item
    photo_viewer = Toplevel(root)
    photo_viewer.attributes('-topmost', True)

    current_photo_index = 0

    def show_photo(index):
        global current_photo_index, curr_label

        # if 0 <= index < len(file_paths):
        #     if len(photo_order) >  0:
        #         subprocess.run(["",
        #                         f"{path[0]}"])
        #         # selected_item = path[0]
        #         # print(selected_item)
        #         # photo_label.config(image=selected_item)
        #         # photo_order.clear()
        #
        #         # if len(photo_order) > 0 :
        #         #     selected_item = path[0] + '/' + photo_order[0]
        #         #     print(selected_item)
        #         #     photo_label.config(image=selected_item)
        #         #     photo_order.clear()
        #
        #     else:
        image = Image.open(file_paths[index])
        photo = ImageTk.PhotoImage(image)
        photo_label.config(image=photo)
        photo_label.image = photo
        current_photo_index = index

    photo_label = Label(photo_viewer)
    photo_label.pack()

    prev_button = Button(photo_viewer, text="Previous", font=("Arial", 20),
                         command=lambda: show_photo(current_photo_index - 1) if current_photo_index > 0 else None)
    next_button = Button(photo_viewer, text="Next", font=("Arial", 20),
                         command=lambda: show_photo(current_photo_index + 1) if current_photo_index < len(
                             file_paths) - 1 else None)

    prev_button.pack(side=LEFT)
    next_button.pack(side=RIGHT)

    show_photo(current_photo_index)

    def delete_photo():
        global current_photo_index, curr_label, file_paths

        if 0 <= current_photo_index < len(file_paths):
            os.remove(file_paths[current_photo_index])
            file_paths.pop(current_photo_index)

        if current_photo_index >= len(file_paths):
            current_photo_index = len(file_paths) - 1

        if current_photo_index >= 0:
            show_photo(current_photo_index)
        else:
            photo_label.config(image=None)  # Очистите фото, если нет доступных фотографий

    if current_photo_index >= len(file_paths):
        current_photo_index = len(file_paths) - 1

    if current_photo_index >= 0:
        show_photo(current_photo_index)
    else:
        photo_label.config(image=None)  # Очистите фото, если нет доступных фотографий

    delete_button = Button(photo_viewer, text="Delete", font=("Arial", 20), command=delete_photo)
    delete_button.pack(side=TOP)


def pop_paint_icon():
    open_paint_button.destroy()
    tkinter.messagebox.showwarning(title="App Tools (currently App Store)",
                                   message="Successfully uninstalled Freeform and removed from apps tab")


def pop_python_icon():
    open_python_button.destroy()
    tkinter.messagebox.showwarning(title="App Tools (currently App Store)",
                                   message="Successfully uninstalled Python and removed from apps tab")


def create_paint_icon():
    try:
        open_paint_button.pack(side='left', padx=1)
        tkinter.messagebox.showinfo(title="App Tools (currently App Store)",
                                    message="Successfully installed Freeform and added to apps tab")
    except Exception:
        temp_res = random.randint(1, 3)
        if temp_res == 1:
            tkinter.messagebox.showerror(title="App Tools (currently App Store)",
                                         message="Can not load app from the server, check your internet connection and try again later!")
        else:
            tkinter.messagebox.showerror(title="App Tools (currently App Store)",
                                         message="Can not load app from the server, File not found on download url (Error 404), try again later!")


def create_python_icon():
    try:
        open_python_button.pack(side='left', padx=1)
        tkinter.messagebox.showinfo(title="App Tools (currently App Store)",
                                    message="Successfully installed Python 3.10 and added to apps tab")
    except Exception:
        temp_res = random.randint(1, 3)
        if temp_res == 1:
            tkinter.messagebox.showerror(title="App Tools (currently App Store)",
                                         message="Can not load app from the server, check your internet connection and try again later!")
        else:
            tkinter.messagebox.showerror(title="App Tools (currently App Store)",
                                         message="Can not load app from the server, File not found on download url (Error 404), try again later!")


def create_personal_app():
    pass


def create_app_modif():
    pass


def create_personal_app_modifier():
    global name_entry, app_name
    p_app = Toplevel(root)
    p_app.attributes('-topmost', True)
    p_app.title("Dev Tools")
    p_app.geometry("400x300")

    app_name = "App 1"

    btn_open_m_app1 = Button(p_app, text=f"Open {app_name} in modifier", command=create_app_modif)
    btn_open_app1 = Button(p_app, text=f"Open {app_name}", command=create_personal_app)
    btn_add_app1 = Button(p_app, text=f"Add {app_name} to home screen",
                          command=open_p_app1_button.pack(side='left', padx=1))
    btn_del_app1 = Button(p_app, text=f"Delete {app_name} from home screen", command=pop_personal_app)

    btn_del_app1.place(x=0, y=40)
    btn_open_app1.place(x=0, y=60)
    btn_open_m_app1.place(x=0, y=80)


def pop_personal_app():
    open_p_app1_button.destroy()
    tkinter.messagebox.showwarning(title="Dev Tools (currently Commands)",
                                   message="Successfully deleted personal app and removed from apps tab. You can restore it in the modifier or completely delete it/")


def app_store_window():
    app_store = Toplevel(root)
    app_store.attributes('-topmost', True)
    app_store.title("App Tools")
    menu = Menu(app_store)
    app_store.config(menu=menu)

    app_menu = Menu(menu)
    menu.add_cascade(label="Apps", menu=app_menu, font=("Arial", 30))
    app_menu.add_separator()
    app_menu.add_command(label="Freeform", command=create_paint_icon, font=("Arial", 20))
    app_menu.add_command(label="Python", command=create_python_icon, font=("Arial", 20))
    app_menu.add_command(label="Create personal App=-\n"
                               "------====New!====------", command=create_personal_app_modifier, font=("Arial", 20))

    app_del_menu = Menu(menu)
    menu.add_cascade(label="Manage apps", menu=app_del_menu, font=("Arial", 30))
    app_del_menu.add_separator()
    app_del_menu.add_command(label="Delete Freeform", command=pop_paint_icon, font=("Arial", 20))
    app_del_menu.add_command(label="Delete Python", command=pop_python_icon, font=("Arial", 20))
    app_del_menu.add_command(label="-=Delete personal App=-\n"
                                   "------====New!====------", command=pop_personal_app, font=("Arial", 20))

    label_text = Label(app_store, text="App Tools for MacOS", font=("Arial", 15))
    label_text.pack()


def create_python_window():
    python_win = Toplevel(root)
    python_win.attributes('-topmost', True)
    python_win.geometry("150x150")
    command_entry = Entry(python_win)
    command_entry.pack()
    label = Label(python_win, text=">>>")

    def run_command():
        entry_result = command_entry.get()
        log = pyexecutor.Executor(entry_result)
        log2 = pyexecutor.Logger(entry_result)
        label.config(text=log)

    run_button = Button(python_win, text="Run command", command=run_command)
    run_button.pack()


def run_paint():
    try:
        subprocess.run(["C:/Users/Andrew/Downloads/PyDPainter.exe"])
        # Замените "python3" на "python" или другую команду, если нужно
    except Exception as e:
        tkinter.messagebox.ERROR(
            "Ошибка при запуске Freeform: File is missing or incorect call. Try re-installing app. If error is happens, open app 'Apple support' and leave problem description ")


def calculate_window():
    import subprocess

    try:
        subprocess.run(["python",
                        "C:/Users/Andrew/PycharmProjects/pythonProject1/xgf.py"])  # Замените "python3" на "python" или другую команду, если нужно

    except Exception as e:
        tkinter.messagebox.ERROR("Ошибка при запуске .py:", str(e))


# Создаем `Frame` для размещения двух иконок
icons_frame = Frame(root)
icons_frame.pack(side='bottom', pady=100)

icon_image13 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_commands.jpg')
resized13 = icon_image13.resize((50, 50))
resize13 = icon_image13.resize((50, 50))
icon13 = ImageTk.PhotoImage(resized13)

icon_image12 = Image.open('C:/Users/Andrew/PycharmProjects/photos/py_python.png')
resized12 = icon_image12.resize((50, 50))
resize12 = icon_image12.resize((50, 50))
icon12 = ImageTk.PhotoImage(resized12)

icon_image11 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_freeform.jpg')
resized11 = icon_image11.resize((50, 50))
resize11 = icon_image11.resize((50, 50))
icon11 = ImageTk.PhotoImage(resized11)

icon_image10 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_store.png')
resized10 = icon_image10.resize((50, 50))
resize10 = icon_image10.resize((50, 50))
icon10 = ImageTk.PhotoImage(resized10)

icon_image9 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_clock.png')
resized9 = icon_image9.resize((50, 50))
resize9 = icon_image9.resize((50, 50))
icon9 = ImageTk.PhotoImage(resized9)

icon_image8 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_files.png')
resized8 = icon_image8.resize((50, 50))
resize8 = icon_image8.resize((50, 50))
icon8 = ImageTk.PhotoImage(resized8)

icon_image7 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_player.png')
resized7 = icon_image7.resize((50, 50))
resized7 = icon_image7.resize((50, 50))
icon7 = ImageTk.PhotoImage(resized7)

icon_image6 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_calendar.png')
resized6 = icon_image6.resize((50, 50))
resized6 = icon_image6.resize((50, 50))
icon6 = ImageTk.PhotoImage(resized6)

icon_image5 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_notes.png')
resized5 = icon_image5.resize((50, 50))
resized5 = icon_image5.resize((50, 50))
icon5 = ImageTk.PhotoImage(resized5)

icon_image4 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_voice.png')
resized4 = icon_image4.resize((50, 50))
resized4 = icon_image4.resize((50, 50))
icon4 = ImageTk.PhotoImage(resized4)

icon_image3 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_calculator.png')
resized3 = icon_image3.resize((50, 50))
resized3 = icon_image3.resize((50, 50))
icon3 = ImageTk.PhotoImage(resized3)

icon_image2 = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_photo.png')
resized2 = icon_image2.resize((50, 50))
resized2 = icon_image2.resize((50, 50))
icon2 = ImageTk.PhotoImage(resized2)

icon_image = Image.open('C:/Users/Andrew/PycharmProjects/photos/a_camera.png')
resized = icon_image.resize((50, 50))
resized = icon_image.resize((50, 50))
icon = ImageTk.PhotoImage(resized)

# Создаем кнопки и добавляем их в `icons_frame`
open_calcul_button = Button(icons_frame, image=icon3, command=calculate_window)
view_photos_button = Button(icons_frame, image=icon2, command=create_photo_viewer)
open_camera_button = Button(icons_frame, image=icon, command=create_camera_window)
open_notes_button = Button(icons_frame, image=icon5, command=create_notes_window)
open_calendar_button = Button(icons_frame, image=icon6, command=create_calendar_window)
open_player_button = Button(icons_frame, image=icon7, command=create_music_player)
open_files_button = Button(icons_frame, image=icon8, command=create_file_explorer)
open_clock_button = Button(icons_frame, image=icon9, command=create_clock_window)
open_store_button = Button(icons_frame, image=icon10, command=app_store_window)
open_paint_button = Button(icons_frame, image=icon11, command=run_paint)
open_python_button = Button(icons_frame, image=icon12, command=create_python_window)
open_p_app1_button = Button(icons_frame, image=icon13, command=create_personal_app)

open_store_button.pack(side='left', padx=1)
open_clock_button.pack(side='left', padx=1)
open_files_button.pack(side='left', padx=1)
open_player_button.pack(side='left', padx=1)
open_calendar_button.pack(side='left', padx=1)
open_notes_button.pack(side='left', padx=1)
open_calcul_button.pack(side='left', padx=1)
view_photos_button.pack(side='left', padx=1)  # Отступ между кнопками
open_camera_button.pack(side='left')


def open_help():
    webbrowser.open('https://support.apple.com/uk-ua/mac')


def search():
    google_url = 'https://www.google.com/search?q='
    webbrowser.open(google_url)


def power_off():
    subprocess.run('shutdown.exe' '/h')


menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label="Apple", menu=file_menu, font=("Arial", 30))
file_menu.add_separator()
file_menu.add_command(label="Shutdown", command=root.destroy, font=("Arial", 20))
file_menu.add_command(label="Sleep", command=root.withdraw, font=("Arial", 20))
file_menu.add_command(label="Power off", command=power_off, font=("Arial", 20))

help_menu = Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=open_help)

search_menu = Menu(menu)
menu.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Search", command=search)

keyboard.add_hotkey('alt+r', root.deiconify)
keyboard.add_hotkey('ctrl+alt', root.destroy)
keyboard.add_hotkey('ctrl+p', create_camera_window)


def update_time():
    current_time = datetime.now().strftime("%H:%M")
    label_time.config(text=current_time)
    label_time.after(1000, update_time)


label_time = Label(root, text="time", font=("Arial", 40))
label_time.pack()

update_time()
root.mainloop()
