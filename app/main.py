import flet as ft
import sqlite3
import requests
import string
import secrets
from message import chat_main


connect = sqlite3.connect("user.db", check_same_thread=False)
cursor = connect.cursor()
cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    token TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS send_message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    messages TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(name) REFERENCES users(name)
);

CREATE TABLE IF NOT EXISTS get_message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    messages TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(name) REFERENCES users(name)
);
""")

connect.commit()

headers = {"Content-Type": "application/json"}


def main(page: ft.Page):
    page.title = "Chat"
    page.theme_mode = "system"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    result = ft.Text()

    cursor.execute("SELECT name FROM users")
    user = cursor.fetchone()

    if user:
        chat_main(page)
    else:

        def register(e):
            data = {
                "name": Name.value,
                "gmail": Gmail.value,
                "password": Password.value,
            }
            try:
                response = requests.post(
                    "http://192.168.1.104:3000/api/regist",
                    json=data,
                    headers=headers,
                )
                if response.status_code == 200:
                    token = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
                    data = {
                        "name": Name.value,
                        "gmail": Gmail.value,
                        "password": Password.value,
                        "token": token
                    }
                    response = requests.post(
                    "http://192.168.1.104:3000/api/user",
                    json=data,
                    headers=headers
                    )
                    if response.status_code == 200:
                        cursor.execute("INSERT INTO users(name, token) VALUES (?, ?)", (Name.value, token))
                        connect.commit()
                        a = response.json()
                        print(a['message'])
                        chat_main(page)

                    else:
                        print(a['message'])

                else:
                    result.value = response.json().get("message", "Registration failed.")

            except requests.RequestException as e:
                result.value = f"Error: {e}"

            page.update()

        Name = ft.TextField(label="Name", width=300)
        Gmail = ft.TextField(label="Gmail", width=300)
        Password = ft.TextField(label="Password", width=300, password=True)
        register_button = ft.ElevatedButton(text="Register", on_click=register)

        page.add(
            ft.Column(
                [Name, Gmail, Password, register_button, result],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

ft.app(target=main)
