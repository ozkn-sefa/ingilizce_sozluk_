import pyodbc
import hashlib
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt


class LoginWidget(QWidget):

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Layout setup
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        with open('style\\styles1.qss', 'r') as f:
            self.setStyleSheet(f.read())

        # Username field
        self.username_label = QLabel('Kullanıcı Adı:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Kullanıcı adınızı girin')

        # Password field
        self.password_label = QLabel('Şifre:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Şifrenizi girin')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Toggle password visibility action
        self.toggle_password_action = QAction(self)
        self.toggle_password_action.setIcon(QIcon('presim\\i2.png'))
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)
        self.password_input.addAction(self.toggle_password_action, QLineEdit.ActionPosition.TrailingPosition)

        # Buttons
        self.login_button = QPushButton('Giriş Yap')
        self.register_button = QPushButton('Kaydol')
        self.forgot_button = QPushButton('Şifremi Unuttum')

        # Button connections
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.go_to_register)
        self.forgot_button.clicked.connect(self.go_to_reset)

        # Set fixed sizes
        for widget in [self.username_input, self.password_input,
                       self.login_button, self.register_button, self.forgot_button]:
            widget.setFixedSize(250, 40)

        # Add widgets to layout
        for widget in [self.username_label, self.username_input,
                       self.password_label, self.password_input,
                       self.login_button, self.register_button, self.forgot_button]:
            self.layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def connect_db(self):
        return pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Uyarı', 'Kullanıcı adı ve şifre boş olamaz!')
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            cursor.execute('SELECT userid, password FROM users WHERE username = ?', username)
            result = cursor.fetchone()

            if not result:
                QMessageBox.warning(self, 'Hata', 'Böyle bir kullanıcı bulunamadı!')
            else:
                userid, stored_password = result
                if stored_password == self.hash_password(password):
                    self.main_app.set_user_id(userid)
                    print(f'Giriş başarılı! Kullanıcı ID: {userid}')

                    # Update welcome message
                    self.main_app.menu_widget.welcome_label.setText(f'Hoş geldiniz, {username}!')
                    self.main_app.setCurrentWidget(self.main_app.menu_widget)

                    # Clear inputs
                    self.clear_inputs()
                else:
                    QMessageBox.warning(self, 'Hata', 'Kullanıcı adı veya şifre yanlış!')
        except Exception as e:
            QMessageBox.critical(self, 'Veritabanı Hatası',
                                 f'Veritabanı bağlantısı sırasında bir hata oluştu')
        finally:
            cursor.close()
            conn.close()

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_action.setIcon(QIcon('presim\\i1.png'))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_action.setIcon(QIcon('presim\\i2.png'))

    def clear_inputs(self):
        """Giriş alanlarını temizler."""
        self.username_input.clear()
        self.password_input.clear()

    def go_to_register(self):
        """Kayıt ekranına gider ve giriş alanlarını temizler."""
        self.clear_inputs()
        self.main_app.setCurrentWidget(self.main_app.register_widget)

    def go_to_reset(self):
        """Şifremi unuttum ekranına gider ve giriş alanlarını temizler."""
        self.clear_inputs()
        self.main_app.setCurrentWidget(self.main_app.reset_widget)