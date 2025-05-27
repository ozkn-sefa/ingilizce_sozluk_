import requests
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTextEdit, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class HikayeWidget(QWidget):
    geri_don_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)  # Reduced spacing between widgets
        # Stil dosyasını yükle
        with open('style\\styles10.qss', 'r') as f:
            self.setStyleSheet(f.read())

        # Hikaye gösterim alanı (üste)
        self.hikaye_alan = QTextEdit(self)
        self.hikaye_alan.setReadOnly(True)
        self.hikaye_alan.setMinimumHeight(350)  # Increased height slightly
        self.main_layout.addWidget(self.hikaye_alan, stretch=1)  # Allow it to expand

        # Orta kısım için dikey hizalama
        self.center_layout = QVBoxLayout()
        self.center_layout.setSpacing(8)  # Reduced spacing
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Bilgilendirici metin (merkezde)
        self.label = QLabel("Lütfen virgül ile ayırarak kelimeleri girin:", self)
        self.label.setFont(QFont("Arial", 12))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.center_layout.addWidget(self.label)

        # Kelime girişi (genişletilmiş ve merkezde)
        self.kelime_input = QLineEdit(self)
        self.kelime_input.setPlaceholderText("kelime1, kelime2, kelime3")
        self.kelime_input.setMinimumWidth(500)
        self.kelime_input.setMaximumWidth(800)
        self.center_layout.addWidget(self.kelime_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Butonlar için yatay layout (daha compact)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(10)  # Reduced button spacing

        # Hikaye oluştur butonu
        self.hikaye_olustur_btn = QPushButton("Hikaye Oluştur", self)
        self.hikaye_olustur_btn.setFixedSize(250, 40)  # Slightly smaller height
        self.hikaye_olustur_btn.clicked.connect(self.hikaye_olustur)
        self.buttons_layout.addWidget(self.hikaye_olustur_btn)

        # Geri dön butonu
        self.geri_don_btn = QPushButton("Geri Dön", self)
        self.geri_don_btn.setFixedSize(250, 40)  # Slightly smaller height
        self.geri_don_btn.clicked.connect(self.geri_don)
        self.buttons_layout.addWidget(self.geri_don_btn)

        self.center_layout.addLayout(self.buttons_layout)
        self.main_layout.addLayout(self.center_layout)

        # Set margins to reduce empty space around edges
        self.main_layout.setContentsMargins(20, 15, 20, 15)

    def hikaye_olustur(self):
        user_input = self.kelime_input.text().strip()
        if not user_input:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir kelime girin.")
            return

        user_words = [w.strip() for w in user_input.split(",") if w.strip()]
        prompt = f"Aşağıdaki kelimeleri kullanarak yaratıcı hikaye yaz: {', '.join(user_words)}. Hikaye Türkçe olsun. Sadece hikaye olsun başlık felan koyma."

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            QMessageBox.critical(self, "Hata", "API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.")
            return

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://openrouter.ai",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek/deepseek-r1-zero:free",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15
            )
            response.raise_for_status()
            story = response.json()['choices'][0]['message']['content']

            if len(story) > 8:
                modified_story = story[7:-1]
            else:
                modified_story = story

            self.hikaye_alan.setPlainText(modified_story.strip())

        except requests.exceptions.Timeout:
            QMessageBox.critical(self, "Hata", "İstek zaman aşımına uğradı. Lütfen tekrar deneyin.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")
        finally:
            if 'response' in locals():
                response.close()

    def geri_don(self):
        self.geri_don_signal.emit()

    def clear(self):
        self.kelime_input.clear()
        self.hikaye_alan.clear()

    def closeEvent(self, event):
        self.clear()
        super().closeEvent(event)