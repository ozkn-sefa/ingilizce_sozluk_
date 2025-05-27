from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem)
import pyodbc


class SettingsWidget(QWidget):
    geri_don_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        print('SettingsWidget oluşturuluyor...')

        with open('style\\styles6.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.btn_kelime_havuzu = QPushButton('Kelime Havuzu')
        self.btn_kelime_havuzu.setFixedSize(250, 40)
        self.btn_kelime_havuzu.clicked.connect(self.show_kelime_havuzu)

        self.btn_info = QPushButton('Info')
        self.btn_info.setFixedSize(250, 40)
        self.btn_info.clicked.connect(self.show_info)

        self.btn_geri_don = QPushButton('Geri Dön')
        self.btn_geri_don.setFixedSize(250, 40)
        self.btn_geri_don.clicked.connect(self.show_main)

        self.btn_ana_menu = QPushButton('Geri Dön')
        self.btn_ana_menu.setFixedSize(250, 40)
        self.btn_ana_menu.clicked.connect(self.return_to_menu)

        self.info_label = QLabel('Bu uygulama, kelimeleri veritabanından çekerek listeleme işlevi görür.')
        self.info_label.setVisible(False)

        self.table = QTableWidget()
        self.table.setVisible(False)
        self.layout.addWidget(self.table)

        self.layout.addWidget(self.btn_kelime_havuzu, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.btn_info, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.btn_geri_don, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.btn_ana_menu, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

        self.btn_geri_don.setVisible(False)
        self.btn_ana_menu.setVisible(True)

    def get_kelimeler_from_db(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')
            cursor = conn.cursor()
            cursor.execute('SELECT kelime_turkce, kelime_ingilizce FROM kelimeler ORDER BY kelimeid ASC')
            kelimeler = cursor.fetchall()

            if 'conn' in locals():
                conn.close()
            return kelimeler

        except pyodbc.Error as e:
            print('Veritabanı bağlantı hatası:', e)
            return []

    def show_kelime_havuzu(self):
        print('Kelime havuzu açılıyor...')
        kelimeler = self.get_kelimeler_from_db()

        if not kelimeler:
            print('Veritabanından kelimeler alınamadı!')
            return

        self.table.setRowCount(len(kelimeler))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Türkçe Kelime', 'İngilizce Kelime'])

        for i, kelime in enumerate(kelimeler):
            self.table.setItem(i, 0, QTableWidgetItem(str(kelime[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(kelime[1])))
            self.table.setColumnWidth(1, 150)
            self.table.setColumnWidth(0, 150)

        self.table.setVisible(True)
        self.btn_kelime_havuzu.setVisible(False)
        self.btn_info.setVisible(False)
        self.info_label.setVisible(False)
        self.btn_geri_don.setVisible(True)
        self.btn_ana_menu.setVisible(False)

    def show_info(self):
        print('Info ekranı açılıyor...')
        self.info_label.setVisible(True)
        self.btn_kelime_havuzu.setVisible(False)
        self.btn_info.setVisible(False)

        if self.table:
            self.table.setVisible(False)

        self.btn_geri_don.setVisible(True)
        self.btn_ana_menu.setVisible(False)

    def show_main(self):
        print('Ana ekrana dönülüyor...')

        if self.table:
            self.table.setVisible(False)

        self.info_label.setVisible(False)
        self.btn_kelime_havuzu.setVisible(True)
        self.btn_info.setVisible(True)
        self.btn_geri_don.setVisible(False)
        self.btn_ana_menu.setVisible(True)

    def return_to_menu(self):
        print('Menüye dönülüyor...')
        self.btn_kelime_havuzu.setVisible(False)
        self.btn_info.setVisible(False)

        if self.table:
            self.table.setVisible(False)

        self.info_label.setVisible(False)
        self.geri_don_signal.emit()
        self.btn_geri_don.setVisible(False)
        self.btn_ana_menu.setVisible(False)