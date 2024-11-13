import flet as ft
import requests
import sqlite3
import string
import secrets

connect = sqlite3.connect('user.db', check_same_thread=False)
cursor = connect.cursor()

# Создание таблиц, если они не существуют
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

def main(page: ft.Page):
    page.title = "Flet app"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    result = ft.Text()

    cursor.execute("SELECT name FROM users")
    name_sender = cursor.fetchall()

    if name_sender:
        page.controls.clear()
        result.value = f"Зарегистрированные пользователи: {name_sender[0]}"
        page.add(result)
        page.update()

    else:
        def register(e):
            data = {
                "name": Name.value,
                "gmail": Gmail.value,
                "password": Password.value
            }

            response = requests.post("https://magnatri.pythonanywhere.com/api/regist", json=data, headers=headers)
            if response.status_code == 200:
                alphabet = string.ascii_letters + string.digits
                token = ''.join(secrets.choice(alphabet) for _ in range(10))

                cursor.execute("SELECT name FROM users WHERE token = ?", (token,))
                data = cursor.fetchone()

                if data is None:
                    cursor.execute("INSERT INTO users(name, token) VALUES (?, ?)", (Name.value, token))
                    connect.commit()

                data = {
                    "name": Name.value,
                    "gmail": Gmail.value,
                    "password": Password.value,
                    "token": token
                }
                response = requests.post("https://magnatri.pythonanywhere.com/api/user", json=data, headers=headers)
                mes = response.json()
                result.value = mes['message']

                if response.status_code == 200:
                    page.controls.clear()
                    result.value = "Регистрация успешна!"
                    page.add(result)
                    page.update()

            page.update()

        Name = ft.TextField(label='Name', width=300)
        Gmail = ft.TextField(label='Gmail', width=300)
        Password = ft.TextField(label='Password', width=300)
        but = ft.ElevatedButton(text='Регистрация', on_click=register)
        result = ft.Text()

        page.add(
            ft.Column(
                [
                    Name,
                    Gmail,
                    Password,
                    but,
                    result
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

ft.app(target=main)
