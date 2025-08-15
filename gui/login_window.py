# gui/login_window.py
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from auth import register_user, verify_password
from db import get_user_by_username
from gui.dashboard import Dashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prompt Repository - Login")
        self.setFixedSize(300, 180)
        layout = QVBoxLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)

        button_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.handle_login)
        self.register_btn.clicked.connect(self.handle_register)

    def handle_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        user_row = get_user_by_username(username)
        if not user_row:
            QMessageBox.warning(self, "Error", "User does not exist.")
            return
        if verify_password(user_row['password_hash'], password):
            self.open_dashboard(user_row)
        else:
            QMessageBox.warning(self, "Error", "Incorrect password.")

    def handle_register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        try:
            register_user(username, password)
            QMessageBox.information(self, "Success", "Account created. Please log in.")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def open_dashboard(self, user_row):
        self.dashboard = Dashboard(user_row)
        self.dashboard.show()
        self.close()
