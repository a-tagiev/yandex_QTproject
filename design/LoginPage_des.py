# LoginPage_des.py
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(110, 50, 146, 106))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.username_label = QtWidgets.QLabel(self.splitter)
        self.username_label.setObjectName("username_label")
        self.login_field = QtWidgets.QLineEdit(self.splitter)
        self.login_field.setText("")
        self.login_field.setObjectName("login_field")
        self.pwd_label = QtWidgets.QLabel(self.splitter)
        self.pwd_label.setMinimumSize(QtCore.QSize(146, 16))
        self.pwd_label.setObjectName("pwd_label")
        self.password_field = QtWidgets.QLineEdit(self.splitter)
        self.password_field.setObjectName("password_field")
        self.Login_button = QtWidgets.QPushButton(self.splitter)
        self.Login_button.setObjectName("Login_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Login Form"))
        self.username_label.setText(_translate("Form", "username"))
        self.pwd_label.setText(_translate("Form", "password"))
        self.Login_button.setText(_translate("Form", " Login or register"))
