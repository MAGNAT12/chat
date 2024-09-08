from tkinter import *
import json
import requests
import hashlib
import asyncio
import sqlite3
import string
import secrets

win = Tk()
win.geometry("500x500")

headers = {'Content-Type': 'application/json'}

connect = sqlite3.connect('user.db', check_same_thread=False)

cursor = connect.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        token TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS send_message(
        name TEXT,
        messages TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS get_message(
        name TEXT,
        messages TEXT
    )
""")

connect.commit()

def name_gmail_pass():
    name = name_entry.get()
    gmail = gmail_entry.get()
    password = password_entry.get()
    regist(name, gmail, password)

name_entry = Entry(win, width=30)
name_entry.pack(pady=6, padx=5)

gmail_entry = Entry(win, width=30)
gmail_entry.pack(pady=7, padx=7)

password_entry = Entry(win, width=30)
password_entry.pack(pady=9, padx=9)

inpu = Button(win, text="Зарегистрироваться", font=('Times', 12), command=lambda: name_gmail_pass())
inpu.pack(pady=11)

async def login_a():
    win.destroy()
    await asyncio.sleep(0.02)
    from login import login
    login()

login_b = Button(win, text="Вход", font=('Times', 12), command=lambda: asyncio.run(login_a()))
login_b.place(x=470, y=10, anchor='ne')

def regist(name, gmail, password):
    password_ha = hashlib.sha3_512(password.encode()).hexdigest()
    date = {
            "name":name,
            "gmail":gmail,
            "password":password_ha,
            }
    respons = requests.post("https://magnatri.pythonanywhere.com/api/regist", data=json.dumps(date), headers=headers)

    if respons.status_code == 200:
        user_name_label = Label(win, text="Вы зарегистрированны", font=('fixed', 10))
        user_name_label.pack(pady=5)
        win.after(2000, lambda: user_name_label.config(text=""))

        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(10))
        cursor.execute("SELECT name FROM users WHERE token = ?", (token,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute("INSERT INTO users(name, token) VALUES (?, ?)", (name, token))
            connect.commit()
        else:
            pass
        data = {
            "name": name,
            "gmail": gmail,
            "password": password_ha,
            "token": token
        }
        response = requests.post("https://magnatri.pythonanywhere.com/api/user", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            async def profile():
                win.destroy()
                await asyncio.sleep(0.02)
                from profil import profil
                profil()
            
            asyncio.run(profile())

        else:
            user_name_label = Label(win, text="Такой пользователь уже существует", font=('fixed', 10))
            user_name_label.pack(pady=6)

        
      
    elif respons.status_code == 400:
        user_name_label = Label(win, text="Такой пользователь уже существует", font=('fixed', 10))
        user_name_label.pack(pady=6)
        win.after(2000, lambda: user_name_label.config(text=""))

win.mainloop()
