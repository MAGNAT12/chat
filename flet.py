import flet as fl
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

def main(page: fl.Page):
    page.title = "Регистрация"
    page.horizontal_alignment = fl.CrossAxisAlignment.CENTER
    page.vertical_alignment = fl.MainAxisAlignment.CENTER

    name_entry = fl.TextField(label="Имя", width=300)
    gmail_entry = fl.TextField(label="Gmail", width=300)
    password_entry = fl.TextField(label="Пароль", width=300, password=True)

    def regist(e):
        name = name_entry.value
        gmail = gmail_entry.value
        password = password_entry.value
        data = {
            "name": name,
            "gmail": gmail,
            "password": password,
        }
        response = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            user_name_label.value = "Вы зарегистрированы"
        elif response.status_code == 400:
            user_name_label.value = "Пользователь уже существует"
        page.update()

    user_name_label = fl.Text(value="", color=fl.colors.GREEN)

    submit_button = fl.ElevatedButton(text="Зарегистрироваться", on_click=regist)

    page.add(
        fl.Column(
            [
                name_entry,
                gmail_entry,
                password_entry,
                submit_button,
                user_name_label,
            ],
            alignment=fl.MainAxisAlignment.CENTER,
            horizontal_alignment=fl.CrossAxisAlignment.CENTER,
        )
    )

fl.app(target=main, view=fl.WEB_BROWSER)

#, view=fl.WEB_BROWSER