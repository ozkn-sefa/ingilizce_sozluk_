import os
import sys
import pyodbc
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class RaporWidget(QWidget):
    geri_don_signal = pyqtSignal()

    def __init__(self, main_app=None, user_id=None):
        super().__init__()
        self.layout = QVBoxLayout()
        self.main_app = main_app
        self.user_id = user_id

        # Stil dosyasını yükle
        with open('style\\styles7.qss', 'r') as f:
            self.setStyleSheet(f.read())

        # Font kaydı (DejaVu Sans örneği)
        font_path = os.path.join('fonts', 'DejaVuSans.ttf')
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
        except Exception as e:
            print(f"Font yükleme hatası: {e}")
            # Hata durumunda varsayılan bir font kullanabilirsiniz.
            pdfmetrics.registerFont(pdfmetrics.Font('Helvetica', 'Helvetica', 'WinAnsiEncoding'))

        # Widget'ları oluştur
        self.label_info = QLabel('')
        self.label_info.setVisible(False)
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_ogrenilen_kelimeler = QPushButton('Öğrenilen Kelimeler')
        self.btn_ogrenilen_kelimeler.setFixedSize(250, 40)
        self.btn_ogrenilen_kelimeler.clicked.connect(self.show_ogrenilen_kelimeler)

        self.btn_kelime_ilerleme = QPushButton('Kelime İlerleme Durumu')
        self.btn_kelime_ilerleme.setFixedSize(250, 40)
        self.btn_kelime_ilerleme.clicked.connect(self.show_kelime_ilerleme)

        self.btn_sinav_sonuclari = QPushButton('Sınav Sonuçları')
        self.btn_sinav_sonuclari.setFixedSize(250, 40)
        self.btn_sinav_sonuclari.clicked.connect(self.show_sinav_sonuclari)

        self.btn_geri_don1 = QPushButton('Geri Dön')
        self.btn_geri_don1.setFixedSize(250, 40)
        self.btn_geri_don1.clicked.connect(self.show_main1)
        self.btn_geri_don1.setVisible(False)

        self.btn_ana_menu1 = QPushButton('Geri Dön')
        self.btn_ana_menu1.setFixedSize(250, 40)
        self.btn_ana_menu1.clicked.connect(self.return_to_menu1)

        self.btn_pdf_ogrenilen = QPushButton('Öğrenilen Kelimeler PDF')
        self.btn_pdf_ogrenilen.setFixedSize(250, 40)
        self.btn_pdf_ogrenilen.clicked.connect(self.save_ogrenilen_pdf)
        self.btn_pdf_ogrenilen.setVisible(False)

        self.btn_pdf_ilerleme = QPushButton('Kelime İlerleme PDF')
        self.btn_pdf_ilerleme.setFixedSize(250, 40)
        self.btn_pdf_ilerleme.clicked.connect(self.save_kelime_ilerleme_pdf)
        self.btn_pdf_ilerleme.setVisible(False)

        self.btn_pdf_sinav_sonuclari = QPushButton('Sınav Sonuçları PDF')
        self.btn_pdf_sinav_sonuclari.setFixedSize(250, 40)
        self.btn_pdf_sinav_sonuclari.clicked.connect(self.save_sinav_sonuclari_pdf)
        self.btn_pdf_sinav_sonuclari.setVisible(False)

        self.table = QTableWidget()
        self.table.setVisible(False)

        # Layout'a widget'ları ekle
        self.layout.addWidget(self.label_info)
        self.layout.addWidget(self.table)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.btn_ogrenilen_kelimeler, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.btn_kelime_ilerleme, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.btn_sinav_sonuclari, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.btn_pdf_ogrenilen, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.btn_pdf_ilerleme, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.btn_pdf_sinav_sonuclari, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.btn_geri_don1, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.btn_ana_menu1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def show_sinav_sonuclari(self):
        sonuclar = self.get_sinav_sonuclari()
        if not sonuclar:
            self.label_info.setText('Hiç sınav sonucu bulunamadı!')
            self.label_info.setVisible(True)
            self.table.setVisible(False)
            self.btn_pdf_sinav_sonuclari.setVisible(False)
            self.btn_geri_don1.setVisible(True)
        else:
            self.label_info.setVisible(False)
            self.table.setRowCount(len(sonuclar))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(
                ['Sınav ID', 'Sınav Tarihi', 'Türkçe Kelime', 'İngilizce Kelime', 'Sonuç'])


            for i, sonuc in enumerate(sonuclar):
                for j, veri in enumerate(sonuc):
                    self.table.setItem(i, j, QTableWidgetItem(str(veri)))

            self.table.setVisible(True)
            self.btn_pdf_sinav_sonuclari.setVisible(True)
            self.btn_geri_don1.setVisible(True)

        self.btn_kelime_ilerleme.setVisible(False)
        self.btn_ana_menu1.setVisible(False)
        self.btn_ogrenilen_kelimeler.setVisible(False)
        self.btn_sinav_sonuclari.setVisible(False)

    def get_sinav_sonuclari(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')
            cursor = conn.cursor()

            sorgu = """
                SELECT s.sinav_id, s.sinav_tarihi, k.kelime_turkce, k.kelime_ingilizce,
                       CASE WHEN sn.dogru_mu = 1 THEN 'Doğru' ELSE 'Yanlış' END AS sonuc
                FROM sinavlar s
                JOIN sonuclar sn ON s.sinav_id = sn.sinav_id
                JOIN kelimeler k ON sn.kelimeid = k.kelimeid
                WHERE s.userid = ?
                ORDER BY s.sinav_tarihi DESC, s.sinav_id ASC
            """
            cursor.execute(sorgu, self.user_id)
            return cursor.fetchall()
        except pyodbc.Error as e:
            print('Veritabanı bağlantı hatası:', e)
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    def show_main1(self):
        self.table.setVisible(False)
        self.label_info.setVisible(False)
        self.btn_geri_don1.setVisible(False)
        self.btn_pdf_ogrenilen.setVisible(False)
        self.btn_pdf_ilerleme.setVisible(False)
        self.btn_pdf_sinav_sonuclari.setVisible(False)

        self.btn_kelime_ilerleme.setVisible(True)
        self.btn_ana_menu1.setVisible(True)
        self.btn_ogrenilen_kelimeler.setVisible(True)
        self.btn_sinav_sonuclari.setVisible(True)

        self.layout.update()

    def save_sinav_sonuclari_pdf(self):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()

        if row_count == 0 or column_count == 0:
            QMessageBox.warning(self, 'PDF Kaydı', 'Tabloda hiçbir veri yok!')
            return

        pdf_klasor = 'pdfs'
        if not os.path.exists(pdf_klasor):
            os.makedirs(pdf_klasor)

        pdf_dosya = os.path.join(pdf_klasor, 'Sinav_Sonuclari.pdf')
        c = canvas.Canvas(pdf_dosya, pagesize=A4)
        width, height = A4

        c.setFont('DejaVuSans', 12)
        c.drawString(100, height - 50, 'Sınav Sonuçları')

        y = height - 80
        # Başlıklar
        c.drawString(50, y, 'Sınav Tarihi')
        c.drawString(150, y, 'Sınav ID')
        c.drawString(250, y, 'Türkçe Kelime')
        c.drawString(400, y, 'İngilizce Kelime')
        c.drawString(550, y, 'Sonuç')
        y -= 20

        # Verileri sınav ID'ye göre grupla
        sinav_id_prev = None
        for row in range(row_count):
            sinav_tarihi = self.table.item(row, 0).text()
            sinav_id = self.table.item(row, 1).text()
            kelime_turkce = self.table.item(row, 2).text()
            kelime_ingilizce = self.table.item(row, 3).text()
            sonuc = self.table.item(row, 4).text()

            # Eğer sınav ID değiştiyse, çizgi çek ve y'yi biraz azalt
            if sinav_id_prev is not None and sinav_id != sinav_id_prev:
                c.line(45, y + 10, width - 45, y + 10)  # yatay çizgi
                y -= 30  # çizgi sonrası biraz boşluk

                # Yeni sınav başlığı olarak sınav ID veya ekstra bilgi yazmak isterseniz buraya ekleyebilirsiniz
                # Örnek: c.drawString(50, y, f"Sınav ID: {sinav_id}")
                # y -= 20

            # Satırları yazdır
            c.drawString(50, y, sinav_tarihi)
            c.drawString(150, y, sinav_id)
            c.drawString(250, y, kelime_turkce)
            c.drawString(400, y, kelime_ingilizce)
            c.drawString(550, y, sonuc)
            y -= 20

            # Sayfa sonuna yaklaşılırsa yeni sayfa
            if y < 50:
                c.showPage()
                c.setFont('DejaVuSans', 12)
                y = height - 80
                # Başlıkları yeni sayfada tekrar yaz
                c.drawString(50, y, 'Sınav Tarihi')
                c.drawString(150, y, 'Sınav ID')
                c.drawString(250, y, 'Türkçe Kelime')
                c.drawString(400, y, 'İngilizce Kelime')
                c.drawString(550, y, 'Sonuç')
                y -= 20

            sinav_id_prev = sinav_id

        # Son grubun altına çizgi çek
        c.line(45, y + 10, width - 45, y + 10)
        y -= 40

        username = self.get_username()
        c.drawString(70, y, f'{username}')

        c.save()
        QMessageBox.information(self, 'PDF Kaydedildi', f"PDF '{pdf_dosya}' olarak kaydedildi.")

    def get_ogrenilen_kelimeler(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')
            cursor = conn.cursor()

            sorgu = """
                SELECT k.kelime_turkce, k.kelime_ingilizce
                FROM kelimeler k
                JOIN ogrenilen_kelimeler d ON k.kelimeid = d.kelimeid
                WHERE d.userid = ? AND d.biliyor_mu = 1
                ORDER BY k.kelimeid ASC
            """
            cursor.execute(sorgu, self.user_id)
            return cursor.fetchall()
        except pyodbc.Error as e:
            print('Veritabanı bağlantı hatası:', e)
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    def show_ogrenilen_kelimeler(self):
        kelimeler = self.get_ogrenilen_kelimeler()
        if not kelimeler:
            self.label_info.setText('Hiç öğrenilen kelime bulunamadı!')
            self.label_info.setVisible(True)
            self.table.setVisible(False)
            self.btn_pdf_ogrenilen.setVisible(False)
            self.btn_sinav_sonuclari.setVisible(False)
            self.btn_geri_don1.setVisible(True)
        else:
            self.label_info.setVisible(False)
            self.table.setRowCount(len(kelimeler))
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(['Türkçe Kelime', 'İngilizce Kelime'])

            for i, kelime in enumerate(kelimeler):
                self.table.setItem(i, 0, QTableWidgetItem(str(kelime[0])))
                self.table.setItem(i, 1, QTableWidgetItem(str(kelime[1])))

            self.table.setColumnWidth(0, 250)
            self.table.setColumnWidth(1, 250)
            self.table.setVisible(True)
            self.btn_pdf_ogrenilen.setVisible(True)
            self.btn_geri_don1.setVisible(True)
            self.btn_pdf_ilerleme.setVisible(False)

        self.btn_kelime_ilerleme.setVisible(False)
        self.btn_ogrenilen_kelimeler.setVisible(False)
        self.btn_sinav_sonuclari.setVisible(False)
        self.btn_ana_menu1.setVisible(False)

    def show_kelime_ilerleme(self):
        kelimeler = self.get_kelime_ilerleme()
        all_kelimeler = self.get_all_kelimeler()

        if not all_kelimeler:
            self.label_info.setText('Kelime ilerleme verisi bulunamadı!')
            self.label_info.setVisible(True)
            self.btn_geri_don1.setVisible(True)
            self.table.setVisible(False)
            self.btn_pdf_ilerleme.setVisible(False)
            self.btn_sinav_sonuclari.setVisible(False)
        else:
            self.label_info.setVisible(False)
            self.table.setRowCount(len(all_kelimeler))
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(['Türkçe Kelime', 'İngilizce Kelime', 'Öğrenilme Durumu (%)'])

            for i, kelime in enumerate(all_kelimeler):
                kelime_turkce = kelime[0]
                kelime_ingilizce = kelime[1]

                ilerleme = next((item for item in kelimeler if item[0] == kelime_turkce), None)

                if ilerleme:
                    dogru_sayisi = ilerleme[2]
                    ogrenme_yuzdesi = int((dogru_sayisi / 6) * 100)
                else:
                    ogrenme_yuzdesi = 0

                self.table.setItem(i, 0, QTableWidgetItem(str(kelime_turkce)))
                self.table.setItem(i, 1, QTableWidgetItem(str(kelime_ingilizce)))
                self.table.setItem(i, 2, QTableWidgetItem(f'{ogrenme_yuzdesi}%'))

            self.table.setColumnWidth(2, 150)
            self.table.setColumnWidth(1, 150)
            self.table.setColumnWidth(0, 150)
            self.table.setVisible(True)
            self.btn_pdf_ogrenilen.setVisible(False)
            self.btn_pdf_ilerleme.setVisible(True)
            self.btn_geri_don1.setVisible(True)

        self.btn_kelime_ilerleme.setVisible(False)
        self.btn_ogrenilen_kelimeler.setVisible(False)
        self.btn_sinav_sonuclari.setVisible(False)
        self.btn_ana_menu1.setVisible(False)

    def get_kelime_ilerleme(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')
            cursor = conn.cursor()

            sorgu = """
                SELECT k.kelime_turkce, k.kelime_ingilizce, d.dogru_sayisi
                FROM kelimeler k
                JOIN kelime_ilerleme d ON k.kelimeid = d.kelimeid
                WHERE d.userid = ?
            """
            cursor.execute(sorgu, self.user_id)
            return cursor.fetchall()
        except pyodbc.Error as e:
            print('Veritabanı bağlantı hatası:', e)
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    def get_all_kelimeler(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')
            cursor = conn.cursor()

            sorgu = 'SELECT kelime_turkce, kelime_ingilizce FROM kelimeler ORDER BY kelimeid ASC'
            cursor.execute(sorgu)
            return cursor.fetchall()
        except pyodbc.Error as e:
            print('Veritabanı bağlantı hatası:', e)
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    def save_kelime_ilerleme_pdf(self):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()

        if row_count == 0 or column_count == 0:
            QMessageBox.warning(self, 'PDF Kaydı', 'Tabloda hiçbir veri yok!')
            return

        pdf_klasor = 'pdfs'
        if not os.path.exists(pdf_klasor):
            os.makedirs(pdf_klasor)

        pdf_dosya = os.path.join(pdf_klasor, 'Kelime_Ilerleme_Durumu.pdf')
        c = canvas.Canvas(pdf_dosya, pagesize=A4)
        width, height = A4

        c.setFont('DejaVuSans', 12)
        c.drawString(100, height - 50, 'Kelime İlerleme Durumu')

        y = height - 80
        c.drawString(100, y, 'Türkçe Kelime')
        c.drawString(250, y, 'İngilizce Kelime')
        c.drawString(400, y, 'Öğrenilme Durumu (%)')
        y -= 20

        for row in range(row_count):
            kelime_turkce = self.table.item(row, 0).text()
            kelime_ingilizce = self.table.item(row, 1).text()
            ogrenme_yuzdesi = self.table.item(row, 2).text()

            c.drawString(100, y, kelime_turkce)
            c.drawString(250, y, kelime_ingilizce)
            c.drawString(400, y, ogrenme_yuzdesi)
            y -= 20

            if y < 50:
                c.showPage()
                c.setFont('DejaVuSans', 12)
                y = height - 80

        y -= 40
        username = self.get_username()
        c.drawString(100, y, f'{username}')

        c.save()
        QMessageBox.information(self, 'PDF Kaydedildi', f"PDF '{pdf_dosya}' olarak kaydedildi.")

    def save_ogrenilen_pdf(self):
        kelimeler = self.get_ogrenilen_kelimeler()
        if not kelimeler:
            QMessageBox.warning(self, 'PDF Kaydı', 'Öğrenilen kelime bulunamadı!')
            return

        pdf_klasor = 'pdfs'
        if not os.path.exists(pdf_klasor):
            os.makedirs(pdf_klasor)

        pdf_dosya = os.path.join(pdf_klasor, 'Ogrenilen_Kelimeler.pdf')
        c = canvas.Canvas(pdf_dosya, pagesize=A4)

        c.setFont('DejaVuSans', 12)
        c.drawString(100, 800, 'Öğrenilen Kelimeler')

        y = 780
        c.drawString(100, y, 'Türkçe Kelime')
        c.drawString(250, y, 'İngilizce Kelime')
        y -= 20

        for turkce, ingilizce in kelimeler:
            c.drawString(100, y, turkce)
            c.drawString(250, y, ingilizce)
            y -= 20

        y -= 40
        username = self.get_username()
        c.drawString(100, y, f'{username}')

        c.save()
        QMessageBox.information(self, 'PDF Kaydedildi', f"PDF '{pdf_dosya}' olarak kaydedildi.")

    def get_username(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;')
            cursor = conn.cursor()

            sorgu = 'SELECT username FROM users WHERE userid = ?'
            cursor.execute(sorgu, self.user_id)
            username = cursor.fetchone()

            if username:
                return username[0]
            return 'Kullanıcı Adı Bulunamadı'
        except pyodbc.Error as e:
            print('Veritabanı bağlantı hatası:', e)
            return 'Veritabanı hatası'
        finally:
            if 'conn' in locals():
                conn.close()

    def return_to_menu1(self):
        print('Ana Menüye dönülüyor...')
        self.btn_ogrenilen_kelimeler.setVisible(False)
        self.btn_kelime_ilerleme.setVisible(False)
        self.btn_ana_menu1.setVisible(False)
        self.geri_don_signal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RaporWidget()
    window.show()
    sys.exit(app.exec())