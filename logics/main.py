import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QMessageBox, QPushButton

from logics.profile import ProfilePage

conn_b = sqlite3.connect("books.sqlite")
cursor_b = conn_b.cursor()
cursor_b.execute('''CREATE TABLE IF NOT EXISTS Books (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book_name TEXT NOT NULL UNIQUE,
                  author TEXT NOT NULL,
                  available BOOL True,
                  booked TEXT DEFAULT 'No'
                )''')


def get_book_id(book_name):
    conn = sqlite3.connect("books.sqlite")
    cursor = conn_b.cursor()
    cursor.execute("SELECT id FROM Books WHERE book_name = ?", (book_name,))
    book_id = cursor.fetchone()
    conn.close()
    if book_id:
        return book_id[0]
    else:
        return None


def get_book_info(id_book):
    return cursor_b.execute(f"SELECT available,booked FROM Books WHERE id={id_book}").fetchone()


class MainPage(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Library Main Page")
        self.resize(400, 800)

        # Создаем центральный виджет для размещения содержимого
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем вертикальный макет для центрального виджета
        layout = QVBoxLayout(central_widget)

        # Добавляем метку с именем пользователя
        self.username_button = QPushButton(f"{self.username}")
        self.username_button.resize(40, 20)
        layout.addWidget(self.username_button)
        self.username_button.clicked.connect(self.open_profile)
        # Добавляем метку с названием "Доступные книги"
        available_books_label = QLabel("Available books:")
        layout.addWidget(available_books_label)
        # Создаем QListWidget для доступных книг
        self.available_books_listWidget = QListWidget()
        self.available_books_listWidget.itemClicked.connect(self.display_book_details)
        layout.addWidget(self.available_books_listWidget)
        available_books = self.get_available_books()
        self.populate_available_books(available_books)
        # Добавляем метку с названием "Временно недоступно (в пользовании)"
        unavailable_books_label = QLabel("Temporarily unavailable (in use):")
        layout.addWidget(unavailable_books_label)

        # Создаем QListWidget для недоступных книг
        self.unavailable_books_listWidget = QListWidget()
        self.unavailable_books_listWidget.itemClicked.connect(self.display_book_details)
        layout.addWidget(self.unavailable_books_listWidget)

        # Получаем список доступных и недоступных книг
        unavailable_books = self.get_unavailable_books()

        # Заполняем QListWidgets
        self.populate_available_books(available_books)
        self.populate_unavailable_books(unavailable_books)

    def display_book_details(self, item):
        # Извлекаем имя книги
        book_name = item.text().split(' (')[0]
        # Извлекаем автора
        id_book = get_book_id(book_name)
        conn = sqlite3.connect("books.sqlite")
        cursor = conn.cursor()
        author = cursor.execute(f'''SELECT author FROM Books WHERE id={id_book}''').fetchone()[0]
        conn.close()
        QMessageBox.information(self, "Book Details", f"Selected Book: {book_name} by {author}")
        # Получить статус книги
        available, booked = get_book_info(id_book)
        if available == 1 and booked == "No":
            message = f"You can choose the book '{book_name}'"
            buttons = QMessageBox.Yes | QMessageBox.No
            response = QMessageBox.question(self, "reserve this book?", message, buttons)
            if response == QMessageBox.Yes:
                conn = sqlite3.connect("books.sqlite")
                cursor = conn.cursor()
                cursor.execute("UPDATE Books SET available = 0, booked = ? WHERE id = ?", (self.username, id_book))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "successful", "successfully booked")
                self.unavailable_books_listWidget.addItem(item.text())
                self.available_books_listWidget.takeItem(self.available_books_listWidget.currentRow())
        elif available == 0 and booked == self.username:
            message = f"The book '{book_name}' is reserved by you, you can hand it over"
            buttons = QMessageBox.Yes | QMessageBox.No
            response = QMessageBox.question(self, "hand over this book?", message, buttons)
            if response == QMessageBox.Yes:
                conn = sqlite3.connect("books.sqlite")
                cursor = conn.cursor()
                cursor.execute("UPDATE Books SET available = 1, booked = ? WHERE id = ?", ('No', id_book))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "successful", "successfully handed over")
                self.available_books_listWidget.addItem(item.text())
                self.unavailable_books_listWidget.takeItem(self.unavailable_books_listWidget.currentRow())
        elif available == 0 and booked != self.username:
            message = f"The book '{book_name}' is reserved by another user"
            buttons = QMessageBox.Ok
            QMessageBox.information(self, "the book is reserved", message, buttons)

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

    def open_profile(self):
        # self.hide()  # Скрыть текущее окно
        user_profile_window = ProfilePage(self.username)
        user_profile_window.show()


