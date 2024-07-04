from tkinter import *
import json
import requests
import platform
import sqlite3

headers = {'Content-Type': 'application/json'}
name_devices = platform.node()
connect = sqlite3.connect('user.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS 
            users(
               name TEXT,
               name_devices TEXT
               )""")
connect.commit()

win = Tk()
win.geometry("500x500")

user_name_entry = Entry(win, width=25)
user_name_entry.grid(column=1, row=1, pady=5, padx=10)


win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_columnconfigure(3, minsize=60)
win.grid_rowconfigure(1, minsize=30)
win.grid_rowconfigure(2, minsize=30)
win.grid_rowconfigure(3, minsize=30)
win.grid_rowconfigure(4, minsize=30)
win.grid_rowconfigure(5, minsize=30)

win.mainloop()