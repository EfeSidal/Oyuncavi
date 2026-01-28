# 🛡️ OyuncuAvi (GamerHunt)
### 🎮 Çevrim İçi Oyunlar İçin Yapay Zeka Destekli Ağ Tehdit Analizi

<div align="center">

  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/AI-Anomaly%20Detection-green?style=for-the-badge" alt="AI">
  <img src="https://img.shields.io/badge/Status-v2.0-success?style=for-the-badge" alt="Status">

  <p>
    <b>Oyun trafiğini dinle, anomalileri tespit et, tehditleri haritalandır.</b>
  </p>
</div>

---

## 🧐 Nedir?

**OyuncuAvi**, yerel ağ trafiğini dinleyerek çevrim içi oyunlar sırasında oluşan veri paketlerini analiz eden bir **Siber Güvenlik & Gözlemlenebilirlik** aracıdır. 

Geleneksel Wireshark analizlerinin aksine, OyuncuAvi **son kullanıcı odaklıdır**. Karmaşık paket listeleri yerine; görsel grafikler, coğrafi saldırı haritaları ve yapay zeka destekli anomali skorları sunar.

### 🎯 Temel Hedefler
* **Şifreli Trafik Analizi (ETA):** Paket içeriğini okumadan, boyut ve zamanlama metadataları üzerinden oyun trafiğini analiz etmek.
* **Anomali Tespiti:** `IsolationForest` algoritması ile normal oyun akışına uymayan (DDoS, Botnet, Hile yazılımı trafiği) paketleri belirlemek.
* **Oyun Servisi Tespiti:** Valve, Riot, Blizzard, Epic Games gibi oyun sunucularından gelen trafiği otomatik tanımlamak.

---

## 🚀 Özellikler (v2.0)

| Özellik | Açıklama |
| :--- | :--- |
| **🎨 Modern React Dashboard** | Vite + React tabanlı, glassmorphism tasarımlı interaktif arayüz |
| **🌓 Dark/Light Tema** | Tek tıkla tema değiştirme, tercih localStorage'da saklanır |
| **🧠 AI Analizi** | Makine öğrenmesi ile şüpheli paket boyutlarını ve sıklıklarını tespit eder |
| **🎮 Oyun Servisi Tespiti** | Valve, Riot, Blizzard, Epic, Discord, Minecraft trafiğini tanır |
| **🔔 Bildirim Sistemi** | Tehdit tespit edildiğinde anlık bildirim ve ses uyarısı |
| **⚙️ Ayarlar Paneli** | Anomali hassasiyeti, bildirimler ve tercihler |
| **📥 Dışa Aktarma** | JSON/CSV formatında analiz sonuçlarını indir |
| **📊 Detaylı Grafikler** | Trafik analizi, protokol dağılımı, port istatistikleri |

---

## 🛠️ Kurulum

Detaylı kurulum için lütfen **[📖 Kullanım Rehberi (User Guide)](User_Guide.md)** dosyasını okuyun.

### Hızlı Başlangıç (Windows)

#### 1. Backend Kurulumu
```bash
# Backend bağımlılıklarını yükle
pip install -r requirements.txt

# Npcap sürücüsünü yükle (Windows için şart)
# [https://npcap.com/](https://npcap.com/) adresinden indirin

```

#### 2. Frontend Kurulumu

```bash
cd frontend
npm install

```

#### 3. Uygulamayı Başlat

```bash
# Terminal 1 - Backend (Yönetici olarak)
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev

```

#### 4. Tarayıcıda Aç

```
http://localhost:5173

```

---

## 📂 Proje Yapısı

```
OyuncuAvi/
├── backend/
│   ├── main.py             # FastAPI sunucusu
│   ├── generate_sample.py  # Örnek veri oluşturucu
│   ├── requirements.txt    # Python bağımlılıkları
│   ├── src/
│   │   ├── analysis.py     # AI ve Anomali tespiti (Isolation Forest)
│   │   ├── capture.py      # Scapy ile ağ dinleme modülü
│   │   ├── utils.py        # Yardımcı fonksiyonlar
│   │   └── visualize.py    # Görselleştirme modülü
│   └── threat_intel/
│       └── blacklist.txt   # Tehdit istihbarat verileri
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── main.jsx
│       ├── App.jsx         # Ana React bileşeni
│       ├── components/     # UI Bileşenleri
│       │   ├── Header.jsx
│       │   ├── KpiCard.jsx
│       │   ├── TrafficChart.jsx
│       │   ├── PortChart.jsx
│       │   ├── ProtocolChart.jsx
│       │   ├── ThreatTable.jsx
│       │   ├── TopTalkers.jsx
│       │   ├── ControlPanel.jsx
│       │   ├── AlertPanel.jsx
│       │   ├── SettingsPanel.jsx
│       │   ├── ExportPanel.jsx
│       │   ├── GameServices.jsx
│       │   └── StatsBar.jsx
│       ├── context/        # React Context (State Yönetimi)
│       │   ├── AlertContext.jsx
│       │   ├── SettingsContext.jsx
│       │   └── ThemeContext.jsx
│       ├── hooks/
│       │   └── useGameSocket.js
│       └── utils/
│           └── gameServices.js
├── README.md
├── User_Guide.md
├── ROADMAP.md
├── STEPS.md
└── LICENSE

```

---

## ⚠️ Yasal Uyarı

Bu proje **eğitim ve araştırma amaçlı** geliştirilmiştir.

* Sadece izinli olduğunuz (kendi ağınız) ağlarda kullanın.
* Başkalarının ağ trafiğini izinsiz dinlemek suç teşkil edebilir.
* Geliştiriciler, bu aracın kötüye kullanımından sorumlu tutulamaz.

---

## 🤝 Katkıda Bulunma

1. Forklayın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit atın (`git commit -m 'Add some AmazingFeature'`)
4. Pushlayın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

---

## 📜 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın.
