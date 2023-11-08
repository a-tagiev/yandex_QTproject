import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget


class ProfilePage(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Profile Page")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.username_label = QLabel(f"Username: {username}", self)
        self.username_label.setGeometry(20, 20, 100, 30)

        self.edit_button = QPushButton("Edit Profile", self)
        self.edit_button.setGeometry(20, 60, 100, 30)
        self.edit_button.clicked.connect(self.edit_profile)

        self.delete_button = QPushButton("Delete Profile", self)
        self.delete_button.setGeometry(20, 100, 100, 30)
        self.delete_button.clicked.connect(self.delete_profile)

    def edit_profile(self):
        pass
        # Обработчик нажатия кнопки "Edit Profile"
        # Добавьте здесь код для редактирования профиля

    def delete_profile(self):
        pass
        # Обработчик нажатия кнопки "Delete Profile"
        # Добавьте здесь код для удаления профиля

if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = "JohnDoe"  # Замените на фактическое имя пользователя
    profile_window = ProfilePage(username)
    profile_window.show()
    sys.exit(app.exec_())
