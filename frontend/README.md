# 🎮 OyuncuAvi Frontend

Bu klasör, OyuncuAvi projesinin modern React tabanlı kullanıcı arayüzünü içerir.

## 🛠️ Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| **React 18** | UI bileşen kütüphanesi |
| **Vite** | Hızlı geliştirme sunucusu ve build aracı |
| **Tailwind CSS** | Utility-first CSS framework |
| **Recharts** | React grafik kütüphanesi |
| **Lucide React** | Modern ikon seti |
| **Axios** | HTTP istekleri için |

## 📦 Kurulum

```bash
# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev

# Üretim build'i oluştur
npm run build
```

## 🚀 Başlatma

```bash
npm run dev
```

Tarayıcıda aç: `http://localhost:5173`

> **Not:** Backend'in (`http://localhost:8000`) çalışıyor olması gerekir.

## 📂 Proje Yapısı

```
src/
├── App.jsx                 # Ana uygulama bileşeni
├── main.jsx                # Giriş noktası
├── index.css               # Global stiller ve tasarım sistemi
├── components/
│   ├── Header.jsx          # Üst menü (tema, bildirim, ayarlar)
│   ├── KpiCard.jsx         # İstatistik kartları
│   ├── TrafficChart.jsx    # Trafik analizi grafiği
│   ├── ThreatTable.jsx     # Tehdit listesi tablosu
│   ├── ControlPanel.jsx    # Tarama kontrolleri
│   ├── AlertPanel.jsx      # Bildirim paneli
│   ├── SettingsPanel.jsx   # Ayarlar modalı
│   ├── ThemeToggle.jsx     # Tema değiştirici
│   ├── ProtocolChart.jsx   # TCP/UDP pasta grafiği
│   ├── TopTalkers.jsx      # En aktif IP'ler
│   ├── GameServices.jsx    # Oyun servisi tespiti
│   ├── PortChart.jsx       # Port dağılımı
│   ├── StatsBar.jsx        # Anlık istatistikler
│   └── ExportPanel.jsx     # JSON/CSV dışa aktarma
├── context/
│   ├── ThemeContext.jsx    # Tema durumu yönetimi
│   ├── SettingsContext.jsx # Uygulama ayarları
│   └── AlertContext.jsx    # Bildirim yönetimi
└── utils/
    └── gameServices.js     # Oyun servisi tespit algoritması
```

## 🎨 Özellikler

- ✅ **Dark/Light Tema** - Otomatik tercih kaydı
- ✅ **Gerçek Zamanlı Grafikler** - Recharts ile interaktif görselleştirme
- ✅ **Bildirim Sistemi** - Tehdit uyarıları ve ses efektleri
- ✅ **Ayarlar Paneli** - Hassasiyet, bildirim tercihleri
- ✅ **Oyun Tespiti** - Valve, Riot, Blizzard, Epic Games vb.
- ✅ **Dışa Aktarma** - JSON ve CSV formatları
- ✅ **Responsive Tasarım** - 16:9 optimizasyonu
- ✅ **Glassmorphism UI** - Modern cam efekti tasarımı

## 🔗 Backend API

Frontend şu API endpoint'lerini kullanır:

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/` | GET | Bağlantı kontrolü |
| `/start/{interface}` | POST | Taramayı başlat |
| `/results` | GET | Sonuçları al |

## 📝 Notlar

- Backend varsayılan olarak `http://localhost:8000` adresinde çalışır
- Gerçek tarama için backend'in Yönetici yetkisiyle çalışması gerekir
- Demo modu backend olmadan da çalışır (simüle veri)
