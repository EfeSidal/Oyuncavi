
# 📖 OyuncuAvi (GamerHunt) - Detaylı Kullanım Kılavuzu

Bu doküman, **OyuncuAvi** siber güvenlik aracının kurulumu, yapılandırılması ve kullanımı hakkında detaylı teknik bilgiler içerir. Eğer kurulumda sorun yaşıyorsanız doğru yerdesiniz.

---

## 🏗️ 1. Ön Hazırlık ve Gereksinimler

Projeyi çalıştırmadan önce bilgisayarınızda aşağıdaki yazılımların doğru şekilde kurulduğundan emin olun. Çoğu hata bu aşamanın atlanmasından kaynaklanır.

### A. Python Kurulumu
* **İndir:** [Python.org](https://www.python.org/downloads/) adresinden en güncel sürümü indirin.
* **⚠️ Kritik Ayar:** Kurulum ekranının en altında yer alan **"Add Python to PATH"** kutucuğunu **MUTLAKA** işaretleyin.
    * *Neden?* İşaretlemezseniz terminalde `python` veya `pip` komutları çalışmaz.

### B. Npcap Kurulumu (Windows İçin Şart)
Windows işletim sistemi, varsayılan olarak ağ kartını "dinleme moduna" (monitor mode) almanıza izin vermez. Scapy kütüphanesinin çalışması için Npcap sürücüsü şarttır.

* **İndir:** [Npcap İndirme Sayfası](https://npcap.com/#download)
* **⚠️ Kritik Ayar:** Kurulum sırasında karşınıza gelen seçeneklerden **"Install Npcap in WinPcap API-compatible Mode"** kutucuğunu **KESİNLİKLE** işaretleyin.
    * *Neden?* Scapy kütüphanesi eski WinPcap API'sini kullanır. Bu seçenek olmadan ağ kartlarınızı göremezsiniz.

---

## ⚙️ 2. Proje Kurulumu

Terminali (Komut İstemi / CMD) açın ve aşağıdaki adımları sırasıyla uygulayın.

### Adım 1: Kütüphaneleri Yükleyin
Proje klasörünün içine girin ve gerekli Python kütüphanelerini yükleyin:

```bash
pip install -r requirements.txt

```

*(Eğer `pip` komutu bulunamadı hatası alırsanız, bilgisayarı yeniden başlatıp tekrar deneyin veya Python kurulumunu onarın.)*

### Adım 2: Demo Verisi Oluşturun (Tavsiye Edilir)

Programı ilk kez çalıştırıyorsanız, canlı ağ trafiği ile uğraşmadan önce sistemin çalıştığını test etmek için sahte veri üretin:

```bash
python generate_sample.py

```

* Bu komut, `data/captures` veya `samples` klasörüne `sample_game_traffic.pcap` adında bir dosya oluşturur.
* İçinde sahte CS:GO, Minecraft ve saldırı (DDoS) paketleri bulunur.

---

## ▶️ 3. Programı Çalıştırma

Programı başlatmak için şu komutu kullanın:

```bash
python -m streamlit run dashboard.py

```

**Not:** Eğer canlı ağ dinleme (Live Sniffing) yapacaksanız, terminali **"Yönetici Olarak Çalıştır" (Run as Administrator)** seçeneği ile açmanız gerekebilir. Windows, normal kullanıcıların ağ trafiğini dinlemesine izin vermeyebilir.

---

## 🎮 4. Arayüz Kullanımı

Tarayıcınızda açılan panelde (genellikle `http://localhost:8501`) şu kontroller bulunur:

### A. Sol Menü (Ayarlar)

1. **Dil / Language:** Arayüzü Türkçe veya İngilizce olarak değiştirebilirsiniz.
2. **Örnek Veri ile Test Et (Demo Modu):**
* **İşaretli ise:** Ağınızı dinlemez. `generate_sample.py` ile oluşturduğunuz dosyayı okur. Güvenli test için idealdir.
* **İşaretli değil ise:** Canlı ağ trafiğini dinlemeye başlar.


3. **Ağ Arayüzü (Interface):**
* Canlı modda hangi kartı dinleyeceğinizi seçersiniz. Genellikle `Wi-Fi` veya `Ethernet` yazmanız yeterlidir.
* Emin değilseniz **"❓ Ağ Kartlarını Listele"** butonuna basarak sistemdeki kart isimlerini görebilirsiniz.


4. **Paket Sayısı:** Analiz için kaç adet paket yakalanacağını belirler. Sayı arttıkça analiz süresi uzar ama doğruluk artar.

### B. Ana Ekran (Sonuçlar)

Analiz tamamlandığında 3 ana sekme görürsünüz:

1. **📊 Analiz Grafiği:**
* **Mavi Noktalar:** Normal, güvenli trafik (örn. Spotify, Google, Web siteleri).
* **Kırmızı Noktalar:** Anormal trafik. Yapay zeka (Isolation Forest) tarafından şüpheli bulunan paketler (örn. Çok büyük boyutlu paketler, beklenmedik portlar).


2. **🌍 Dünya Haritası:**
* Şüpheli paketlerin hangi ülkelerden geldiğini gösterir. (Örn: Çin veya Rusya'dan gelen beklenmedik trafik).


3. **🚨 Detaylı Tehdit Listesi:**
* Saldırganın IP adresi, hedef portu, paketin boyutu ve tespit edilebildiyse Kurum/Oyun bilgisi (örn. Valve, Riot Games).



---

## ❓ 5. Sık Karşılaşılan Hatalar ve Çözümleri

| Hata Mesajı | Olası Sebep | Çözüm |
| --- | --- | --- |
| `Scapy_Exception: Interface is invalid` | Ağ kartı ismi yanlış veya Npcap yüklü değil. | Npcap'i "WinPcap Mode" ile tekrar kurun. Arayüz ismini (Wi-Fi vb.) doğru yazdığınızdan emin olun. |
| `Permission denied` / `Erişim engellendi` | Yetki eksikliği. | Terminali (CMD) sağ tıklayıp **"Yönetici Olarak Çalıştır"** deyin. |
| `No module named 'streamlit'` | Kütüphaneler yüklenmemiş. | `pip install -r requirements.txt` komutunu tekrar çalıştırın. |
| `Hata: Örnek dosya bulunamadı!` | Demo verisi üretilmemiş. | `python generate_sample.py` komutunu çalıştırın. |
| **Grafik Boş Geliyor** | Arayüzden veri geçmiyor olabilir. | Doğru ağ kartını seçtiğinizden emin olun veya bir YouTube videosu açarak ağda trafik oluşturun. |

---

## 📞 Destek

Eğer yukarıdaki adımlara rağmen sorun yaşıyorsanız, hatanın ekran görüntüsünü alarak geliştirici ekibe (veya GitHub Issues kısmına) iletin.
