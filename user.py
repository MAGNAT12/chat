import json
import requests
import sqlite3
import secrets
import string

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

headers = {'Content-Type': 'application/json'}

def register(name, gmail, password):
    data = {
        "name": name,
        "gmail": gmail,
        "password": password,
    }
    response = requests.post("https://magnatri.pythonanywhere.com/api/regist", data=json.dumps(data), headers=headers)
    print(response.json())

def profil(name, gmail, password):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(10))
    cursor.execute("SELECT name FROM users WHERE token = ?", (token,))
    data = cursor.fetchone()
    if data is not None:
        cursor.execute("INSERT INTO users(name, token) VALUES (?, ?)", (name, token))
        connect.commit()
    else:
        pass
    data = {
        "name": name,
        "gmail": gmail,
        "password": password,
        "token": token
    }
    response = requests.post("https://magnatri.pythonanywhere.com/api/user", data=json.dumps(data), headers=headers)
    print(response.json())

def message(name, messages):
    cursor.execute("SELECT name FROM users")
    name_sender = cursor.fetchall()
    cursor.execute("SELECT token FROM users")
    token = cursor.fetchall()
    date = {
        "name_sender":name_sender,
        "name":name,
        "message":messages,
        "token": token
    }
    respons = requests.post("https://magnatri.pythonanywhere.com/api/send_message", data=json.dumps(date), headers=headers)
    if respons.status_code == 200:
        cursor.execute("INSERT INTO send_message(name, messages) VALUES (?, ?)", (name, messages))
        connect.commit()
        print("Сообщение отправелено")
    else:
        print(f"Ошибка: {respons.status_code}")

def get():
    cursor.execute("SELECT token FROM users")
    token = cursor.fetchone()
    print(token)
    date = {
        "token":token
    }
    respons = requests.get(f"https://magnatri.pythonanywhere.com/api/get_messages", data = json.dumps(date), headers=headers)
    print(respons.json())

def send_all_message():
    cursor.execute("SELECT * FROM send_message")
    messages = cursor.fetchall()
    for message in messages:
        print(f"name: {message[0]}, message:{message[1]}")

def get_all_messages():
    cursor.execute("SELECT * FROM get_message")
    messages = cursor.fetchall()
    for message in messages:
        print(f"name: {message[0]} message:{message[1]},")

if __name__ == "__main__":
    token = None
    while True:
        print("1. Зарегистрироваться")
        print("2. Вход")
        print("3. Отправить сообщение")
        print("4. Для получения сообщений")
        print("5. Посмотреть все отправленные сообщения")
        print("6. Посмотреть все полученные сообщения")
        print("7. Выход")
        choice = input("Выберите: ")
        if choice == "1":
            name = input("Введите имя: ")
            gmail = input("Введите gmail: ")
            password = input("Введите пароль: ")
            register(name, gmail, password)
            print("---------------")
        elif choice == "2":
            name = input("Введите имя: ")
            gmail = input("Введите gmail: ")
            password = input("Введите пароль: ")
            profil(name, gmail, password)
            print("---------------")
        elif choice == "3":
            recipient_name = input("Введите имя кому хотите отправить сообщение: ")
            message_text = input("Введите сообщение которое хотите отправить: ")
            message(recipient_name, message_text)
            print("---------------")
        elif choice == "4":
            get()
            print("---------------")
        elif choice == "5":
            send_all_message()
            print("---------------")
        elif choice == "6":
            get_all_messages()
            print("---------------")
        elif choice == "7":
            break


