import flet as ft
import sqlite3
import requests
import string
import secrets
from chat import chat_main

# Database connection
connect = sqlite3.connect("user.db", check_same_thread=False)
cursor = connect.cursor()

# Create tables if they don't exist
cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    token TEXT
);
CREATE TABLE IF NOT EXISTS send_message (
    name TEXT,
    messages TEXT
);
CREATE TABLE IF NOT EXISTS get_message (
    name TEXT,
    messages TEXT
);
""")
connect.commit()

headers = {"Content-Type": "application/json"}


def main(page: ft.Page):
    page.title = "Chat"
    page.theme_mode = "system"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    result = ft.Text()

    # Check if user is already registered
    cursor.execute("SELECT name FROM users")
    user = cursor.fetchone()

    if user:
        chat_main(page)  # Redirect to chat interface
    else:
        # Registration Form
        def register(e):
            data = {
                "name": Name.value,
                "gmail": Gmail.value,
                "password": Password.value,
            }
            try:
                response = requests.post(
                    "https://magnatri.pythonanywhere.com/api/regist",
                    json=data,
                    headers=headers,
                )
                if response.status_code == 200:
                    token = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
                    cursor.execute("INSERT INTO users(name, token) VALUES (?, ?)", (Name.value, token))
                    connect.commit()
                    chat_main(page)  # Redirect to chat interface
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
