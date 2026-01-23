
# 📖 OyuncuAvi (GamerHunt) - Detaylı Kullanım Kılavuzu

Bu doküman, **OyuncuAvi v2.0** siber güvenlik aracının kurulumu, yapılandırılması ve kullanımı hakkında detaylı teknik bilgiler içerir.

---

## 🏗️ 1. Ön Hazırlık ve Gereksinimler

### A. Python Kurulumu
* **İndir:** [Python.org](https://www.python.org/downloads/) adresinden Python 3.10+ sürümünü indirin.
* **⚠️ Kritik:** Kurulum sırasında **"Add Python to PATH"** kutucuğunu işaretleyin.

### B. Node.js Kurulumu
* **İndir:** [Node.js](https://nodejs.org/) adresinden LTS sürümünü indirin.
* Kurulum sonrası terminalde `node -v` ve `npm -v` komutlarıyla doğrulayın.

### C. Npcap Kurulumu (Windows İçin Şart)
* **İndir:** [Npcap İndirme Sayfası](https://npcap.com/#download)
* **⚠️ Kritik:** Kurulum sırasında **"Install Npcap in WinPcap API-compatible Mode"** kutucuğunu işaretleyin.

---

## ⚙️ 2. Proje Kurulumu

### Adım 1: Backend Bağımlılıklarını Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 2: Frontend Bağımlılıklarını Yükleyin
```bash
cd frontend
npm install
```

---

## ▶️ 3. Programı Çalıştırma

**İki ayrı terminal açarak** uygulamayı başlatın:

### Terminal 1 - Backend (Yönetici Olarak)
```bash
cd backend
python main.py
```
> **Not:** Windows'ta "Yönetici olarak çalıştır" ile açın.

Backend başarıyla başladığında şunu göreceksiniz:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Frontend başladığında:
```
VITE v6.x.x ready in xxx ms
➜ Local: http://localhost:5173/
```

### Tarayıcıda Aç
```
http://localhost:5173
```

---

## 🎮 4. Arayüz Kullanımı

### A. Üst Menü (Header)

| Öğe | Açıklama |
|-----|----------|
| 🌓 Tema Değiştir | Dark/Light mod arasında geçiş yapar |
| 🔔 Bildirimler | Tehdit uyarılarını ve sistem mesajlarını gösterir |
| ⚙️ Ayarlar | Anomali hassasiyeti, bildirim tercihleri |
| 🟢 Bağlantı Durumu | Backend ile bağlantı durumunu gösterir |

### B. Sol Panel (Kontrol)

1. **Ağ Arayüzü:** Dinlenecek ağ kartını yazın (örn: `Wi-Fi`, `Ethernet`)
2. **Paket Sayısı:** Analiz edilecek paket miktarını seçin (50-500)
3. **Taramayı Başlat:** Gerçek ağ trafiğini dinlemeye başlar
4. **Demo Modu:** Simüle edilmiş veriyle test edin

### C. Ana Ekran (Dashboard)

| Bölüm | Açıklama |
|-------|----------|
| **KPI Kartları** | Toplam paket, tehdit sayısı, risk oranı, benzersiz kaynak |
| **Trafik Analizi** | Paket boyutlarının zaman grafiği, anomaliler kırmızı ile işaretlenir |
| **Tespit Edilen Tehditler** | Şüpheli IP adresleri, ciddiyet seviyeleri |
| **Protokol Dağılımı** | TCP/UDP oranlarını gösteren pasta grafik |
| **Top Kaynaklar** | En aktif IP adresleri |
| **Oyun Servisleri** | Valve, Riot, Blizzard vb. tespit edilen oyun trafiği |

### D. Dışa Aktarma

- **JSON:** Tüm analiz verilerini JSON formatında indir
- **CSV:** Tablo formatında indir (Excel uyumlu)

---

## 🎨 5. Temalar ve Ayarlar

### Tema Değiştirme
- Header'daki güneş/ay ikonuna tıklayın
- Tercih otomatik olarak saklanır

### Ayarlar Paneli
| Ayar | Açıklama |
|------|----------|
| **Anomali Hassasiyeti** | 1-20% arası, düşük değer = daha fazla tehdit tespiti |
| **Bildirimler** | Tarayıcı bildirimleri aç/kapa |
| **Ses Efektleri** | Tehdit sesli uyarı aç/kapa |
| **Varsayılan Arayüz** | Başlangıç ağ kartı adı |

---

## ❓ 6. Sık Karşılaşılan Hatalar

| Hata | Çözüm |
|------|-------|
| `CORS error` | Backend'in çalıştığından emin olun (port 8000) |
| `Network Error` | Backend'i Yönetici olarak başlatın |
| `Interface is invalid` | Npcap'i WinPcap modunda kurun |
| `Permission denied` | Terminali Yönetici olarak çalıştırın |
| `npm: command not found` | Node.js'i yükleyin |
| Grafik boş geliyor | Demo modunu deneyin veya ağda trafik oluşturun |

---

## 🔧 7. API Endpoints

Backend şu endpoint'leri sunar:

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/` | GET | Bağlantı kontrolü |
| `/start/{interface}` | POST | Taramayı başlat |
| `/results` | GET | Analiz sonuçlarını al |
| `/interfaces` | GET | Mevcut ağ kartlarını listele |

---

## 📞 Destek

Sorun yaşarsanız:
1. Her iki terminaldeki hata mesajlarını kontrol edin
2. GitHub Issues sayfasına ekran görüntüsü ile bildirin
