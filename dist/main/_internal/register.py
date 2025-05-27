import pyodbc
import hashlib
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon


class RegisterWidget(QWidget):


    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            with open('style\\styles2.qss', 'r') as f:
                self.setStyleSheet(f.read())

        except FileNotFoundError:
            print("Style file not found. Make sure 'style\\styles2.qss' exists.")

        self.username_label = QLabel('Kullanıcı Adı:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Kullanıcı adınızı girin')

        self.password_label = QLabel('Şifre:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Şifrenizi girin')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.toggle_password_action = QAction(self)
        self.toggle_password_action.setIcon(QIcon('presim\\i2.png'))
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)
        self.password_input.addAction(
            self.toggle_password_action,
            QLineEdit.ActionPosition.TrailingPosition
        )

        self.register_button = QPushButton('Kayıt Ol')
        self.back_button = QPushButton('Geri Dön')

        self.register_button.clicked.connect(self.register_user)
        self.back_button.clicked.connect(self.go_back_to_login)

        self.username_input.setFixedSize(250, 40)
        self.password_input.setFixedSize(250, 40)
        self.register_button.setFixedSize(250, 40)
        self.back_button.setFixedSize(250, 40)

        self.layout.addWidget(self.username_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.password_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def connect_db(self):
        return pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Uyarı', 'Kullanıcı adı ve şifre boş olamaz!')
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', username)
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, 'Uyarı', 'Bu kullanıcı adı zaten alınmış!')
                cursor.close()
                conn.close()
                return

            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, self.hash_password(password))
            )
            conn.commit()

            QMessageBox.information(self, 'Başarılı', 'Kayıt başarılı!')

            cursor.close()
            conn.close()

            self.clear_inputs()
            self.main_app.setCurrentWidget(self.main_app.login_widget)

        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu:')
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_action.setIcon(QIcon('presim\\i1.png'))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_action.setIcon(QIcon('presim\\i2.png'))

    def clear_inputs(self):
        """Kayıt alanlarını temizler."""
        self.username_input.clear()
        self.password_input.clear()

    def go_back_to_login(self):
        """Giriş ekranına geri döner ve kayıt alanlarını temizler."""
        self.clear_inputs()
        self.main_app.setCurrentWidget(self.main_app.login_widget)