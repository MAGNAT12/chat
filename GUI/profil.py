from tkinter import *
import sqlite3

connect = sqlite3.connect('user.db', check_same_thread=False)

cursor = connect.cursor()

def profil():
    pro = Tk()
    pro.geometry("500x500")
    pro.title("profile")
    cursor.execute("SELECT name FROM users")
    name_sender = cursor.fetchall()

    l = Label(pro, text=name_sender[0], font=('Times', 20),)
    l.pack()


    pro.mainloop()