#цей код містить в собі реєстрацію по пошті, але він не робить, тому що: "Щоб захистити ваш обліковий запис, починаючи з 30 травня 2022 року, Google більше не підтримує сторонні програми та пристрої, 
#які пропонують увійти в обліковий запис Google лише за допомогою імені користувача та пароля."

# module(not working)-vladyslav.kahanets

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import smtplib
import random
from email.mime.text import MIMEText

def create_users_table():
    try:
        with sqlite3.connect("for_modul", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    email TEXT UNIQUE,
                    verification_code INTEGER
                )
            """)
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при створенні таблиці користувачів: {str(e)}")

def is_email_unique(email):
    with sqlite3.connect("for_modul", timeout=10) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cursor.fetchone()
    return existing_user is None

def send_verification_code(email, code):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    username = "noreplyformoduleprogramm@gmail.com"
    password = "123www123"

    server.login(username, password)

    subject = "Код підтвердження реєстрації"
    body = f"Ваш код підтвердження: {code}"
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = username
    message["To"] = email

    server.sendmail(username, [email], message.as_string())
    server.quit()

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    age = entry_age.get()
    gender = variable_gender.get()
    email = entry_email.get()

    if not is_email_unique(email):
        messagebox.showerror("Помилка", "Ця електронна пошта вже використовується.")
        return

    verification_code = random.randint(1000, 9999)

    send_verification_code(email, verification_code)

    try:
        with sqlite3.connect("for_modul", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, age, gender, email, verification_code)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, password, age, gender, email, verification_code))

        messagebox.showinfo("Реєстрація", "Код підтвердження відправлено на вашу електронну пошту.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при реєстрації: {str(e)}")

create_users_table()

root = tk.Tk()
root.title("Реєстрація та авторизація користувача by Vladyslav Kahanets")
root.geometry("900x600")

root.tk_setPalette(background='#F5F5DC', foreground='#000000')
root.option_add('*TButton*highlightBackground', '#F5F5DC')
root.option_add('*TButton*highlightColor', '#F5F5DC')
root.option_add('*TButton*background', '#D2B48C')
root.option_add('*TButton*foreground', '#000000')

label_username = tk.Label(root, text="Логін:", font=('Arial', 12), background='#F5F5DC')
label_username.pack(pady=5)

entry_username = tk.Entry(root, font=('Arial', 12), background='#FFFFFF')
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Пароль:", font=('Arial', 12), background='#F5F5DC')
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*", font=('Arial', 12), background='#FFFFFF')
entry_password.pack(pady=5)

label_age = tk.Label(root, text="Вік:", font=('Arial', 12), background='#F5F5DC')
label_age.pack(pady=5)

entry_age = tk.Entry(root, font=('Arial', 12), background='#FFFFFF')
entry_age.pack(pady=5)

label_gender = tk.Label(root, text="Стать:", font=('Arial', 12), background='#F5F5DC')
label_gender.pack(pady=5)

variable_gender = tk.StringVar(root)
variable_gender.set("Чоловіча")  # Значення за замовчуванням

gender_options = ["Чоловіча", "Жіноча"]

gender_menu = tk.OptionMenu(root, variable_gender, *gender_options)
gender_menu.config(font=('Arial', 12), background='#D2B48C')
gender_menu.pack(pady=5)

label_email = tk.Label(root, text="Електронна пошта:", font=('Arial', 12), background='#F5F5DC')
label_email.pack(pady=5)

entry_email = tk.Entry(root, font=('Arial', 12), background='#FFFFFF')
entry_email.pack(pady=5)

button_register = tk.Button(root, text="Зареєструвати", command=register_user, font=('Arial', 12),
                            background='#D2B48C', activebackground='#B8860B', foreground='#000000')
button_register.pack(pady=10)

root.mainloop()
