import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from design import LoginPage_des
from logics.main import MainPage

conn = sqlite3.connect("../database/users.sqlite")
cursor = conn.cursor()

def check_password(username, password):
    cursor.execute(f"SELECT user,password FROM Users WHERE user={username} AND password={password}")
    flag = cursor.fetchone()
    if len(flag) == 0:
        return False
    return True


class LoginForm(QWidget, LoginPage_des.Ui_Form):
    username = ""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Form")
        self.Login_button.clicked.connect(self.login)
        self.username = self.username_label.text()
        self.password = self.password_field.text()

    def login(self):

        if check_password(self.username, self.password):
            self.switch_to_main_window(self.username)
        else:
            self.setWindowTitle("Incorrect password")

    def add_new_user(self, username, password):
        cursor.execute("INSERT INTO Users (user, password) VALUES (?, ?)", (username, password))
        conn.commit()  # Сохраняем изменения в базе данных

    def switch_to_main_window(self, username):
        self.close()  # Закрыть окно входа
        self.main_window = MainPage(username)
        self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())
