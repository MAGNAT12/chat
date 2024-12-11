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
        "name":"addf",
        "gmail":"asddf",
        "password":"adf"
    }

    respons = requests.post("https://magnatri.pythonanywhere.com/api/regist", data=json.dumps(date), headers=headers)
    print(respons.json())


def message():
    date = {
        "name_sender":"asd",
        "name":"dfg",
        "message":"привет",
        "token":"VCYVakoIT0"
    }
    respons = requests.post("https://magnatri.pythonanywhere.com/api/send_message", data=json.dumps(date), headers=headers)
    print(respons.json())

def get():
    date = {
    }
    respons = requests.get(f"https://magnatri.pythonanywhere.com/api/get_messages", data = json.dumps(date), headers=headers)
    print(respons.json())


def profil():
    date = {
        "name":"2",
        "gmail":"2",
        "password":"2",
        "token": None
    }
    respons = requests.post("https://magnatri.pythonanywhere.com/api/user", data=json.dumps(date), headers=headers)
    print(respons.json())
    print(token)

regist()