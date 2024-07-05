from tkinter import *
import json
import requests
import platform
import sqlite3

headers = {'Content-Type': 'application/json'}
name_devices = platform.node()
connect = sqlite3.connect('user.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS 
            users(
               name TEXT,
               name_devices TEXT
               )""")
connect.commit()

win = Tk()
win.geometry("500x500")

def name_gmail_pass():
   name = name_entry.get()
   gmail = gmail_entry.get()
   password = password_entry.get()
   regist(name, gmail, password)


name_entry = Entry(win, width=25)
name_entry.pack(pady=5)

gmail_entry = Entry(win, width=25)
gmail_entry.pack(pady=5)

password_entry = Entry(win, width=25)
password_entry.pack(pady=5)

inpu = Button(win, text="Зарегистрироваться", font=('Times', 12) ,command=lambda: name_gmail_pass())
inpu.pack(pady=5)

win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_columnconfigure(3, minsize=80)
win.grid_columnconfigure(4, minsize=80)
win.grid_columnconfigure(5, minsize=80)
win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=30)
win.grid_rowconfigure(4, minsize=30)
win.grid_rowconfigure(5, minsize=30)

def regist(name, gmail, password):
   date = {
        "name":name,
        "gmail":gmail,
        "password":password,
        }
   respons = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(date), headers=headers)
   if respons.status_code == 200:
      user_name_label = Label(win, text="Вы зарегистрированны", font=('fixed', 10))
      user_name_label.pack(pady=5)
      win.after(2000, lambda: user_name_label.config(text=""))
   elif respons.status_code == 400:
      user_name_label = Label(win, text="Пользователь уже существует", font=('fixed', 10))
      user_name_label.pack(pady=5)
      win.after(2000, lambda: user_name_label.config(text=""))




win.mainloop()