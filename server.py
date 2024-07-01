from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import sqlite3
import threading
import time
import hashlib

app = Flask(__name__)
api = Api(app)
token = ''
list_token = ('1234567890')
connect = sqlite3.connect('Chat.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS 
            users(
               id INTEGER PRIMARY KEY,
               name TEXT,
               gmail TEXT,
               password TEXT
            )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS
               mes(
               name_sender TEXT,
               name TEXT,
               message TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS
               devices(
               name TEXT,
               name_devices TEXT
               )""")

cursor.execute('PRAGMA journal_mode = OFF')
connect.commit()

class Name_gmail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument('gmail', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        name = args["name"]
        gmail = args['gmail']
        cursor.execute(f"SELECT `name`, `gmail` FROM `users` WHERE `name` = '{name}' AND `gmail` = '{gmail}'")
        data = cursor.fetchone()
        if data is None:
            name = args["name"]
            gmail = args['gmail']
            password = args['password']
            password_ha = hashlib.sha3_512(password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (name, gmail, password) VALUES (?, ?, ?);", (name, gmail, password_ha))
            connect.commit()
            return {'message': 'Вы зарегистрированны'}
        else:
            return {'message': 'Ник уже зарегистрированн'}
        
class Send_message(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("message", type=str)
        parser.add_argument("name_devices", type=str)
        args = parser.parse_args()
        name = args["name"]
        name_devices = args['name_devices']
        cursor.execute(f"SELECT `name` FROM `users` WHERE `name` = '{name}'")
        data = cursor.fetchone()
        if data:
            cursor.execute(f"SELECT `name_devices` FROM devices WHERE `name_devices` = '{name_devices}'")
            data = cursor.fetchone()
            if data:
                name = args["name"]
                message = args["message"]
                cursor.execute('SELECT name FROM devices WHERE `name_devices` = ?', (name_devices,))
                name_sender = cursor.fetchone()
                name_sender = name_sender[0]
                cursor.execute(
                "INSERT INTO mes(name_sender, name, message, timestamp) VALUES(?, ?, ?, datetime('now'));",
                (name_sender, name, message)
                            )
                connect.commit()
                connect.close()
                return {'message': 'сообщение отправлено'}
            else:
                return {"message":"Вы не вошли в профель"}
        else:
            return {'message': "НЕ найде пользователь"}

class Get_messages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name_devices", type=str)
        args = parser.parse_args()
        name_devices = args['name_devices']
        cursor.execute(f"SELECT `name_devices` FROM devices WHERE `name_devices` = '{name_devices}'")
        data = cursor.fetchone()
        if data:
            cursor.execute('SELECT name FROM devices WHERE `name_devices` = ?', (name_devices,))
            name_sender = cursor.fetchone()
            name_sender = name_sender[0]
            cursor.execute("SELECT name_sender, message, timestamp FROM mes WHERE name = ?", (name_sender,))
            messages = cursor.fetchall()
            if messages:
                messages_list = [{'name_sender': msg[0], 'message': msg[1]} for msg in messages]
                return jsonify(messages_list)
            else:
                return {'message': 'Сообщений не найдено'}
        else:
            connect.close()
            return {"message": "Зарегистрируйтесь"}

        
class Profil_user(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument('gmail', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument("name_devices", type=str)
        args = parser.parse_args()
        name = args["name"]
        gmail = args["gmail"]
        password = args['password']
        name_devices = args['name_devices']
        password_ha = hashlib.sha3_512(password.encode()).hexdigest()
        cursor.execute("SELECT name, gmail, password FROM users WHERE name = ? AND gmail = ? AND password = ?", (name, gmail, password_ha))
        data = cursor.fetchone()
        if name in data:
            cursor.execute("SELECT name_devices FROM devices WHERE `name_devices` = ?", (name_devices,))
            data = cursor.fetchone()
            if data is None:
                cursor.execute('INSERT INTO devices (name_devices, name) VALUES (?, ?)', (name_devices, name))
                connect.commit()
                return {"message":"Вы вошли в профиль"}
            else:
                return {"message":"Вы уже вошли в провель"}
        else:
            return {"message":"Зарегистрируйтесь"}


api.add_resource(Name_gmail, "/api/regist")
api.add_resource(Send_message, "/api/send_message")
api.add_resource(Get_messages, "/api/get_messages")
api.add_resource(Profil_user, "/api/user")

def delete_old_messages():
    while True:
        cursor.execute("DELETE FROM mes WHERE timestamp <= datetime('now', '-2 hours')")
        connect.commit()
        time.sleep(3600)

thread = threading.Thread(target=delete_old_messages, daemon=True)
thread.start()

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
