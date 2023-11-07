import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from design.MainPage_des import Ui_LibraryMainPage
from LoginPage import LoginForm
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

# Inside the MainPage class
class MainPage(QMainWindow, Ui_LibraryMainPage):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setupUi(self)
        self.setWindowTitle("Library Main Page")
        self.user_profile_button.clicked.connect(self.open_user_profile)

        # Create QListWidget for available books
        self.available_books_listWidget = QListWidget()
        self.available_books_listWidget.setGeometry(20, 50, 300, 200)
        self.available_books_listWidget.itemClicked.connect(self.display_book_details)  # Connect a slot to show book details

        # Create QListWidget for rented books
        self.rented_books_listWidget = QListWidget()
        self.rented_books_listWidget.setGeometry(20, 260, 300, 200)
        self.rented_books_listWidget.itemClicked.connect(self.display_book_details)  # Connect a slot to show book details

        # Add the QListWidgets to the layout
        self.centralWidget().layout().addWidget(self.available_books_listWidget)
        self.centralWidget().layout().addWidget(self.rented_books_listWidget)

    def display_book_details(self, item):
        # Implement this method to show book details when a book is clicked
        # You can get the selected book from the item and display its details in a separate window

        def open_user_profile(self):
            user_profile_window = UserProfileWindow(self.username)
            user_profile_window.exec_()

# Rest of your code

if __name__ == "__main__":
    app = QApplication(sys.argv)
    username=LoginForm.username
    window = MainPage(username)
    window.show()
    sys.exit(app.exec_())
