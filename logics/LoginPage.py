import sqlite3
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from design.LoginPage_des import Ui_Form
from main import MainPage

conn = sqlite3.connect("users.sqlite")
cursor = conn.cursor()

# Создаем таблицу пользователей, если ее нет
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  registration_date TEXT
                )''')


class LoginForm(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.username = ""
        self.setupUi(self)
        self.setWindowTitle("Login Form")
        self.Login_button.clicked.connect(self.login)

    def login(self):
        username = self.login_field.text()
        password = self.password_field.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Both username and password are required.")
            return

        cursor.execute("SELECT username, password FROM Users WHERE username = ? AND password = ?",
                       (username, password))
        user = cursor.fetchone()

        if user:
            conn.close()
            self.switch_to_main_window(username)
        else:
            response = QMessageBox.question(self, "Error",
                                            "Incorrect username or password. Do you want to register a new user?",
                                            QMessageBox.Yes | QMessageBox.No)
            if response == QMessageBox.Yes:
                self.add_new_user(username, password)
            else:
                self.login_field.clear()
                self.password_field.clear()

    def add_new_user(self, username, password):
        self.username = username
        try:
            date = datetime.now()
            reg_date = "{}.{}.{}  {}:{}".format(date.day, date.month, date.year, date.hour, date.minute)
            cursor.execute("INSERT INTO Users (username, password, registration_date) VALUES (?, ?, ?)",
                           (username, password, reg_date))
            conn.commit()
            QMessageBox.information(self, "Success", "Registration successful.")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "User already exists.")

    def switch_to_main_window(self, username):
        self.close()  # Закрыть окно входа
        self.main_window = MainPage(username)  # Создать основное окно, передавая имя пользователя
        self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())
