import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtGui import QIcon
from login import LoginWidget
from register import RegisterWidget
from reset_password import ResetPasswordWidget
from anasayfa1 import MenuWidget


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sözlük')
        self.setWindowIcon(QIcon('presim/images.png'))  # Doğru dosya yolunu belirtin

        self.load_stylesheet('style/styles.qss')  # QSS stil dosyasının yolunu düzeltin

        self.current_user_id = None

        # Widget'ları oluştur
        self.login_widget = LoginWidget(self)
        self.register_widget = RegisterWidget(self)
        self.reset_widget = ResetPasswordWidget(self)
        self.menu_widget = MenuWidget(self)

        # Kullanıcı id'sini menü widget'ına aktar
        self.menu_widget.set_user_id(self.current_user_id)

        # Widget'ları stacked widget'a ekle
        self.addWidget(self.login_widget)
        self.addWidget(self.register_widget)
        self.addWidget(self.reset_widget)
        self.addWidget(self.menu_widget)

        # İlk başta login widget'ı göster
        self.setCurrentWidget(self.login_widget)

        self.showMaximized()

    def load_stylesheet(self, file_path):
        # QSS stil dosyasını yükle
        with open(file_path, 'r') as file:
            self.setStyleSheet(file.read())

    def set_user_id(self, user_id):
        # Kullanıcı id'sini güncelle
        self.current_user_id = user_id
        self.menu_widget.set_user_id(user_id)
        print(f'Aktif kullanıcı ID: {self.current_user_id}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
