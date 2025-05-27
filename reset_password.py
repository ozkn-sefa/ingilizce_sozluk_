import pyodbc
import hashlib
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon


class ResetPasswordWidget(QWidget):


    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            with open('style\\styles3.qss', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Style file not found. Make sure 'style\\styles3.qss' exists.")

        # Username field
        self.username_label = QLabel('Kullanıcı Adı:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Kullanıcı adınızı girin')

        # Password field
        self.new_password_label = QLabel('Yeni Şifre:')
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText('Yeni şifrenizi girin')
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Toggle password visibility action
        self.toggle_password_action = QAction(self)
        self.toggle_password_action.setIcon(QIcon('presim\\i2.png'))
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)
        self.new_password_input.addAction(
            self.toggle_password_action,
            QLineEdit.ActionPosition.TrailingPosition
        )

        # Buttons
        self.reset_button = QPushButton('Şifreyi Sıfırla')
        self.back_button = QPushButton('Geri Dön')

        # Connect signals
        self.reset_button.clicked.connect(self.reset_user_password)
        self.back_button.clicked.connect(self.go_back_to_login)

        # Set fixed sizes
        self.username_input.setFixedSize(250, 40)
        self.new_password_input.setFixedSize(250, 40)
        self.reset_button.setFixedSize(250, 40)
        self.back_button.setFixedSize(250, 40)

        # Add widgets to layout
        self.layout.addWidget(self.username_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.new_password_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.new_password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.reset_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def connect_db(self):
        return pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def reset_user_password(self):
        username = self.username_input.text().strip()
        new_password = self.new_password_input.text().strip()

        if not username or not new_password:
            QMessageBox.warning(self, 'Uyarı', 'Kullanıcı adı ve yeni şifre boş olamaz!')
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM users WHERE username = ?', username)
            result = cursor.fetchone()

            if not result:
                QMessageBox.warning(self, 'Hata', 'Böyle bir kullanıcı bulunamadı!')
                return

            cursor.execute(
                'UPDATE users SET password = ? WHERE username = ?',
                self.hash_password(new_password),
                username
            )
            conn.commit()

            QMessageBox.information(self, 'Başarılı', 'Şifre başarıyla güncellendi!')

            self.clear_inputs()
            self.main_app.setCurrentWidget(self.main_app.login_widget)

        except Exception as e:
            QMessageBox.critical(
                self,
                'Veritabanı Hatası',
                f'Veritabanı hatası oluştu:'
            )
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def toggle_password_visibility(self):
        if self.new_password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.new_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_action.setIcon(QIcon('presim\\i1.png'))
        else:
            self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_action.setIcon(QIcon('presim\\i2.png'))

    def clear_inputs(self):
        """Sıfırlama alanlarını temizler."""
        self.username_input.clear()
        self.new_password_input.clear()

    def go_back_to_login(self):
        """Giriş ekranına geri döner ve sıfırlama alanlarını temizler."""
        self.clear_inputs()
        self.main_app.setCurrentWidget(self.main_app.login_widget)