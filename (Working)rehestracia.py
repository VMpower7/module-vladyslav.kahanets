import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_users_table():
    try:
        with sqlite3.connect("for_modul.db", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT
                )
            """)
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при створенні таблиці користувачів: {str(e)}")

def is_username_unique(username):
    with sqlite3.connect("for_modul.db", timeout=10) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
    return existing_user is None

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    age = entry_age.get()
    gender = variable_gender.get()

    if not is_username_unique(username):
        messagebox.showerror("Помилка", "Ім'я користувача вже використовується.")
        return

    try:
        with sqlite3.connect("for_modul.db", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password, age, gender) VALUES (?, ?, ?, ?)",
                           (username, password, age, gender))
        messagebox.showinfo("Реєстрація", f"Користувач {username} успішно зареєстрований!")
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при реєстрації: {str(e)}")

def login_user():
    username = entry_username.get()
    password = entry_password.get()

    try:
        with sqlite3.connect("for_modul.db", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()

        if existing_user:
            stored_password = existing_user[2]  # індекс 2 - це пароль у таблиці
            if password == stored_password:
                messagebox.showinfo("Авторизація", f"Користувач {username} успішно авторизований!")
            else:
                messagebox.showerror("Помилка", "Неправильний пароль.")
        else:
            messagebox.showerror("Помилка", "Користувача з таким логіном не знайдено.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при авторизації: {str(e)}")

# Створення таблиці користувачів при запуску програми
create_users_table()

# Створення головного вікна
root = tk.Tk()
root.title("Реєстрація та авторизація користувача by Vladyslav Kahanets")

# Встановлення розміру вікна в три рази більше
root.geometry("900x600")

# Кастомний стиль для мінімалістичного дизайну
root.tk_setPalette(background='#F5F5DC', foreground='#000000')
root.option_add('*TButton*highlightBackground', '#F5F5DC')
root.option_add('*TButton*highlightColor', '#F5F5DC')
root.option_add('*TButton*background', '#D2B48C')
root.option_add('*TButton*foreground', '#000000')

# Елементи вікна
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

# Використовуємо tk.StringVar для відстеження вибраного значення статі
variable_gender = tk.StringVar(root)
variable_gender.set("Чоловіча")  # Значення за замовчуванням

# Опції для випадаючого списку статі
gender_options = ["Чоловіча", "Жіноча"]

# Створення випадаючого списку
gender_menu = tk.OptionMenu(root, variable_gender, *gender_options)
gender_menu.config(font=('Arial', 12), background='#D2B48C')
gender_menu.pack(pady=5)

# Створення стилізованої кнопки для реєстрації
button_register = tk.Button(root, text="Зареєструвати", command=register_user, font=('Arial', 12),
                            background='#D2B48C', activebackground='#B8860B', foreground='#000000')
button_register.pack(pady=10)

# Створення стилізованої кнопки для входу
button_login = tk.Button(root, text="Увійти", command=login_user, font=('Arial', 12),
                         background='#D2B48C', activebackground='#B8860B', foreground='#000000')
button_login.pack(pady=10)

# Запуск головного циклу програми
root.mainloop()
