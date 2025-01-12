import flet as ft
import sqlite3
import requests
import json

# Подключение к базе данных
connect = sqlite3.connect("user.db", check_same_thread=False)
cursor = connect.cursor()

# Заголовки для API-запросов
headers = {"Content-Type": "application/json"}

def chat_main(page: ft.Page):
    page.title = "Chat"
    page.theme_mode = "system"

    # Проверка наличия пользователя
    cursor.execute("SELECT name, token FROM users")
    user = cursor.fetchone()

    if not user:
        page.controls.clear()
        page.add(ft.Text("User not found. Please register first."))
        page.update()
        return

    name_sender, token = user
    message_field = ft.TextField(label="Message", expand=True)

    # Список для отображения чата
    chat_view = ft.ListView(
        expand=True, 
        spacing=10, 
        reverse=True  # Сообщения снизу вверх
    )

    # Подгрузка сообщений (оба собеседника)
    def load_messages():
        chat_view.controls.clear()
        cursor.execute("SELECT name, messages FROM send_message ORDER BY id DESC")
        messages = cursor.fetchall()

        for sender, message in messages:
            if sender == name_sender:
                alignment = ft.alignment.center_right
                color = ft.colors.BLUE
            else:
                alignment = ft.alignment.center_left
                color = ft.colors.GREEN

            chat_view.controls.append(
                ft.Container(
                    content=ft.Text(f"{sender}: {message}"),
                    alignment=alignment,
                    bgcolor=color,
                    padding=10,
                    border_radius=10,
                )
            )
        page.update()

    load_messages()  # Загрузка существующих сообщений

    # Отправка сообщения
    def send_message(e):
        message = message_field.value.strip()

        if not message:
            return

        data = {
            "name_sender": name_sender,
            "name": "asd",  # Укажите имя получателя
            "message": message,
            "token": token,
        }

        try:
            response = requests.post(
                "http://127.0.0.1:3000/api/send_message",
                data=json.dumps(data),
                headers=headers,
            )

            if response.status_code == 200:
                # Сохраняем сообщение в базе данных
                cursor.execute("INSERT INTO send_message(name, messages) VALUES (?, ?)", (name_sender, message))
                connect.commit()

                # Обновляем список сообщений
                load_messages()
                message_field.value = ""
                page.update()

            else:
                chat_view.controls.append(ft.Text(f"Error: {response.json().get('error', 'Unknown error')}", color=ft.colors.RED))
                page.update()

        except requests.RequestException as ex:
            chat_view.controls.append(ft.Text(f"Request failed: {ex}", color=ft.colors.RED))
            page.update()

    # Элементы интерфейса
    send_button = ft.ElevatedButton(text="Send", icon=ft.icons.SEND, on_click=send_message)
    input_row = ft.Row([message_field, send_button], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Column(
            [
                chat_view,
                input_row,
            ],
            expand=True,
        )
    )
    page.update()
