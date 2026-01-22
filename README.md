
# 🛡️ OyuncuAvi (GamerHunt)
### 🎮 Çevrim İçi Oyunlar İçin Yapay Zeka Destekli Ağ Tehdit Analizi

<div align="center">

  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/AI-Anomaly%20Detection-green?style=for-the-badge" alt="AI">
  <img src="https://img.shields.io/badge/Status-Prototype-orange?style=for-the-badge" alt="Status">

  <p>
    <b>Oyun trafiğini dinle, anomalileri tespit et, tehditleri haritalandır.</b>
  </p>
</div>

---

## 🧐 Nedir?

**OyuncuAvi**, yerel ağ trafiğini dinleyerek çevrim içi oyunlar sırasında oluşan veri paketlerini analiz eden bir **Siber Güvenlik & Gözlemlenebilirlik** aracıdır. 

Geleneksel Wireshark analizlerinin aksine, OyuncuAvi **son kullanıcı odaklıdır**. Karmaşık paket listeleri yerine; görsel grafikler, coğrafi saldırı haritaları ve yapay zeka destekli anomali skorları sunar.

### 🎯 Temel Hedefler
* **Şifreli Trafik Analizi (ETA):** Paket içeriğini okumadan (şifrelemeyi kırmadan), boyut ve zamanlama metadataları üzerinden oyun trafiğini analiz etmek.
* **Anomali Tespiti:** `IsolationForest` algoritması ile normal oyun akışına uymayan (DDoS, Botnet, Hile yazılımı trafiği) paketleri belirlemek.
* **Coğrafi İstihbarat:** Paketlerin hangi ülkeden ve hangi oyun sunucusundan (Valve, Riot, Blizzard vb.) geldiğini görselleştirmek.

---

## 🚀 Özellikler

| Özellik | Açıklama |
| :--- | :--- |
| **🧪 Demo Modu** | Herhangi bir ağ trafiği olmadan, simüle edilmiş veri ile aracı test etme imkanı. |
| **📊 Canlı Dashboard** | Streamlit tabanlı, interaktif grafikler ve dünya haritası. |
| **🧠 AI Analizi** | Makine öğrenmesi ile şüpheli paket boyutlarını ve sıklıklarını tespit eder. |
| **🌍 IP Zenginleştirme** | IP adreslerini otomatik olarak Ülke, ISP ve Oyun Servisi bilgisiyle eşleştirir. |

---

## 🛠️ Kurulum

Detaylı kurulum için lütfen **[📖 Kullanım Rehberi (User Guide)](User_Guide.md)** dosyasını okuyun.

### Hızlı Başlangıç (Windows)

1. **Gereksinimleri Yükleyin:**
   ```bash
   pip install -r requirements.txt

```

*(Not: Windows'ta paket yakalamak için [Npcap](https://npcap.com/) sürücüsünün kurulu olması gerekir.)*

2. **Demo Verisi Oluşturun (Opsiyonel):**
```bash
python generate_sample.py

```


3. **Uygulamayı Başlatın:**
```bash
python -m streamlit run dashboard.py

```



---

## 📂 Proje Yapısı

```
OyuncuAvi/
├── dashboard.py        # Ana Streamlit Uygulaması (Arayüz)
├── generate_sample.py  # Demo verisi üreten simülasyon aracı
├── requirements.txt    # Kütüphane bağımlılıkları
├── src/
│   ├── analysis.py     # AI ve Anomali tespiti (Isolation Forest)
│   ├── capture.py      # Scapy ile ağ dinleme modülü
│   └── utils.py        # IP Whois ve Blacklist işlemleri
└── threat_intel/
    └── blacklist.txt   # Bilinen zararlı IP listesi

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
