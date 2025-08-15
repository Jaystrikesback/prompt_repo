# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow
from db import initialize_database

def main():
    # Ensure database tables exist
    initialize_database()
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
