#!/usr/bin/python3

from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame
import subject
import description
import subprocess

def is_redos_installed():
    try:
        # Вызываем команду flatpak list для получения списка установленных приложений
        output = subprocess.check_output(["flatpak","list"])
        print("Проверка репозиториев")
        subprocess.check_output(["sudo","flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"])
        subprocess.check_output(["sudo","flatpak", "remote-add", "--if-not-exists", "gnome-nightly", "https://nightly.gnome.org/gnome-nightly.flatpakrepo"])
        subprocess.check_output(["sudo","flatpak", "remote-add", "--if-not-exists", "kdeapps", "--from", "https://distribute.kde.org/kdeapps.flatpakrepo"])
        # Ищем строку с именем redos в выводе команды
        return True
    except:
        return False

if is_redos_installed():
    print("Flatpak redos уже установлен.")
    path = str(subprocess.check_output(["pwd"])[:-1])[2:-1]
else:
    print("Flatpak redos не установлен.")
    print("Начинается установка")
    try:
        subprocess.check_output(["sudo", "dnf", "install", "-y", "flatpak"])
        is_redos_installed()
    except:
        print("Ошибка, установите flatpak вручную")
        exit()
class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.title("EduApps")
        toplevel1.configure(height=480, width=720)
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=200, width=200)
        ########
        row = 0
        for el in subject.dict:
            buttondisc = ttk.Button(frame1)
            buttondisc.configure(text=el, padding=10)
            buttondisc.configure(text=el, command=lambda i=el: self.frame2build(i))
            buttondisc.grid(column=0, row=row)
            row +=1
        #######
        frame1.place(
            anchor="nw",
            relheight=1.0,
            relwidth=0.2,
            relx=0.0,
            x=0,
            y=0)
        separator1 = ttk.Separator(toplevel1)
        separator1.configure(orient="vertical")
        separator1.place(
            anchor="nw",
            relheight=1.0,
            relwidth=0.0,
            relx=0.2,
            x=0)
        separator2 = ttk.Separator(toplevel1)
        separator2.configure(orient="vertical")
        separator2.place(
            anchor="nw",
            relheight=1.0,
            relwidth=0.0,
            relx=0.5,
            x=0)
        # Main widget
        self.mainwindow = toplevel1

    def frame2build(self, disc):
        frame2 = ttk.Frame(self.mainwindow)
        frame2.configure(height=200, width=200)
        scrolledframe2 = ScrolledFrame(frame2, scrolltype="vertical")
        scrolledframe2.configure(usemousewheel=True)
        #####################
        row = 0
        for elb in subject.dict.get(disc):
            button = ttk.Button(scrolledframe2.innerframe)
            button.configure(text=elb, command=lambda i=elb: self.frame3build(i))
            button.pack()
            row += 1
        #####################
        scrolledframe2.pack(anchor="n", fill="both", ipady=150, side="top")
        scrolledframe2.bind("<Activate>", self.callback, add="")
        separator1 = ttk.Separator(self.mainwindow)
        separator1.configure(orient="vertical")
        separator1.place(
            anchor="nw",
            relheight=1.0,
            relwidth=0.0,
            relx=0.2,
            x=0)
        frame2.place(
            anchor="nw",
            relheight=1.0,
            relwidth=0.3,
            relx=0.2,
            x=0,
            y=0)
        self.run()

    def install_packages(self, program):
        if description.dict.get(program).get("repo") == "redos":
            # Устанавливаем выбранные пакеты ПО с помощью apt-get
            subprocess.run(['sudo', 'dnf', 'install', "-y", description.dict.get(program).get("command")])
            print(str(['sudo', 'dnf', 'install', "-y", description.dict.get(program).get("command")]))
            print("Установка завершена", "Пакеты ПО были успешно установлены.")
        elif description.dict.get(program).get("repo") == "fp":
            subprocess.run(['sudo', 'flatpak', 'install', '-y', description.dict.get(program).get("command")])
            subprocess.run(["ls"])
            print("Установка завершена", "Пакеты ПО были успешно установлены.")

    def frame3build(self, program):
        frame3 = ttk.Frame(self.mainwindow)
        frame3.configure(height=200, width=200)
        self.labelframe3 = ttk.Label(frame3)
        self.labelframe3.configure(text=program, padding=10)
        self.labelframe3.pack(side="top")
        text1 = tk.Text(frame3)
        text1.configure(height=10, state="disabled", width=50)
        _text_ = description.dict.get(program).get("description")
        text1.configure(state="normal")
        text1.insert("0.0", _text_)
        text1.configure(state="disabled")
        text1.pack(ipady=10, pady=10, side="top")
        images = ttk.Frame(frame3)
        images.configure()
        image1 = Image.open(path + "/GUI/images/" +description.dict.get(program).get("images")[0])
        scaled_image1 = image1.resize((100, 100))
        image1 = ImageTk.PhotoImage(scaled_image1)
        Label(images, image=image1).pack(side="left", padx=10)
        image2 = Image.open(path + "/GUI/images/" +description.dict.get(program).get("images")[1])
        scaled_image2 = image2.resize((100, 100))
        image2 = ImageTk.PhotoImage(scaled_image2)
        Label(images, image=image2).pack(side="left", padx=10)
        image3 = Image.open(path + "/GUI/images/" +description.dict.get(program).get("images")[2])
        scaled_image3 = image3.resize((100, 100))
        image3 = ImageTk.PhotoImage(scaled_image3)
        Label(images, image=image3).pack(side="left", padx=10)
        images.pack()
        install_button = ttk.Button(frame3, text="Установить", command=lambda i=program: self.install_packages(i))
        install_button.pack(side="top",pady=30)
        separator2 = ttk.Separator(self.mainwindow)
        separator2.configure(orient="vertical")
        separator2.place(
            anchor="nw",
            relheight=1.0,
            relwidth=0.0,
            relx=0.5,
            x=0)
        frame3.place(
            anchor="ne",
            relheight=1.0,
            relwidth=0.5,
            relx=1.0,
            x=0,
            y=0)
        frame3.mainloop()
        self.run()

    def run(self):
        self.mainwindow.mainloop()

    def callback(self, event=None):
        pass


if __name__ == "__main__":

    app = NewprojectApp()
    app.run()
