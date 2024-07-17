import json
import requests
import sqlite3
import secrets
import string

alphabet = string.ascii_letters + string.digits
token = ''.join(secrets.choice(alphabet) for _ in range(10))


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

cursor.execute("""CREATE TABLE IF NOT EXISTS 
            get_message(
               name TEXT,
               messages TEXT
               )""")

connect.commit()

headers = {'Content-Type': 'application/json'}


def register(name, gmail, password):
    date = {
        "name":name,
        "gmail":gmail,
        "password":password,
    }

    respons = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(date), headers=headers)
    print(respons.json())


def profil(name, gmail, password):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(10))
    cursor.execute("SELECT token FROM users WHERE token = ?", (token,))
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO users(name, token) VALUES (?, ?)", (name, token))
    else:
        pass
    connect.commit()
    date = {
        "name":name,
        "gmail":gmail,
        "password":password,
        "token": token
    }
    respons = requests.post("http://127.0.0.1:3000/api/user", data=json.dumps(date), headers=headers)
    print(respons.json())


def message(name, messages):
    cursor.execute("SELECT name FROM users WHERE token = ?", (token,))
    name_sender = cursor.fetchone()
    cursor.execute("SELECT token FROM users WHERE name = ?", (name_sender,))
    token = cursor.fetchone()
    date = {
        "name_sender":name_sender,
        "name":name,
        "message":messages,
        "token": token
    }
    respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
    print(respons.json())


if __name__ == "__main__":
    while True:
        print("1. Зарегистрироваться")
        print("2. Вход")
        print("3. Отправить сообщение")
        print("4. Выход")
        a = input("Выберите: ")
        if a == "1":
            name = input("Ввидите имя: ")
            gmail = input("Ввидете gmail: ")
            password = input("Ввидите пароль: ")
            register(name, gmail, password)
        if a == "2":
            name = input("Ввидите имя: ")
            gmail = input("Ввидете gmail: ")
            password = input("Ввидите пароль: ")
            profil(name, gmail, password)
        if a == "3":
            name = input("Ввидите имя каму хотите отправить сообщение: ")
            messages = input("Ввидите сообщение которое хотите отправить: ")
            message(name, messages)
        if a == "4":
            break