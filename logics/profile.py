import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QPushButton, QLabel, QWidget, QToolBar


class ProfilePage(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("User Profile")
        self.resize(300, 200)

        # Создаем метку с именем пользователя
        self.username_label = QLabel(f"Username: {self.username}")
        self.username_label.setAlignment(Qt.AlignCenter)

        # Создаем метку для отображения количества взятых книг
        self.books_taken_label = QLabel("Books Taken: 0")
        self.books_taken_label.setAlignment(Qt.AlignCenter)

        # Создаем кнопку для удаления профиля
        self.delete_profile_button = QPushButton("Delete Profile")
        self.delete_profile_button.clicked.connect(self.delete_profile)

        self.log_out_button = QPushButton("Log out")
        self.delete_profile_button.clicked.connect(self.open_login)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.get_back_to_main)

        # Размещаем виджеты в вертикальном макете
        layout = QVBoxLayout(self)
        layout.addWidget(self.back_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.username_label)
        layout.addWidget(self.books_taken_label)
        layout.addWidget(self.delete_profile_button)
        layout.addWidget(self.log_out_button)
        # Подсчитываем количество взятых книг
        self.calculate_books_taken()

    def calculate_books_taken(self):
        try:
            conn = sqlite3.connect("../database/books.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Books WHERE booked = ?", (self.username,))
            books_taken_count = cursor.fetchone()[0]
            conn.close()

            self.books_taken_label.setText(f"Books Taken: {books_taken_count}")

        except sqlite3.Error as e:
            print("SQLite error:", str(e))

    def delete_profile(self):
        response = QMessageBox.question(self, "Delete Profile", "Are you sure you want to delete your profile?",
                                        QMessageBox.Yes | QMessageBox.No)

        if response == QMessageBox.Yes:
            try:
                conn = sqlite3.connect("../database/users.sqlite")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Users WHERE username = ?", (self.username,))
                conn.commit()
                conn.close()
                message = f"Your profile {self.username} was successfully deleted"
                buttons = QMessageBox.Ok
                QMessageBox.information(self, "delete profile", message, buttons)
                self.open_login()
                # Закрыть окно профиля после удаления
                self.close()
            except sqlite3.Error as e:
                print("SQLite error:", str(e))

    def get_back_to_main(self):
        self.close()

    def open_login(self):
        from LoginPage import LoginForm
        self.login_window = LoginForm()
        self.login_window.show()
        self.close()
