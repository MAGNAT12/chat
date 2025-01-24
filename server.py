from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3
import threading
import time
import os

app = Flask(__name__)
api = Api(app)
from flask_cors import CORS
CORS(app)

connect = sqlite3.connect('Chat.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS 
            users(
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               gmail TEXT NOT NULL,
               password TEXT NOT NULL
            )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS
               mes(
               name_sender TEXT NOT NULL,
               name TEXT NOT NULL,
               message TEXT NOT NULL,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS
               ton(
               name TEXT NOT NULL,
               token TEXT NOT NULL
               )""")

cursor.execute('PRAGMA journal_mode = OFF')
connect.commit()


journal_file = 'Chat.db-journal'

if os.path.exists(journal_file):
    os.remove(journal_file)

class Name_gmail(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, required=True, help="Name is required")
            parser.add_argument('gmail', type=str, required=True, help="Gmail is required")
            parser.add_argument('password', type=str, required=True, help="Password is required")
            args = parser.parse_args()

            name = args["name"]
            gmail = args['gmail']
            password = args['password']

            cursor.execute("SELECT `name`, `gmail` FROM `users` WHERE `name` = ? AND `gmail` = ?", (name, gmail))
            data = cursor.fetchone()

            if data is None:
                cursor.execute("INSERT INTO users (name, gmail, password) VALUES (?, ?, ?);", (name, gmail, password))
                connect.commit()
                return {'message': 'Вы зарегистрированы'}, 200
            else:
                return {'message': 'Такой пользователь уже существует'}, 400
        except sqlite3.Error as e:
            connect.rollback()
            return {'message': 'Ошибка базы данных', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'Произошла ошибка', 'error': str(e)}, 500

        
class Send_message(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name_sender", type=str, required=True, help="Sender name is required")
            parser.add_argument("name", type=str, required=True, help="Recipient name is required")
            parser.add_argument("message", type=str, required=True, help="Message is required")
            parser.add_argument("token", type=str, required=True, help="Token is required")
            args = parser.parse_args()

            name_sender = args["name_sender"]
            name = args['name']
            message = args['message']
            token = args['token']

            cursor.execute("SELECT name FROM users WHERE `name` = ?", (name,))
            recipient_exists = cursor.fetchone()

            if recipient_exists:
                cursor.execute("SELECT token FROM ton WHERE `token` = ?", (token,))
                token_valid = cursor.fetchone()

                if token_valid:
                    cursor.execute("INSERT INTO mes(name_sender, name, message) VALUES (?, ?, ?);", 
                                   (name_sender, name, message))
                    connect.commit()
                    return {'message': 'Сообщение отправлено'}, 200
                else:
                    return {"message": "Вы не вошли в профиль"}, 400
            else:
                return {'message': "Пользователь не найден"}, 400
        except sqlite3.Error as e:
            connect.rollback()
            return {'message': 'Ошибка базы данных', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'Произошла ошибка', 'error': str(e)}, 500



class Get_messages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str)
        args = parser.parse_args()
        token = args['token']
        cursor.execute('SELECT name FROM ton WHERE `token` = ?', (token,))
        data = cursor.fetchone()
        if data:
            cursor.execute('SELECT name FROM ton WHERE `token` = ?', (token,))
            name_sender = cursor.fetchone()
            name_sender = name_sender[0]
            cursor.execute("SELECT name_sender, message, timestamp FROM mes WHERE name = ?", (name_sender,))
            messages = cursor.fetchall()
            if messages:
                for msg in messages:
                    messages_list = {'name_sender':msg[0], 'message':msg[1]}
                return messages_list
            else:
                return {'message': 'Сообщений не найдено'}, 400
        else:
            return {"message": "Зарегистрируйтесь"}, 400

        
class Profil_user(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("gmail", type=str)
        parser.add_argument("password", type=str)
        parser.add_argument("token", type=str)
        args = parser.parse_args()
        name = args["name"]
        gmail = args["gmail"]
        password = args["password"]
        token = args["token"]

        cursor.execute("SELECT name, gmail, password FROM users WHERE name = ? AND gmail = ? AND password = ?", (name, gmail, password,))
        data = cursor.fetchall()
        if data:
            cursor.execute("SELECT name FROM ton WHERE name = ?", (name,))
            data = cursor.fetchone()
            if data is None:
                cursor.execute("INSERT INTO ton (token, name) VALUES (?, ?)", (token, name))
                connect.commit()
                return {"message": "Вы успешно вошли в аккаунт"}, 200
            else:
                return {"message": "Вы уже вошли в аккаунт"}, 300
        return {"message": "Вы не зарегистрированы"}, 400


class Search(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Поисковый запрос обязателен")
        args = parser.parse_args()

        query = args["name"].lower()
        if query == "":
            return {"message":"Введите име пользователь"}

        else:
            cursor.execute("SELECT name FROM users WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
            results = cursor.fetchall()

            if results:
                users = [{"name": user[0]} for user in results]
                return {"users": users}, 200
            else:
                return {"message": "Пользователи не найдены"}, 404


class Comands(Resource):  
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, required=True, help="Token is required")
        args = parser.parse_args()
        name = args["token"]
        if name == 'd7':
            cursor.execute("SELECT `name` FROM `users`")
            all_user = cursor.fetchall()
            return {"users":all_user}
        
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str)
        parser.add_argument("name", type=str)
        args = parser.parse_args()
        token = args["token"]
        name = args["name"]
        if token == 'd7':
            cursor.execute("SELECT `name` FROM `users` WHERE `name` = ?", (name,))
            user = cursor.fetchall()
            if user:
                cursor.execute("DELETE FROM `users` WHERE `name` = ?", (name,))
                connect.commit()
                connect.close()
                return {"message": "True"}
            else:
                return {"message": "False"}
        else:
            return {"message": "False"}

api.add_resource(Name_gmail, "/api/regist")
api.add_resource(Send_message, "/api/send_message")
api.add_resource(Get_messages, "/api/get_messages")
api.add_resource(Profil_user, "/api/user")
api.add_resource(Comands,"/api/comands")
api.add_resource(Search, "/api/search")

def delete_old_messages():
    while True:
        cursor.execute("DELETE FROM mes WHERE timestamp <= datetime('now', '-1 hours')")
        connect.commit()
        time.sleep(3600)

thread = threading.Thread(target=delete_old_messages, daemon=True)
thread.start()

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")