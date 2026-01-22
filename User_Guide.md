# 🛡️ OyuncuAvi (GamerHunt) - Kurulum ve Kullanım Rehberi

Bu proje, yerel ağ trafiğini dinleyerek yapay zeka ile şüpheli paketleri ve olası siber tehditleri tespit eden görsel bir analiz aracıdır.

## 📂 Dosya Yapısı

Projeyi çalıştırmadan önce klasörün içinde şu dosyaların olduğundan emin olun:

* `dashboard.py` (Ana program dosyası)
* `requirements.txt` (Gerekli kütüphane listesi)
* `src/` (Kaynak kod klasörü - içinde `capture.py`, `analysis.py` vb. olmalı)

---

## 🚀 Adım 1: Gerekli Programların Kurulumu

Bu aracı çalıştırmak için bilgisayarınızda şu iki yazılımın kurulu olması gerekir:

### 1. Python (Yüklü değilse)

* [Python.org](https://www.python.org/downloads/) adresinden Python'un son sürümünü indirin.
* **ÖNEMLİ:** Kurulum ekranında en altta çıkan **"Add Python to PATH"** kutucuğunu mutlaka işaretleyin.

### 2. Npcap (Ağ Trafiğini Dinlemek İçin)

Windows, fabrikasyon olarak ağ trafiğini dinlemeye izin vermez. Bunun için bir sürücü gerekir.

* [Npcap İndir](https://www.google.com/search?q=https://npcap.com/%23download) adresine gidin ve yükleyiciyi indirin.
* Kurulum sırasında **"Install Npcap in WinPcap API-compatible Mode"** seçeneğini **KESİNLİKLE İŞARETLEYİN**. (İşaretlemezseniz program çalışmaz).

---

## ⚙️ Adım 2: Kütüphanelerin Yüklenmesi

1. Proje klasörünün içine girin.
2. Klasördeki boş bir yere **Sağ Tık > Terminalde Aç** (veya cmd yazıp Enter) yapın.
3. Aşağıdaki komutu yapıştırıp Enter'a basın:

```bash
pip install -r requirements.txt

```

*(Bu işlem internet hızınıza göre 1-2 dakika sürebilir. Tüm yüklemeler bitene kadar bekleyin.)*

---

## ▶️ Adım 3: Programı Çalıştırma

Kurulum bittikten sonra programı açmak için terminale şu komutu yazın:

```bash
python -m streamlit run dashboard.py

```

Bu komutu yazdıktan sonra internet tarayıcınız otomatik olarak açılacak ve **OyuncuAvi Kontrol Paneli** karşınıza gelecektir.

---

## 🎮 Adım 4: Kullanım

Panel açıldığında yapmanız gerekenler:

1. **Dil Seçimi:** Sol menüden **Türkçe** veya **English** seçebilirsiniz.
2. **Ağ Arayüzü:**
* Wi-Fi kullanıyorsanız kutucuğa `Wi-Fi` yazın.
* Kablo ile bağlıysanız `Ethernet` yazın.
* *Emin değilseniz "Ağ Kartlarını Listele" butonuna basıp ismine bakabilirsiniz.*


3. **Analiz:**
* **"Analizi Başlat"** butonuna basın.
* Program paketleri dinleyecek ve yapay zeka analizi yapacaktır.


4. **Sonuçlar:**
* Grafikte **Mavi Noktalar** normal trafiği, **Kırmızı Noktalar** şüpheli (anormal) trafiği gösterir.
* Alt kısımdaki tabloda şüpheli paketlerin hangi ülkeden ve hangi kurumdan (Google, Valve, DigitalOcean vb.) geldiğini görebilirsiniz.



---

## ❓ Sık Karşılaşılan Hatalar

**Hata:** `Scapy_Exception: Interface is invalid` veya `No libpcap provider available`

* **Çözüm:** Npcap yüklü değildir veya yüklerken "WinPcap Compatible Mode" seçilmemiştir. Npcap'i silip tekrar doğru şekilde yükleyin.

**Hata:** Program hiç açılmıyor, kırmızı yazılar çıkıyor.

* **Çözüm:** `pip install -r requirements.txt` komutunu tekrar çalıştırarak kütüphanelerin tam yüklendiğinden emin olun.

**İpucu:** Programı kapatmak için terminal ekranında `CTRL + C` tuşlarına basabilirsiniz.
