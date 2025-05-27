import pyodbc
import secrets  # random yerine secrets kullandık

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QSpacerItem, QSizePolicy,QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt


class WordleWidget(QWidget):
    geri_don_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        with open('style\\styles5.qss', 'r') as f:
            self.setStyleSheet(f.read())

        with open("veri\\kelimeler.txt", "r") as f:
            self.kelime_listesi = set(k.strip().lower() for k in f.readlines())

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        self.oyun_alani_widget = QWidget()
        self.oyun_alani_layout = QVBoxLayout(self.oyun_alani_widget)
        self.oyun_alani_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.oyun_alani_widget, stretch=1)

        self.alt_buton_widget = QWidget()
        self.alt_buton_layout = QVBoxLayout(self.alt_buton_widget)
        self.alt_buton_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alt_buton_layout.setSpacing(15)
        self.main_layout.addWidget(self.alt_buton_widget, stretch=1)

        self.oyun_alani_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.giris = QLineEdit()
        self.giris.setFixedSize(250, 50)
        self.alt_buton_layout.addWidget(self.giris)

        self.btn_tahmin = QPushButton("Tahmin Et")
        self.btn_tahmin.setFixedSize(250, 50)
        self.btn_tahmin.clicked.connect(self.tahmin_et)
        self.alt_buton_layout.addWidget(self.btn_tahmin)

        self.btn_yeniden = QPushButton("Yeniden Başla")
        self.btn_yeniden.setFixedSize(250, 50)
        self.btn_yeniden.clicked.connect(self.yeni_oyun)
        self.alt_buton_layout.addWidget(self.btn_yeniden)

        self.geri_don_btn = QPushButton("Geri Dön")
        self.geri_don_btn.setFixedSize(250, 50)
        self.geri_don_btn.clicked.connect(self.geri_don)
        self.alt_buton_layout.addWidget(self.geri_don_btn)

        self.uyari_etiketi = QLabel("")
        self.uyari_etiketi.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uyari_etiketi.setWordWrap(True)
        self.uyari_etiketi.setFixedWidth(300)
        self.uyari_etiketi.hide()
        self.alt_buton_layout.addWidget(self.uyari_etiketi)

        self.alt_buton_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.yeni_oyun()

    def kelime_getir(self):
        conn = pyodbc.connect("Driver={SQL Server};Server=localhost;Database=projeyazılımyapımı;Trusted_Connection=yes;")
        cursor = conn.cursor()
        cursor.execute("SELECT kelime_ingilizce FROM kelimeler")
        kelimeler = [row[0].upper() for row in cursor.fetchall()]
        conn.close()
        return secrets.choice(kelimeler)  # Burada random.choice yerine secrets.choice kullandık

    # (Diğer fonksiyonlar aynı kalacak...)

    def degerlendir_tahmin(self, hedef, tahmin):
        sonuc = []
        for i in range(len(tahmin)):
            if tahmin[i] == hedef[i]:
                sonuc.append(('green', tahmin[i]))
            elif tahmin[i] in hedef:
                sonuc.append(('yellow', tahmin[i]))
            else:
                sonuc.append(('gray', tahmin[i]))
        return sonuc

    def yeni_oyun(self):
        self.clear_game_widgets()

        self.hedef_kelime = self.kelime_getir()
        self.uzunluk = len(self.hedef_kelime)
        self.tahmin_hakki = 6
        self.satir = 0

        self.giris.setMaxLength(self.uzunluk)
        self.giris.setPlaceholderText(f"{self.uzunluk} harfli tahmin girin")
        self.giris.setDisabled(False)
        self.btn_tahmin.setDisabled(False)
        self.uyari_etiketi.hide()

        self.kutular = []
        self.kutu_container = QWidget()
        self.kutu_layout = QVBoxLayout(self.kutu_container)
        self.kutu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kutu_layout.setSpacing(10)

        for _ in range(self.tahmin_hakki):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            hbox.setSpacing(5)
            satir_kutular = []
            for _ in range(self.uzunluk):
                label = QLabel("")
                label.setFixedSize(60, 60)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
                label.setStyleSheet("""
                    background-color: lightgray; 
                    border: 2px solid #333;
                    qproperty-alignment: AlignCenter;
                """)
                hbox.addWidget(label)
                satir_kutular.append(label)
            self.kutu_layout.addLayout(hbox)
            self.kutular.append(satir_kutular)

        self.oyun_alani_layout.addWidget(self.kutu_container)
        self.oyun_alani_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def clear_game_widgets(self):
        for i in reversed(range(self.oyun_alani_layout.count())):
            widget = self.oyun_alani_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def tahmin_et(self):
        tahmin = self.giris.text().strip().upper()

        if len(tahmin) != self.uzunluk:
            self.uyari_goster(f"Lütfen {self.uzunluk} harfli bir kelime girin.")
            return

        if tahmin.lower() not in self.kelime_listesi:
            self.uyari_goster("Bu geçerli bir İngilizce kelime değil.")
            return

        if self.satir >= self.tahmin_hakki:
            return

        degerlendirme = self.degerlendir_tahmin(self.hedef_kelime, tahmin)
        for i in range(self.uzunluk):
            renk, harf = degerlendirme[i]
            label = self.kutular[self.satir][i]
            label.setText(harf)
            label.setStyleSheet(f"""
                background-color: {'green' if renk == 'green' else 'gold' if renk == 'yellow' else 'gray'};
                color: {'white' if renk != 'yellow' else 'black'}; 
                border: 2px solid black;
                qproperty-alignment: AlignCenter;
            """)

        self.satir += 1
        self.giris.clear()

        if tahmin == self.hedef_kelime:
            self.uyari_goster("🎉 Doğru bildin! Tebrikler.", bilgi=True)
            self.giris.setDisabled(True)
            self.btn_tahmin.setDisabled(True)
        elif self.satir == self.tahmin_hakki:
            self.uyari_goster(f"❌ Oyun bitti. Doğru kelime: {self.hedef_kelime}", bilgi=True)
            self.giris.setDisabled(True)
            self.btn_tahmin.setDisabled(True)

    def uyari_goster(self, mesaj, bilgi=False):
        msg_box = QMessageBox(self)
        msg_box.setText(mesaj)
        msg_box.setWindowTitle("Bilgi" if bilgi else "Uyarı")
        msg_box.setIcon(QMessageBox.Icon.Information if bilgi else QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def geri_don(self):
        self.geri_don_signal.emit()
