# Market Otomasyon Sistemi

**Profesyonel Market Automation System** - Küçük marketler ve bakkallar için kapsamlı satış ve yönetim sistemi.

## Özellikler

### Satış Yönetimi
- ✅ Barkodlu satış sistemi
- ✅ Normal satış (barkodsuz ürün satışı)
- ✅ Veresiye satış sistemi
- ✅ Fiş yazdırma desteği

### Ürün Yönetimi
- ✅ Ürün ekleme, düzenleme ve silme
- ✅ Toplu ürün içe/dışa aktarma (Excel)
- ✅ Ürün arama ve filtreleme
- ✅ Stok takibi
- ✅ Kritik stok uyarıları
- ✅ Kategori yönetimi
- ✅ Barkod etiketi oluşturma ve yazdırma

### Müşteri Yönetimi
- ✅ Müşteri kayıtları
- ✅ Veresiye takip ekranı
- ✅ Müşteri cari hesap sistemi
- ✅ Veresiye alacak toplama ve raporlama

### Tedarikçi Yönetimi
- ✅ Tedarikçi yönetimi
- ✅ Alış faturası takibi
- ✅ Gider takibi

### Kasa Yönetimi
- ✅ Kasa açılış ve kapanış işlemleri
- ✅ Günlük kasa durum raporları

### Raporlar
- ✅ Günlük, haftalık ve aylık satış raporları
- ✅ Kar/Zarar raporları
- ✅ İstatistiksel analizler

### Sistem Özellikleri
- ✅ Personel yönetimi
- ✅ Yetki sistemi (Admin, Kasiyer vb.)
- ✅ Türkçe arayüz
- ✅ Tema seçimi (Aç��k/Koyu Tema)
- ✅ Otomatik yedekleme sistemi
- ✅ Veritabanı yedekleme ve geri yükleme
- ✅ Çoklu kullanıcı desteği

### Entegrasyonlar
- ⏳ Trendyol GO entegrasyonu
- ⏳ Online sipariş ekranı
- ⏳ Sipariş durum takibi

## Teknik Gereksinimler

- **İşletim Sistemi:** Windows 7, 8, 10 ve 11
- **Python:** 3.8 veya üzeri
- **Veritabanı:** SQLite (varsayılan) veya MySQL
- **RAM:** Minimum 4 GB
- **Disk:** Minimum 100 MB

## Kurulum

### Gerekli Paketlerin Kurulması

```bash
pip install -r requirements.txt
```

### Uygulamayı Çalıştırma

```bash
python main.py
```

## Proje Yapısı

```
market-automation/
├── main.py                 # Ana uygulama
├── config/
│   ├── settings.py        # Ayarlar
│   └── messages.py        # Türkçe mesajlar
├── database/
│   ├── db_manager.py      # Veritabanı yönetimi
│   └── repositories.py    # Veri işlemleri
├── ui/
│   ├── main_window.py     # Ana pencere
│   ├── styles.py          # Tema stilleri
│   └── screens/           # Ekranlar
│       ├── dashboard.py
│       ├── sales.py
│       ├── products.py
│       ├── customers.py
│       ├── credit_sales.py
│       ├── reports.py
│       ├── users.py
│       └── settings.py
├── modules/               # İş mantığı modülleri
├── resources/             # Resimler, ikonlar
├── reports/               # Rapor şablonları
├── utils/                 # Yardımcı fonksiyonlar
└── requirements.txt       # Python paketleri
```

## Varsayılan Giriş Bilgileri

- **Kullanıcı Adı:** admin
- **Şifre:** admin123

> ⚠️ İlk kurulumdan sonra şifrenizi değiştirmeyi unutmayın!

## Geliştirme Durumu

- [x] Proje yapısı oluşturuldu
- [x] Veritabanı şeması tasarlandı
- [x] Dashboard ekranı geliştirme başlandı
- [ ] Satış sistemi modülü
- [ ] Ürün yönetimi modülü
- [ ] Müşteri yönetimi modülü
- [ ] Raporlar modülü
- [ ] Trendyol GO entegrasyonu

## Lisans

Bu proje profesyonel kullanım için geliştirilmiştir.

## İletişim

Soru ve önerileriniz için iletişime geçebilirsiniz.
