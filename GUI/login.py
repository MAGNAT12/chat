import string
import secrets
import requests
import sqlite3
import json
from tkinter import *
import asyncio


headers = {'Content-Type': 'application/json'}

def login():
    root = Tk()
    root.geometry("500x500")
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
        asyncio.create_task(profil(name, gmail, password))

    name_entry = Entry(root, width=25)
    name_entry.pack(pady=5)

    gmail_entry = Entry(root, width=25)
    gmail_entry.pack(pady=5)

    password_entry = Entry(root, width=25)
    password_entry.pack(pady=5)

    inpu = Button(root, text="Вход", font=('Times', 12), command=name_gmail_pass)
    inpu.pack(pady=5)

    async def profil(name, gmail, password):
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(10))
        cursor.execute("SELECT name FROM users WHERE token = ?", (token,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute("INSERT INTO users(name, token) VALUES (?, ?)", (name, token))
            connect.commit()

        data = {
            "name": name,
            "gmail": gmail,
            "password": password,
            "token": token
        }
        response = requests.post("http://127.0.0.1:3000/api/user", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            root.after(10, lambda: asyncio.create_task(profile()))

        if response.status_code == 400:
            a = response.json()
            user_name_label = Label(root, text=a["message"], font=('fixed', 10))
            user_name_label.pack(pady=6)
            root.after(2000, lambda: user_name_label.config(text=""))

    async def profile():
        root.destroy()
        from GUI.profil import profil
        profil()

    root.mainloop()
