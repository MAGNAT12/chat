import flet as ft
import sqlite3
import requests
import json

connect = sqlite3.connect("user.db", check_same_thread=False)
cursor = connect.cursor()

headers = {"Content-Type": "application/json"}


def chat_main(page: ft.Page):
    page.title = "Chat"
    page.theme_mode = "system"

    # Fetch user details
    cursor.execute("SELECT name, token FROM users")
    user = cursor.fetchone()
    if not user:
        page.controls.clear()
        page.add(ft.Text("User not found. Please register first."))
        return

    name_sender, token = user
    message_field = ft.TextField(label="Message", expand=True)

    def send_message(e):
        message = message_field.value.strip()
        if not message:
            return

        data = {
            "name_sender": name_sender,
            "name": "addf",
            "message": message,
            "token": token,
        }

        try:
            response = requests.post(
                "https://magnatri.pythonanywhere.com/api/send_message",
                data=json.dumps(data),
                headers=headers,
            )
            if response.status_code == 200:
                cursor.execute("INSERT INTO send_message(name, messages) VALUES (?, ?)", (name_sender, message))
                connect.commit()
            else:
                print(f"Error: {response.json()}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")

    send_button = ft.ElevatedButton(text="Send", icon=ft.icons.SEND, on_click=send_message)
    input_row = ft.Row([message_field, send_button], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Column(
            [ft.Text("Chat Application", size=20), ft.Container(expand=True), input_row],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.update()
