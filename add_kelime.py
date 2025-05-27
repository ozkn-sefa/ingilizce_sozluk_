import shutil
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
import pyodbc


class AddKelimeWidget(QWidget):
    geri_don_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        with open('style\\styles5.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.ingilizce_label = QLabel('İngilizce Kelime:')
        self.ingilizce_input = QLineEdit()

        self.turkce_label = QLabel('Türkçe Kelime:')
        self.turkce_input = QLineEdit()

        self.resim_label = QLabel('Resim Seç:')
        self.resim_sec_btn = QPushButton('Resim Seç')
        self.resim_sec_btn.clicked.connect(self.resim_sec)

        self.kelime_ekle_btn = QPushButton('Kelime Ekle')
        self.kelime_ekle_btn.clicked.connect(self.kelime_ekle)

        self.geri_don_btn = QPushButton('Geri Dön')
        self.geri_don_btn.clicked.connect(self.geri_don)

        # Set fixed sizes for all widgets
        self.ingilizce_label.setFixedSize(250, 40)
        self.ingilizce_input.setFixedSize(250, 40)
        self.turkce_label.setFixedSize(250, 40)
        self.turkce_input.setFixedSize(250, 40)
        self.resim_label.setFixedSize(250, 40)
        self.resim_sec_btn.setFixedSize(250, 40)
        self.kelime_ekle_btn.setFixedSize(250, 40)
        self.geri_don_btn.setFixedSize(250, 40)

        # Add widgets to layout with center alignment
        align_center = Qt.AlignmentFlag.AlignCenter
        self.layout.addWidget(self.ingilizce_label, alignment=align_center)
        self.layout.addWidget(self.ingilizce_input, alignment=align_center)
        self.layout.addWidget(self.turkce_label, alignment=align_center)
        self.layout.addWidget(self.turkce_input, alignment=align_center)
        self.layout.addWidget(self.resim_label, alignment=align_center)
        self.layout.addWidget(self.resim_sec_btn, alignment=align_center)
        self.layout.addWidget(self.kelime_ekle_btn, alignment=align_center)
        self.layout.addWidget(self.geri_don_btn, alignment=align_center)

        self.setLayout(self.layout)
        self.resim_yolu = None

    def resim_sec(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(
            self, 'Resim Seç', '', 'Resim Dosyaları (*.png *.jpg *.jpeg *.bmp)'
        )

        if dosya_yolu:
            resim_klasoru = 'resim'
            if not os.path.exists(resim_klasoru):
                os.makedirs(resim_klasoru)

            yeni_resim_yolu = os.path.join(resim_klasoru, os.path.basename(dosya_yolu))
            shutil.copy(dosya_yolu, yeni_resim_yolu)

            self.resim_yolu = yeni_resim_yolu
            self.resim_label.setText(f'Seçilen Resim: {os.path.basename(dosya_yolu)}')

    def kelime_ekle(self):
        ingilizce = self.ingilizce_input.text().strip()
        turkce = self.turkce_input.text().strip()
        resim_yolu = self.resim_yolu if self.resim_yolu else None

        if not ingilizce or not turkce:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen tüm alanları doldurun!')
            return

        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;'
            )
            cursor = conn.cursor()

            cursor.execute('SELECT kelimeid FROM dbo.kelimeler WHERE kelime_ingilizce = ?', ingilizce)
            result = cursor.fetchone()

            if result:
                QMessageBox.warning(self, 'Hata', 'Bu kelime zaten mevcut!')
                self.ingilizce_input.clear()
                self.turkce_input.clear()
                self.resim_yolu = None
                self.resim_label.setText('Resim Seç:')
            else:
                cursor.execute(
                    """
                    INSERT INTO dbo.kelimeler (kelime_ingilizce, kelime_turkce, kelime_resimYolu) 
                    VALUES (?, ?, ?)
                    """,
                    ingilizce, turkce, resim_yolu
                )

                self.ingilizce_input.clear()
                self.turkce_input.clear()
                self.resim_yolu = None
                self.resim_label.setText('Resim Seç:')

                conn.commit()
                QMessageBox.information(self, 'Başarılı', 'Kelime başarıyla eklendi!')

            cursor.close()
            conn.close()

        except Exception as e:
            self.resim_label.setText(f'Hata: {str(e)}')

    def geri_don(self):
        self.geri_don_signal.emit()