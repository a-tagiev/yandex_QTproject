import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QMessageBox

from logics.profile import ProfilePage

conn_b = sqlite3.connect("books.sqlite")
cursor_b = conn_b.cursor()
cursor_b.execute('''CREATE TABLE IF NOT EXISTS Books (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book_name TEXT NOT NULL UNIQUE,
                  author TEXT NOT NULL,
                  available BOOL True
                )''')


def get_book_id(book_name):
    conn_b = sqlite3.connect("books.sqlite")
    cursor_b = conn_b.cursor()
    cursor_b.execute("SELECT id FROM Books WHERE book_name = ?", (book_name,))
    book_id = cursor_b.fetchone()
    conn_b.close()
    if book_id:
        return book_id[0]
    else:
        return None


class MainPage(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Library Main Page")
        self.resize(400, 600)

        # Создаем центральный виджет для размещения содержимого
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем вертикальный макет для центрального виджета
        layout = QVBoxLayout(central_widget)

        # Добавляем метку с именем пользователя
        self.username_label = QLabel(f"<a href=''>{self.username}</a>")
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setOpenExternalLinks(True)  # Позволяет открывать ссылку в браузере
        self.username_label.linkActivated.connect(self.open_user_profile)  # Связываем сигнал с функцией
        layout.addWidget(self.username_label)

        # Добавляем метку с названием "Доступные книги"
        available_books_label = QLabel("Доступные книги:")
        layout.addWidget(available_books_label)
        # Создаем QListWidget для доступных книг
        self.available_books_listWidget = QListWidget()
        self.available_books_listWidget.itemClicked.connect(self.display_book_details)
        layout.addWidget(self.available_books_listWidget)

        # Добавляем метку с названием "Временно недоступно (в пользовании)"
        unavailable_books_label = QLabel("Временно недоступно (в пользовании):")
        layout.addWidget(unavailable_books_label)

        # Создаем QListWidget для недоступных книг
        self.unavailable_books_listWidget = QListWidget()
        self.unavailable_books_listWidget.itemClicked.connect(self.display_book_details)
        layout.addWidget(self.unavailable_books_listWidget)

        # Получаем список доступных и недоступных книг
        available_books = self.get_available_books()
        unavailable_books = self.get_unavailable_books()

        # Заполняем QListWidgets
        self.populate_available_books(available_books)
        self.populate_unavailable_books(unavailable_books)

    def display_book_details(self, item):
        # Извлекаем имя книги
        book_name = item.text().split(' (')[0]
        # Извлекаем автора
        id_book = get_book_id(book_name)
        author = cursor_b.execute(f'''SELECT author FROM Books WHERE id={id_book}''').fetchone()[0]
        QMessageBox.information(self, "Book Details", f"Selected Book: {book_name} by {author}")
        # Получить статус книги

    def get_unavailable_books(self):
        try:
            conn = sqlite3.connect("books.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT book_name FROM Books WHERE available = 0")
            unavailable_books = cursor.fetchall()
            conn.close()
            return [book[0] for book in unavailable_books]
        except sqlite3.Error as e:
            print("SQLite error:", str(e))
            return []

    def populate_unavailable_books(self, books):
        for book in books:
            self.unavailable_books_listWidget.addItem(book)

    def get_available_books(self):
        try:
            conn = sqlite3.connect("books.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT book_name FROM Books WHERE available = 1")
            available_books = cursor.fetchall()
            conn.close()
            return [book[0] for book in available_books]
        except sqlite3.Error as e:
            print("SQLite error:", str(e))
            return []

    def populate_available_books(self, books):
        for book in books:
            self.available_books_listWidget.addItem(book)

    def open_user_profile(self):
        user_profile_window = ProfilePage(self.username)
        self.hide()  # Скрыть текущее окно
        user_profile_window.show()
