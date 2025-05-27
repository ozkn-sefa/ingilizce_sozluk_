import sys
import pyodbc
import secrets  # random yerine secrets modülünü kullanıyoruz
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QRadioButton,
                             QVBoxLayout, QPushButton, QButtonGroup,
                             QGroupBox, QMessageBox, QSpinBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime, timedelta


class ExamSetupWidget(QWidget):
    geri_don_signal = pyqtSignal()

    def __init__(self, main_app=None, user_id=None):
        super().__init__()
        self.main_app = main_app
        self.user_id = user_id
        print(f'ExamSetupWidget - User ID: {self.user_id}')

        with open('style\\styles8.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.selected_questions = 10
        self.current_question_index = 0
        self.conn = None
        self.cursor = None
        self.correct_answer = None
        self.asked_questions = set()
        self.correct_count = 0
        self.incorrect_count = 0
        self.correct_answers = []
        self.incorrect_answers = []

        self.init_ui()
        self.connect_to_database()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.question_count_layout = QVBoxLayout()

        self.question_count_label = QLabel('Sorulacak Soru Sayısı:', self)
        self.question_count_spinbox = QSpinBox(self)
        self.question_count_spinbox.setRange(5, 20)
        self.question_count_spinbox.setValue(5)
        self.question_count_spinbox.setFixedSize(70, 40)

        self.question_count_layout.addWidget(self.question_count_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.question_count_layout.addWidget(self.question_count_spinbox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.question_count_layout)

        self.start_button = QPushButton('Başlat', self)
        self.start_button.clicked.connect(self.start_exam)
        self.start_button.setFixedSize(150, 40)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.back_button1 = QPushButton('Geri Dön', self)
        self.back_button1.clicked.connect(self.go_back_to_main_menu)
        self.back_button1.setFixedSize(150, 40)
        self.layout.addWidget(self.back_button1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel(self)
        self.turkish_word_label = QLabel('Türkçe Kelime', self)
        self.group_box = QGroupBox(self)
        self.group_layout = QVBoxLayout()
        self.options = []
        self.button_group = QButtonGroup(self)

        for i in range(4):
            option = QRadioButton(self)
            self.button_group.addButton(option)
            self.group_layout.addWidget(option)
            self.options.append(option)

        self.group_box.setLayout(self.group_layout)

        self.answer_button = QPushButton('Cevapla', self)
        self.answer_button.setFixedSize(200, 40)
        self.answer_button.clicked.connect(self.check_answer)

        self.back_button = QPushButton('Geri Dön', self)
        self.back_button.setFixedSize(200, 40)
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        # Hide exam elements initially
        self.image_label.setVisible(False)
        self.turkish_word_label.setVisible(False)
        self.group_box.setVisible(False)
        self.answer_button.setVisible(False)
        self.back_button.setVisible(False)

        # Add widgets to main layout
        self.layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.turkish_word_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.group_box)
        self.layout.addWidget(self.answer_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def connect_to_database(self):
        if not self.conn:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=projeyazılımyapımı;Trusted_Connection=yes;'
            )
            self.cursor = self.conn.cursor()

    def close_database_connection(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.conn:
            self.conn.close()
            self.conn = None

    def start_exam(self):
        user_id = self.user_id
        today_date = datetime.now().strftime('%Y-%m-%d')

        query = "SELECT TOP 1 FORMAT(sinav_tarihi, 'yyyy-MM-dd') FROM sinavlar WHERE userid = ? ORDER BY sinav_tarihi DESC"
        self.cursor.execute(query, user_id)
        last_exam = self.cursor.fetchone()

        if last_exam and last_exam[0] == today_date:
            QMessageBox.warning(self, 'Uyarı', 'Günlük sınav hakkınızı doldurdunuz!')
            return

        self.selected_questions = self.question_count_spinbox.value()

        # Hide setup widgets
        self.start_button.setVisible(False)
        self.back_button1.setVisible(False)
        self.question_count_label.setVisible(False)
        self.question_count_spinbox.setVisible(False)

        # Show exam widgets
        self.image_label.setVisible(True)
        self.turkish_word_label.setVisible(True)
        self.group_box.setVisible(True)
        self.answer_button.setVisible(True)
        self.back_button.setVisible(True)

        # Reset counters
        self.current_question_index = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.correct_answers.clear()
        self.incorrect_answers.clear()
        self.asked_questions.clear()

        self.load_questions()

    def load_questions(self):
        self.cursor.execute('SELECT kelimeid, kelime_ingilizce, kelime_turkce, kelime_resimyolu FROM kelimeler')
        rows = self.cursor.fetchall()

        if len(rows) < 4:
            QMessageBox.warning(self, 'Hata', 'Yeterli veri yok! En az 4 kelime ekleyin.')
            return

        today = datetime.now().date()

        # Daha önce sorulan kelimeleri filtrele
        available_words = [row for row in rows if row[0] not in self.asked_questions]

        if not available_words:
            self.show_results()
            return

        # Güvenli rastgele seçim yap
        row = secrets.choice(available_words)
        word_id = row[0]

        # Kullanıcının bu kelimeyi bilip bilmediğini kontrol et
        self.cursor.execute(
            'SELECT biliyor_mu FROM ogrenilen_kelimeler WHERE userid = ? AND kelimeid = ?',
            (self.user_id, word_id)
        )
        result = self.cursor.fetchone()

        if result and result[0]:
            self.cursor.execute(
                'SELECT sorulma_serisi, son_test_tarihi FROM kelime_ilerleme WHERE userid = ? AND kelimeid = ?',
                (self.user_id, word_id)
            )
            progress = self.cursor.fetchone()

            if progress:
                sorulma_serisi, son_test_tarihi = progress
                test_intervals = [0, 1, 7, 30, 90, 180, 365]

                if sorulma_serisi < len(test_intervals):
                    required_date = (
                            datetime.strptime(son_test_tarihi, '%Y-%m-%d').date() +
                            timedelta(days=test_intervals[sorulma_serisi])
                    )

                    if today < required_date:
                        self.asked_questions.add(word_id)
                        return self.load_questions()

        self.asked_questions.add(word_id)
        turkish_word = row[2]
        english_word = row[1]
        image_path = row[3]

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(
                300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.image_label.clear()

        self.turkish_word_label.setText(turkish_word)
        self.correct_answer = english_word

        random_answers = [english_word]
        wrong_answers = [r[1] for r in rows if r[1] != english_word]


        random_answers.extend(secrets.SystemRandom().sample(wrong_answers, min(3, len(wrong_answers)))) # NOSONAR


        secrets.SystemRandom().shuffle(random_answers) # NOSONAR

        self.button_group.setExclusive(False)
        for i, option in enumerate(self.options):
            option.setText(random_answers[i])
            option.setChecked(False)
        self.button_group.setExclusive(True)

        self.current_question_index += 1

    def check_answer(self):
        selected_answer = None
        for option in self.options:
            if option.isChecked():
                selected_answer = option.text()
                break

        if selected_answer == self.correct_answer:
            self.correct_count += 1
            self.correct_answers.append(
                f"{self.turkish_word_label.text()} - {self.correct_answer}")
        else:
            self.incorrect_count += 1
            self.incorrect_answers.append(
                f"{self.turkish_word_label.text()} - {self.correct_answer}")

        # Soru sayısı kontrolü (current_question_index 1'den başlıyor)
        if self.current_question_index >= self.selected_questions:
            self.show_results()
        else:
            self.load_questions()

    def show_results(self):
        correct_words = '\n'.join(self.correct_answers) if self.correct_answers else "Hiç doğru cevap yok."
        incorrect_words = '\n'.join(self.incorrect_answers) if self.incorrect_answers else "Hiç yanlış cevap yok."

        result_message = (
            f'Doğru: {self.correct_count}\n'
            f'Yanlış: {self.incorrect_count}\n\n'
            f'Doğru Cevaplanan Kelimeler:\n{correct_words}\n\n'
            f'Yanlış Cevaplanan Kelimeler:\n{incorrect_words}\n\n'
            f'Sınavınız kaydedildi.'
        )

        try:
            self.save_exam_results()
            QMessageBox.information(self, 'Sonuçlar', result_message)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Sınav kaydedilirken hata oluştu: {str(e)}')
        finally:
            self.go_back_to_main_menu()

    def save_exam_results(self):
        if not self.user_id:
            QMessageBox.warning(self, 'Hata', 'Kullanıcı ID bulunamadı! Lütfen tekrar giriş yapın.')
            return

        today = datetime.today().strftime('%Y-%m-%d')

        try:
            # Check exam count
            self.cursor.execute(
                'SELECT COUNT(*) FROM sinavlar WHERE userid = ?',
                (self.user_id,)
            )
            sinav_sayisi = self.cursor.fetchone()[0]

            # Keep only last 5 exams
            if sinav_sayisi >= 5:
                self.cursor.execute(
                    'DELETE FROM sinavlar WHERE sinav_id IN ('
                    'SELECT TOP 1 sinav_id FROM sinavlar '
                    'WHERE userid = ? '
                    'ORDER BY sinav_id ASC'
                    ')',
                    (self.user_id,)
                )
                self.conn.commit()

            # Insert new exam and get inserted ID
            self.cursor.execute(
                'INSERT INTO sinavlar (userid, sinav_tarihi) '
                'OUTPUT INSERTED.sinav_id '
                'VALUES (?, ?)',
                (self.user_id, today)
            )
            sinav_id_row = self.cursor.fetchone()

            if not sinav_id_row:
                QMessageBox.warning(self, 'Hata', 'Sınav ID alınamadı! İşlem iptal edildi.')
                return

            sinav_id = sinav_id_row[0]
            self.conn.commit()

            # Save results
            for answer, is_correct in (
                    [(word, 1) for word in self.correct_answers] +
                    [(word, 0) for word in self.incorrect_answers]):

                turkish_word, correct_word = answer.split(' - ')

                # Get word ID
                self.cursor.execute(
                    'SELECT kelimeid FROM kelimeler '
                    'WHERE kelime_turkce = ? AND kelime_ingilizce = ?',
                    (turkish_word, correct_word)
                )
                kelimeid_row = self.cursor.fetchone()

                if not kelimeid_row:
                    continue

                kelimeid = kelimeid_row[0]

                # Save answer
                self.cursor.execute(
                    'INSERT INTO sonuclar (sinav_id, kelimeid, dogru_mu) '
                    'VALUES (?, ?, ?)',
                    (sinav_id, kelimeid, is_correct)
                )

                # Update progress
                self.cursor.execute(
                    'SELECT dogru_sayisi, sorulma_serisi '
                    'FROM kelime_ilerleme '
                    'WHERE userid = ? AND kelimeid = ?',
                    (self.user_id, kelimeid)
                )
                ilerleme_row = self.cursor.fetchone()

                if ilerleme_row:
                    current_count, sorulma_serisi = ilerleme_row
                    new_count = current_count + 1 if is_correct else 0
                    new_seri = sorulma_serisi + 1 if is_correct else 0

                    self.cursor.execute(
                        'UPDATE kelime_ilerleme '
                        'SET dogru_sayisi = ?, sorulma_serisi = ?, son_test_tarihi = ? '
                        'WHERE userid = ? AND kelimeid = ?',
                        (new_count, new_seri, today, self.user_id, kelimeid)
                    )
                else:
                    self.cursor.execute(
                        'INSERT INTO kelime_ilerleme '
                        '(userid, kelimeid, dogru_sayisi, sorulma_serisi, son_test_tarihi) '
                        'VALUES (?, ?, ?, ?, ?)',
                        (self.user_id, kelimeid, 1 if is_correct else 0, 1 if is_correct else 0, today)
                    )

                # Mark as learned if answered correctly 6 times
                if is_correct:
                    self.cursor.execute(
                        'SELECT dogru_sayisi '
                        'FROM kelime_ilerleme '
                        'WHERE userid = ? AND kelimeid = ?',
                        (self.user_id, kelimeid)
                    )
                    new_count_row = self.cursor.fetchone()

                    if new_count_row and new_count_row[0] >= 6:
                        self.cursor.execute(
                            'MERGE ogrenilen_kelimeler AS target '
                            'USING (SELECT ? AS userid, ? AS kelimeid) AS source '
                            'ON (target.userid = source.userid AND target.kelimeid = source.kelimeid) '
                            'WHEN MATCHED THEN '
                            '    UPDATE SET biliyor_mu = 1 '
                            'WHEN NOT MATCHED THEN '
                            '    INSERT (userid, kelimeid, biliyor_mu) VALUES (?, ?, 1);',
                            (self.user_id, kelimeid, self.user_id, kelimeid)
                        )

            self.conn.commit()
            return True

        except pyodbc.Error as e:
            QMessageBox.critical(
                self,
                'Veritabanı Hatası',
                f'Sınav kaydedilirken hata oluştu:\n{str(e)}'
            )
            self.conn.rollback()
            return False

    def go_back_to_main_menu(self):
        self.geri_don_signal.emit()

    def closeEvent(self, event):
        self.close_database_connection()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExamSetupWidget()
    window.show()
    sys.exit(app.exec())