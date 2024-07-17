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

def regist():
    date = {
        "name":"",
        "gmail":"",
        "password":"",
    }

    respons = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(date), headers=headers)
    print(respons.json())


def message():
    date = {
        "name_sender":"Magnat",
        "name":"Azamat",
        "message":"Привет",
        "token": "8oWr3aiFJM"
    }
    respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
    print(respons.json())

def get():
    date = {
    }
    respons = requests.get(f"http://127.0.0.1:3000/api/get_messages", data = json.dumps(date), headers=headers)
    print(respons.json())


def profil():
    date = {
        "name":"Azamat",
        "gmail":"azamat@gmail.com",
        "password":"1234567",
        "token": token
    }
    respons = requests.post("http://127.0.0.1:3000/api/user", data=json.dumps(date), headers=headers)
    print(respons.json())
    print(token)

message()