from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from add_word import AddKelimeWidget
from exam_setup import ExamSetupWidget
from settings import SettingsWidget
from report import RaporWidget
from puzzle import WordleWidget
from story import HikayeWidget
class MenuWidget(QWidget):


    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        with open('style\\styles4.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.welcome_label = QLabel('Hoş Geldiniz!')
        self.welcome_label.setFixedSize(250, 40)

        self.kelime_ekle_btn = QPushButton('Kelime Ekle')
        self.kelime_ekle_btn.setFixedSize(90, 90)
        self.kelime_ekle_btn.clicked.connect(self.open_add_kelime)

        self.sinav_btn = QPushButton('Sınav')
        self.sinav_btn.setFixedSize(90, 90)
        self.sinav_btn.clicked.connect(self.open_exam_setup)

        self.ayarlar_btn = QPushButton('Ayarlar')
        self.ayarlar_btn.setFixedSize(90, 90)
        self.ayarlar_btn.clicked.connect(self.open_settings)

        self.bulmaca_btn = QPushButton('Bulmaca')
        self.bulmaca_btn.setFixedSize(90, 90)
        self.bulmaca_btn.clicked.connect(self.open_bulmaca)

        self.hikaye_btn = QPushButton('Hikaye')
        self.hikaye_btn.setFixedSize(90, 90)
        self.hikaye_btn.clicked.connect(self.open_hikaye)

        self.rapor_al_btn = QPushButton('Rapor')
        self.rapor_al_btn.setFixedSize(90, 90)
        self.rapor_al_btn.clicked.connect(self.open_rapor)

        self.logout_btn = QPushButton('Çıkış Yap')
        self.logout_btn.setFixedSize(90, 90)
        self.logout_btn.clicked.connect(self.logout)

        self.top_buttons_layout = QHBoxLayout()
        self.top_buttons_layout.addWidget(self.kelime_ekle_btn)
        self.top_buttons_layout.addWidget(self.sinav_btn)
        self.top_buttons_layout.addWidget(self.bulmaca_btn)

        self.center_buttons_layout = QHBoxLayout()
        self.center_buttons_layout.addWidget(self.hikaye_btn)
        self.center_buttons_layout.addWidget(self.rapor_al_btn)
        self.center_buttons_layout.addWidget(self.ayarlar_btn)

        self.bottom_buttons_layout = QHBoxLayout()
        self.bottom_buttons_layout.addWidget(self.logout_btn)

        self.layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.top_buttons_layout)
        self.layout.addLayout(self.center_buttons_layout)
        self.layout.addLayout(self.bottom_buttons_layout)

        self.setLayout(self.layout)

    def set_user_id(self, user_id):
        self.current_user_id = user_id
        print(f'MenuWidget - Aktif kullanıcı ID: {self.current_user_id}')

    def logout(self):
        self.main_app.setCurrentWidget(self.main_app.login_widget)

    def open_add_kelime(self):
        self.add_kelime_widget = AddKelimeWidget()
        self.add_kelime_widget.geri_don_signal.connect(self.show_menu)
        self.hide_menu()
        self.layout.addWidget(self.add_kelime_widget)

    def open_bulmaca(self):
         self.bulmaca = WordleWidget()
         self.bulmaca.geri_don_signal.connect(self.show_menu)
         self.hide_menu()
         self.layout.addWidget(self.bulmaca)

    def open_hikaye(self):
        self.hikaye = HikayeWidget()
        self.hikaye.geri_don_signal.connect(self.show_menu)
        self.hide_menu()
        self.layout.addWidget(self.hikaye)

    def open_exam_setup(self):
        self.add_sinav = ExamSetupWidget(user_id=self.current_user_id)
        self.add_sinav.geri_don_signal.connect(self.show_menu)
        self.hide_menu()
        self.layout.addWidget(self.add_sinav)

    def open_settings(self):
        self.settings = SettingsWidget()
        self.settings.geri_don_signal.connect(self.show_menu)
        self.hide_menu()
        self.layout.addWidget(self.settings)

    def open_rapor(self):
        self.rapor = RaporWidget(user_id=self.current_user_id)
        self.rapor.geri_don_signal.connect(self.show_menu)
        self.hide_menu()
        self.layout.addWidget(self.rapor)

    def hide_menu(self):
        self.welcome_label.setVisible(False)
        self.kelime_ekle_btn.setVisible(False)
        self.sinav_btn.setVisible(False)
        self.ayarlar_btn.setVisible(False)
        self.logout_btn.setVisible(False)
        self.rapor_al_btn.setVisible(False)
        self.bulmaca_btn.setVisible(False)
        self.hikaye_btn.setVisible(False)

    def show_menu(self):
        if hasattr(self, 'add_kelime_widget'):
            self.add_kelime_widget.setParent(None)
        if hasattr(self, 'add_sinav'):
            self.add_sinav.setParent(None)
        if hasattr(self, 'settings'):
            self.settings.setParent(None)
        if hasattr(self, 'rapor'):
            self.rapor.setParent(None)
        if hasattr(self, 'bulmaca'):
            self.bulmaca.setParent(None)
        if hasattr(self, 'hikaye'):
            self.hikaye.setParent(None)

        self.welcome_label.setVisible(True)
        self.kelime_ekle_btn.setVisible(True)
        self.sinav_btn.setVisible(True)
        self.ayarlar_btn.setVisible(True)
        self.logout_btn.setVisible(True)
        self.rapor_al_btn.setVisible(True)
        self.bulmaca_btn.setVisible(True)
        self.hikaye_btn.setVisible(True)