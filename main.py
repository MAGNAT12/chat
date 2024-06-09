from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import sqlite3

app = Flask(__name__)
api = Api(app)

connect = sqlite3.connect('Chat.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS 
            users(
               id INTEGER PRIMARY KEY,
               name TEXT 
            )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS
               mes(
               name TEXT,
               message TEXT)""") 

connect.commit()


class Name_gmail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        args = parser.parse_args()
        name = args["name"]
        cursor.execute(f"SELECT `name` FROM `users` WHERE `name` = '{name}'")
        data = cursor.fetchone()
        if data is None:
            name = args["name"]
            cursor.execute("INSERT INTO users (name) VALUES (?);", (name,))
            connect.commit()
            return {'message':'Вы зарегистрированны'}  # Возвращаем пустой словарь в случае отсутствия данных
        else:
            return {'message':'Вы уже зарегистрированны'}
        

class Send_message(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("message", type=str)
        args = parser.parse_args()
        name = args["name"]
        cursor.execute(f"SELECT `name` FROM `users` WHERE `name` = '{name}'")
        data = cursor.fetchone()
        if data:
            name = args["name"]
            message = args["message"]
            cursor.execute("INSERT INTO mes(name, message) VALUES(?, ?);", (name, message))
            connect.commit()
            return {'message':'сообщение отправлено'}
        else:
            return {'message':"отправлено"}

class Get_messages(Resource):
    def get(self, name):
        cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
        user = cursor.fetchone()
        if not user:
            return {'error': 'User does not exist'}, 400
        cursor.execute("SELECT name, message FROM mes WHERE name = ?", (name,))
        messages = cursor.fetchall()
        if messages:
            for msg in messages:
                message_list = {'message': msg[1]}
            return message_list
        else:
            return {'message': 'No messages found'}, 200

api.add_resource(Name_gmail, "/api/regist")
api.add_resource(Send_message, "/api/send_message")
api.add_resource(Get_messages, "/api/get_messages/<string:name>")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")