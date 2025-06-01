# İngilizce Kelime Öğrenme Uygulaması

Bu, İngilizce kelime öğrenme sürecini kolaylaştırmak için tasarlanmış, PyQt6 tabanlı bir masaüstü uygulamasıdır. Kullanıcılar bu uygulama ile kelime ekleyebilir, sınavlara katılabilir, ilerlemelerini takip edebilir ve çeşitli öğrenme araçlarını kullanabilir.

## Özellikler

### Kullanıcı Yönetimi
- **Kayıt Olma ve Giriş Yapma**: Yeni hesap oluşturun veya mevcut hesabınızla giriş yapın.
- **Şifre Sıfırlama**: Şifrenizi güvenli bir şekilde sıfırlayın.

### Kelime Yönetimi
- **Yeni Kelime Ekleme**: Kişisel kelime havuzunuza yeni kelimeler ekleyin.
- **Kelime Havuzunu Görüntüleme**: Kelime koleksiyonunuzu görüntüleyin ve yönetin.
- **Resimli Kelime Öğrenme**: Kelimeleri görsellerle öğrenerek daha iyi hatırlayın.

### Sınav Modülü
- **Çoktan Seçmeli Sınavlar**: Bilginizi interaktif sınavlarla test edin.
- **Günlük Sınav Limiti**: Düzenli öğrenmeyi teşvik etmek için günde bir sınav.
- **Akıllı Tekrar Algoritması**: Kelimeleri öğrenme durumunuza göre tekrar edin.

### Raporlama
- **Öğrenilen Kelimeler Listesi**: Öğrendiğiniz kelimeleri listeleyin.
- **Öğrenme İlerleme Durumu**: Kelime öğrenme sürecinizdeki ilerlemeyi takip edin.
- **Sınav Sonuçları**: Sınav performansınızı inceleyin.
- **PDF Raporlar**: İlerlemenizi ve sonuçlarınızı PDF olarak dışa aktarın.

### Eğlenceli Öğrenme Araçları
- **Wordle Benzeri Kelime Bulmacası**: Wordle'dan ilham alan eğlenceli bir oyunla öğrenin.
- **Yapay Zeka Destekli Hikaye Oluşturucu**: Kelimelerinizle yapay zeka destekli hikayeler oluşturun.

### Ayarlar
- **Uygulama Bilgileri**: Uygulama hakkında detaylara erişin.
- **Kelime Havuzu Görüntüleme**: Kelime havuzunuzu nasıl görüntüleyeceğinizi özelleştirin.

## Teknik Gereksinimler

### Nasıl Çalıştırılır
  - Proje klasorundeki dist dosyasında .exe formatında bulunuyor veritabanı kurulumlarını yaptıktan sonra direkt oradan çalıştırabilirsiniz ama geliştirci veya proje üzerinde değişiklikler yapmak için gerekli şeyleri aşağıda bulabilirsiniz. 
### Yazılım Gereksinimleri
- **Python**: Sürüm 3.9 veya üzeri
- **Kütüphaneler**:
  - PyQt6
  - pyodbc (SQL Server bağlantısı için)
  - requests (yapay zeka entegrasyonu için)
  - python-dotenv (ortam değişkenleri için)
  - reportlab (PDF oluşturma için)

Gerekli kütüphaneleri kurmak için:
```bash
pip install pyqt6 pyodbc requests python-dotenv reportlab
```

### Donanım Gereksinimleri
- **İşletim Sistemi**: Windows (SQL Server bağlantısı için)
- **RAM**: En az 4GB
- **Disk Alanı**: En az 500MB boş alan

### Veritabanı Gereksinimleri
- **Veritabanı**: Microsoft SQL Server
- **Veritabanı Adı**: `projeyazılımyapımı`
- **Tablolar**: Veritabanı Kurulumu bölümünde belirtildiği şekilde oluşturulmalıdır.

## Kurulum Talimatları

### 1. Python ve Kütüphane Kurulumu
Gerekli Python kütüphanelerini kurun:
```bash
pip install pyqt6 pyodbc requests python-dotenv reportlab
```

### 2. Veritabanı Kurulumu
1. Microsoft SQL Server'da `projeyazılımyapımı` adında bir veritabanı oluşturun.
2. Gerekli tabloları proje de bulunan database klasorundeki veritabanı dosylarını kopyalayıp ,oluşturduğunuz veritabanı dosyaları ile değiştirin.
3. Veritabanı bağlantısını localhost üzerinden yapınız aksi takdirde uygulama veritabanına bağlanmayabilir.

### 3. Yapay Zeka Entegrasyonu (Hikaye Oluşturucu)
1. [OpenRouter.ai](https://openrouter.ai) adresinde bir hesap oluşturun ve Deepseek R1 Zero(Free) modeli için API anahtarı alın.
2. Proje kök dizininde `.env` dosyası oluşturun ve şu satırı ekleyin:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

### 4. Dosya Yapısı Kurulumu
Proje kök dizininde şu klasörleri oluşturun:
- `style/` - QSS stil dosyaları için
- `presim/` - Uygulama ikonları için
- `pdfs/` - Oluşturulan PDF raporlar için
- `fonts/` - PDF'lerde kullanılacak yazı tipleri için (`DejaVuSans.ttf` dahil olmalı)
- `veri/` - Kelime listeleri için

## Kullanım Kılavuzu

### Başlangıç
1. Uygulamayı `main.py` dosyasını çalıştırarak başlatın:
   ```bash
   python main.py
   ```
2. **Yeni Kullanıcılar**: "Kaydol" butonuna tıklayarak hesap oluşturun.
3. **Mevcut Kullanıcılar**: Kimlik bilgilerinizle giriş yapın.

### Ana Menü
- **Kelime Ekle**: Kelime havuzunuza yeni kelimeler ekleyin.
- **Sınav**: Günlük sınavla bilginizi test edin.
- **Bulmaca**: Wordle benzeri oyunla eğlenerek öğrenin.
- **Hikaye**: Kelimelerinizle yapay zeka destekli hikayeler oluşturun.
- **Rapor**: Öğrenme ilerlemenizi görüntüleyin ve dışa aktarın.
- **Ayarlar**: Uygulama ayarlarını yönetin.

### Önemli Notlar
- Günde **yalnızca bir sınav** hakkınız vardır.
- Bir kelimeyi tam öğrenmek için **6 kez doğru cevaplamanız** gerekir.
- PDF raporlar `pdfs/` klasörüne kaydedilir.

## Geliştirici Notları
- **Veritabanı Bağlantıları**: Bağlantı dizeleri kod içinde sabit olarak ayarlanmıştır.
- **Güvenlik**: Şifreler SHA-256 ile hashlenmektedir.
- **Rastgele Seçim**: Güvenli rastgele seçimler için `secrets` modülü kullanılmıştır.
- **Kullanıcı Arayüzü**: PyQt6 ile sağlam bir masaüstü deneyimi sunulmuştur.

## Bilinen Sorunlar ve Çözümleri

### SQL Server Bağlantı Sorunları
- **Çözüm**:
  - Kod içindeki bağlantı dizesini kontrol edin.
  - SQL Server'ın çalıştığından emin olun.
  - Windows Kimlik Doğrulaması kullanıyorsanız gerekli izinleri kontrol edin.

### PDF Oluşturma Hataları
- **Çözüm**:
  - `fonts/` klasöründe `DejaVuSans.ttf` dosyasının bulunduğunu doğrulayın.
  - `pdfs/` klasörünün yazılabilir olduğunu kontrol edin.

### Yapay Zeka Hikaye Oluşturucu Çalışmıyor
- **Çözüm**:
  - `.env` dosyasındaki `OPENROUTER_API_KEY` anahtarını kontrol edin.
  - İnternet bağlantınızı doğrulayın.


