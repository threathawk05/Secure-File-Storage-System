import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, 
    QLineEdit, QMessageBox, QCheckBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from auth import login_user, register_user
from file_manager import encrypt_file, decrypt_file

# 🎨 Global Styles
STYLE_SHEET = """
    QWidget {
        background-color: #121212;
        color: white;
        font-size: 18px;
    }
    QLineEdit {
        background-color: #1E1E1E;
        border: 2px solid #00FF00;
        color: white;
        padding: 8px;
        border-radius: 8px;
        font-size: 20px;
    }
    QLineEdit:focus {
        border: 2px solid #00AA00;
    }
    QPushButton {
        background-color: #00FF00;
        color: black;
        font-weight: bold;
        padding: 10px;
        border-radius: 10px;
        font-size: 18px;
    }
    QPushButton:hover {
        background-color: #00AA00;
    }
    QLabel {
        font-size: 20px;
        font-weight: bold;
    }
"""

# ✅ Login Window
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Login - Secure File Storage")
        self.setGeometry(500, 300, 350, 350)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        self.title_label = QLabel("🔐 Secure File Storage")
        self.title_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter Password")
        layout.addWidget(self.password_input)

        # 🔘 Show/Hide Password Toggle
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setStyleSheet("color: lightgray; font-size: 14px;")
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.login_button = QPushButton("Login ✅")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Create Account 📝")
        self.register_button.clicked.connect(self.open_register_window)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        self.password_input.setEchoMode(
            QLineEdit.Normal if self.show_password_checkbox.isChecked() else QLineEdit.Password
        )

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Both fields are required!")
            return

        success, message = login_user(username, password)
        if success:
            QMessageBox.information(self, "Success", "Login successful! ✅")
            self.close()
            self.main_window = MainWindow(username)
            self.main_window.show()
        else:
            QMessageBox.warning(self, "Login Failed", message)

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

# ✅ Registration Window
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✍ Register - Secure File Storage")
        self.setGeometry(500, 300, 350, 320)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        self.title_label = QLabel("✍ Create a New Account")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Create a Password (Min 6 characters)")
        layout.addWidget(self.password_input)

        # 🔘 Show/Hide Password Toggle
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setStyleSheet("color: lightgray; font-size: 14px;")
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.register_button = QPushButton("Register 🛡️")
        self.register_button.clicked.connect(self.handle_registration)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        self.password_input.setEchoMode(
            QLineEdit.Normal if self.show_password_checkbox.isChecked() else QLineEdit.Password
        )

    def handle_registration(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Registration Failed", "Both fields are required!")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Weak Password", "Password must be at least 6 characters long!")
            return

        success, message = register_user(username, password)
        if success:
            QMessageBox.information(self, "Success", "Account created successfully! ✅")
            self.close()
        else:
            QMessageBox.warning(self, "Registration Failed", message)

# ✅ Main Application Window
class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username  
        self.setWindowTitle("🛡️ Secure File Storage")
        self.setGeometry(400, 200, 400, 300)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()

        self.title_label = QLabel(f"🔐 Welcome, {self.username}")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.encrypt_button = QPushButton("Encrypt File 🔒")
        self.encrypt_button.clicked.connect(self.encrypt_selected_file)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Decrypt File 🔓")
        self.decrypt_button.clicked.connect(self.decrypt_selected_file)
        layout.addWidget(self.decrypt_button)

        # ✅ Help Button (Added)
        self.help_button = QPushButton("❓ Help")
        self.help_button.clicked.connect(self.show_help)
        layout.addWidget(self.help_button)

        self.logout_button = QPushButton("Logout 🔄")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def encrypt_selected_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        if file_path:
            success = encrypt_file(file_path, self.username)
            self.status_label.setText("✅ Encryption Successful!" if success else "❌ Encryption Failed!")

    def decrypt_selected_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Decrypt")
        if file_path:
            output_path = file_path.replace(".enc", ".decrypted")
            success = decrypt_file(file_path, self.username, output_path)
            self.status_label.setText("✅ Decryption Successful!" if success else "❌ Decryption Failed!")

    def show_help(self):
        QMessageBox.information(self, "🔹 Help - Secure File Storage", "Use this tool to encrypt and decrypt files securely.")

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

# ✅ Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()

    # Ensure the event loop keeps running
    exit_code = app.exec_()
    print("Application closed.")  # Debugging message
    sys.exit(exit_code)


