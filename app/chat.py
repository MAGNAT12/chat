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

    cursor.execute("SELECT name, token FROM users")
    user = cursor.fetchone()

    if not user:
        page.controls.clear()
        page.add(ft.Text("User not found. Please register first."))
        return

    search_field = ft.TextField(label="Search User", 
    expand=True)
    search_results = ft.Column()

    def search_users(e):
        query = search_field.value.strip()

        response = requests.post(
        "http://127.0.0.1:3000/api/search",
        json={"name":query}, 
        headers=headers)

        if response.status_code == 200:

            results = response.json().get("users", [])
            search_results.controls.clear()

            for user in results:
                search_results.controls.append(ft.Button(user['name']))
            page.update()

        else:
            search_results.controls.clear()
            search_results.controls.append(ft.Text("No users found"))
            page.update()

    search_field.on_change = search_users

    page.add(
        ft.Column(
            [
                search_field,
                search_results,
                ft.Container(expand=True),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.update()
