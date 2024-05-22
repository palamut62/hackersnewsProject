# HackersNewsProject

## Proje Açıklaması
HackersNewsProject, Django framework'ü kullanılarak geliştirilmiş bir haber sitesi uygulamasıdır. Kullanıcılar, haberleri görüntüleyebilir, yorum yapabilir ve haberleri değerlendirebilir.

## Özellikler
- Kullanıcı Kayıt ve Giriş Sistemi
- Haber Listesi ve Detay Sayfaları
- Yorum Yapma ve Yorumları Görüntüleme
- Haber Değerlendirme Sistemi
- SSS (Sıkça Sorulan Sorular) Sayfası

## Kurulum

### Gereksinimler
- Python 3.x
- Django 3.x veya üzeri

### Adımlar
1. Bu depoyu yerel makinenize klonlayın:
   ```sh
   git clone https://github.com/palamut62/hackersnewsProject.git
   ```
2. Proje dizinine gidin:
   ```sh
   cd hackersnewsProject
   ```
3. Sanal ortam oluşturun ve etkinleştirin:
   ```sh
   python -m venv venv
   source venv/bin/activate   # Windows için: venv\Scripts\activate
   ```
4. Gerekli paketleri yükleyin:
   ```sh
   pip install -r requirements.txt
   ```
5. Veritabanını oluşturun ve gerekli migrasyonları uygulayın:
   ```sh
   python manage.py migrate
   ```
6. Yönetici hesabı oluşturun:
   ```sh
   python manage.py createsuperuser
   ```
7. Geliştirme sunucusunu başlatın:
   ```sh
   python manage.py runserver
   ```

## Kullanım
- Tarayıcınızda `http://127.0.0.1:8000` adresine giderek uygulamayı görüntüleyebilirsiniz.
- Yönetici paneline erişmek için `http://127.0.0.1:8000/admin` adresini kullanabilirsiniz.

## Katkıda Bulunma
Katkıda bulunmak için:
1. Fork yapın (https://github.com/palamut62/hackersnewsProject/fork)
2. Kendi dalınızı oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Dalınıza push yapın (`git push origin feature/AmazingFeature`)
5. Bir Pull Request açın

## Lisans
----------------------------------

## İletişim
Herhangi bir soru veya geri bildirim için lütfen [umutcelik6230@gmail.com](mailto:umutcelik6230@gmail.com) adresinden iletişime geçin.


