import sqlite3
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMainWindow

# Welcome Interface
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("WelcomeScreen.ui", self)
        self.login.clicked.connect(self.Tologin) # when user clicked "login"
        self.create.clicked.connect(self.Tocreate)

    def Tologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Tocreate(self):
        create = CreateScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Login interface if button = login
class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("Login_Screen.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.userfield.text()
        password = self.passwordfield.text()

        if not user or not password:
            self.error1.setText("Please input all fields.")
            return

        try:
            conn = sqlite3.connect("account.db")
            cur = conn.cursor()
            query = 'SELECT password FROM information WHERE username = ?'
            cur.execute(query, (user,))
            result_pass = cur.fetchone()

            if result_pass is None or result_pass[0] != password:
                self.error1.setText("Invalid username or password")
            else:
                # Navigate to main menu instead of just printing success
                self.error1.setText("")
                main_menu = MainMenuScreen()
                widget.addWidget(main_menu)
                widget.setCurrentIndex(widget.currentIndex() + 1)

        except sqlite3.Error as e:
            self.error1.setText("Database error occurred.")
        finally:
            if conn:
                conn.close()

class CreateScreen(QDialog):
    def __init__(self):
        super(CreateScreen, self).__init__()
        loadUi("create.ui", self)
        self.password1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password2.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signup.clicked.connect(self.signupfunction)

    def signupfunction(self):
        user = self.user1.text()
        email = self.email.text()
        firstName = self.fname.text()
        lastName = self.lname.text()
        password = self.password1.text()
        confirmpassword = self.password2.text()

        if len(user) == 0 or len(email) == 0 or len(firstName) == 0 or len(lastName) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            self.error.setText("Please fill in all inputs.")
            return

        if password != confirmpassword:
            self.error.setText("Passwords do not match.")
            return

        try:
            conn = sqlite3.connect("account.db")
            cur = conn.cursor()
            user_info = [user, firstName, lastName, password, confirmpassword]
            cur.execute('INSERT INTO information (username, firstname, lastname, password, cpassword) VALUES (?, ?, ?, ?, ?)', user_info)
            conn.commit()
            self.error.setText("Signup successful! Please Re-Start the Application")
        except sqlite3.Error as e:
            self.error.setText(f"Database error: {e}")

# Main Menu interface
class MainMenuScreen(QDialog):
    def __init__(self):
        super(MainMenuScreen, self).__init__()
        loadUi("main_menu.ui", self)
        # Add any main menu button connections or functionality here
        #features to be added

#execute
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(811)
widget.setFixedWidth(1289)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")