# 🗺️ OyuncuAvi (GamerHunt) - Proje Yol Haritası

Bu yol haritası, **"2025 ve Sonrası İçin Gelişmiş Ağ Trafiği Analizi"** araştırma raporumuzdaki bulgulara dayanarak hazırlanmıştır. Hedefimiz, basit bir paket dinleyicisinden, Yapay Zeka destekli proaktif bir siber savunma sistemine evrilmektir.

---

## ✅ Faz 1: MVP ve Temel Görünürlük (Mevcut Durum)

*Projenin şu anki yetenekleri. Temel izleme ve anomali tespiti.*

* [x] **Canlı Paket Yakalama:** `Scapy` tabanlı yerel ağ dinleme altyapısı.
* [x] **Görsel Dashboard:** Streamlit ile gerçek zamanlı trafik grafikleri.
* [x] **Temel Anomali Tespiti:** `IsolationForest` algoritması ile istatistiksel sapmaların (anormal paket boyutları) tespiti.
* [x] **IP Zenginleştirme:** Paketlerin ülke ve servis (Valve, Riot vb.) bazlı etiketlenmesi.
* [x] **Demo Modu:** Sentetik veri üretimi ile test ortamı.

---

## 🚧 Faz 2: Şifreli Trafik Analizi (ETA) ve Profilleme (Q2 2026)

*Odak: Paket içeriğini okuyamadığımız modern oyunlarda (HTTPS/TLS) tehdit tespiti.*

* [ ] **Şifreli Trafik Analizi (ETA):** Paket içeriği şifreli olsa bile; paket boyutu, zamanlama ve akış (flow) metadatalarını analiz ederek oyun trafiğini tanımlayan modülün geliştirilmesi.
* [ ] **Oyuncu Profilleme:** Her oyuncu/cihaz için "Normal Davranış" taban çizgisi (baseline) oluşturan ve bu profilden sapmaları (örn. hesap çalınması, bot kullanımı) tespit eden sistem.
* [ ] **Gelişmiş Protokol Tersine Mühendisliği:** Popüler oyunların (Valorant, CS2) ağ imzalarının veritabanına eklenmesi.

---

## 🔮 Faz 3: Yapay Zeka Destekli NDR ve Tehdit Avcılığı (Q3 2026)

*Odak: Reaktif savunmadan, proaktif "Tehdit Avcılığına" geçiş.*

* [ ] **Gelişmiş AI Modelleri:** Basit `IsolationForest` yerine, zaman serisi analizi yapan **LSTM** veya **Autoencoder** derin öğrenme modellerinin entegrasyonu.
* [ ] **Otomatik NDR (Network Detection & Response):** Tespit edilen tehditlere karşı otomatik aksiyon (örn. bağlantı kesme önerisi, firewall kuralı üretme) mekanizması.
* [ ] **Tehdit Avcılığı (Threat Hunting) Arayüzü:** Geçmişe dönük trafik verileri üzerinde "Girişimci Saldırgan" (Enterprise Attacker) izlerini aramak için sorgu paneli.

---

## 🚀 Faz 4: Gelecek Vizyonu (2027 ve Ötesi)

*Odak: Yeni nesil ağ teknolojileri ve donanım güvenliği.*

* [ ] **Sıfır Güven (Zero Trust) Entegrasyonu:** "Asla güvenme, her zaman doğrula" prensibiyle, ağ içindeki her akışın sürekli kimlik doğrulamasını yapan modül.
* [ ] **Donanım Hile Tespiti:** DMA kartları veya donanım tabanlı hilelerin yarattığı mikro gecikme (latency) anomalilerini tespit eden hassas zamanlama analizi.
* [ ] **5G ve Edge Desteği:** 5G ağlarının düşük gecikme avantajını kullanarak analizi uç cihazlara (Edge) taşıma.

---

### 📂 Dokümantasyon ve Kaynaklar

Bu yol haritası aşağıdaki araştırma raporuna dayanmaktadır:

* `researchs/deepsearch.01.result.md`: *Çevrim İçi Oyunlarda Oyuncu Tespiti için Gelişmiş Ağ Trafiği Analizi*
