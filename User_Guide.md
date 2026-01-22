# 🛡️ OyuncuAvi (GamerHunt) - Kurulum ve Kullanım Rehberi

Bu proje, yerel ağ trafiğini (Wi-Fi/Ethernet) dinleyerek yapay zeka destekli analiz yapan ve siber tehditleri tespit eden görsel bir siber güvenlik aracıdır.

## 📂 Dosya Yapısı

Proje klasörünüzün şu şekilde göründüğünden emin olun:

* `dashboard.py` (Arayüz ve ana program)
* `generate_sample.py` (Demo verisi üreten araç)
* `requirements.txt` (Gerekli kütüphaneler)
* `src/` (Kaynak kod klasörü)
* `samples/` (Örnek verilerin kaydedildiği klasör)

---

## 🚀 Adım 1: Gerekli Programların Kurulumu

Bu aracı çalıştırmak için bilgisayarınızda şu iki yazılımın kurulu olması gerekir:

### 1. Python (Yüklü değilse)

* [Python.org](https://www.python.org/downloads/) adresinden Python'un son sürümünü indirin.
* **⚠️ ÇOK ÖNEMLİ:** Kurulum ekranının en altında çıkan **"Add Python to PATH"** kutucuğunu mutlaka işaretleyin.

### 2. Npcap (Canlı Ağ Trafiğini Dinlemek İçin)

Windows, varsayılan olarak ağ trafiğini dinlemeye (sniffing) izin vermez. Npcap sürücüsü bu işi yapar.

* [Npcap İndir](https://npcap.com/#download) adresine gidin ve yükleyiciyi indirin.
* Kurulum sırasında **"Install Npcap in WinPcap API-compatible Mode"** seçeneğini **KESİNLİKLE İŞARETLEYİN**.
    * *(Eğer bu kutucuğu işaretlemezseniz program ağ kartınızı göremez.)*

---

## ⚙️ Adım 2: Kütüphanelerin Yüklenmesi

1. Proje klasörünün içine girin.
2. Klasördeki boş bir yere **Sağ Tık > Terminalde Aç** (veya adres çubuğuna `cmd` yazıp Enter) yapın.
3. Aşağıdaki komutu yapıştırıp Enter'a basın:

```bash
pip install -r requirements.txt

```

*(İnternet hızınıza göre 1-2 dakika sürebilir. Hata alırsanız Python sürümünüzü kontrol edin.)*

---

## 🧪 Adım 3: Demo Verisi Oluşturma (İsteğe Bağlı)

Eğer programı canlı ağda test etmeden önce **Demo Modu** ile denemek istiyorsanız, önce örnek veri dosyasını oluşturmalısınız.

Terminalde şu komutu çalıştırın:

```bash
python generate_sample.py

```

* Bu işlem `samples` klasörü içine `sample_game_traffic.pcap` adında sahte bir oyun trafiği dosyası oluşturacaktır.
* Programdaki "Demo Modu" bu dosyayı kullanır.

---

## ▶️ Adım 4: Programı Çalıştırma

**⚠️ ÖNEMLİ UYARI:** Canlı ağ dinleme (Sniffing) işlemi için terminali **Yönetici Olarak (Run as Administrator)** açmanız gerekebilir.

1. Terminali açın ve şu komutu yazın:

```bash
python -m streamlit run dashboard.py

```

2. Komutu yazdıktan sonra internet tarayıcınız otomatik olarak açılacak ve **OyuncuAvi Kontrol Paneli** karşınıza gelecektir.

---

## 🎮 Adım 5: Kullanım

Panel açıldığında yapmanız gerekenler:

### Seçenek A: Canlı Analiz

1. Sol menüden **"Demo Modu"** kutucuğunun işaretini kaldırın.
2. **Ağ Arayüzü** kutusuna kullandığınız bağlantıyı yazın (`Wi-Fi` veya `Ethernet`).
* *Emin değilseniz "Ağ Kartlarını Listele" butonuna basıp ismine bakabilirsiniz.*


3. **"Analizi Başlat"** butonuna basın.

### Seçenek B: Demo Modu (Test)

1. Sol menüden **"Örnek Veri ile Test Et (Demo Modu)"** kutucuğunu işaretleyin.
2. Program otomatik olarak `sample_game_traffic.pcap` dosyasını analiz eder ve sonuçları gösterir.

---

## 📊 Sonuçların Okunması

* **Grafik:** Mavi Noktalar **normal trafiği**, Kırmızı Noktalar **şüpheli/saldırı trafiğini** gösterir.
* **Dünya Haritası:** Saldırıların hangi ülkelerden geldiğini (örn. Çin, Rusya vb.) harita üzerinde boyar.
* **Tablo:** Şüpheli paketlerin detaylarını (IP Adresi, Kurum, Oyun Servisi) listeler.

---

## ❓ Sık Karşılaşılan Hatalar

**Hata 1:** `Scapy_Exception: Interface is invalid` veya `No libpcap provider available`

* **Çözüm:** Npcap yüklü değildir veya yüklerken "WinPcap Compatible Mode" seçilmemiştir. Npcap'i silip tekrar rehberdeki gibi yükleyin.

**Hata 2:** `Permission denied` veya Paket yakalamıyor.

* **Çözüm:** Kullandığınız terminali (CMD veya PowerShell) **Yönetici Olarak Çalıştır** diyerek açın.

**Hata 3:** `Hata: Örnek dosya bulunamadı!`

* **Çözüm:** Adım 3'teki `python generate_sample.py` komutunu çalıştırmayı unuttunuz.
