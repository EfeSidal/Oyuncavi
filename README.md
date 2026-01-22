<div align="center">

  # 🎮 Oyuncuavi (Gamer Hunt)
  
  **Çevrim İçi Oyunlar için Ağ Trafiği Analizi**

  <p>
    <a href="https://github.com/EfeSidal/Oyuncavi">
      <img src="https://img.shields.io/github/languages/top/EfeSidal/Oyuncavi?style=flat-square&color=1e90ff" alt="Ana Dil" />
    </a>
    <a href="https://github.com/EfeSidal/Oyuncavi">
      <img src="https://img.shields.io/github/last-commit/EfeSidal/Oyuncavi?style=flat-square&color=ff69b4" alt="Son Commit" />
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/EfeSidal/Oyuncavi?style=flat-square&color=yellow" alt="Lisans" />
    </a>
    <img src="https://img.shields.io/badge/Odak-Ağ_Adli_Analizi-red?style=flat-square" alt="Odak" />
  </p>

  <p>
    <a href="#about">Hakkında</a> •
    <a href="#features">Özellikler</a> •
    <a href="#installation">Kurulum</a> •
    <a href="#usage">Kullanım</a> •
    <a href="#threat-model">Tehdit Modeli</a>
  </p>
</div>

---

## 🧐 Hakkında <a name="about"></a>

**Oyuncuavi**, çevrim içi oyunların iletişim desenlerini anlaşılır hâle getirmek için tasarlanmış, özel bir ağ trafiği analiz aracıdır.  
`.pcap` ve `.pcapng` dosyalarını ayrıştırarak **oyun sunucusu bağlantılarını** tespit eder, **gecikme (latency) karakteristiklerini** analiz eder ve **bölgesel sunucu altyapısını** haritalandırır.

Genel amaçlı trafik analiz araçlarının aksine Oyuncuavi, oyun protokollerine özgü davranışlara odaklanır (UDP yoğunluğu, heartbeat paketleri, paylaşılan CDN kullanımı).

> **Not:** Bu proje **kesinlikle analiz ve gözlemlenebilirlik** amaçlıdır; istismar, hile veya avantaj sağlama hedeflemez.

---

## 🚀 Özellikler <a name="features"></a>

| Özellik | Açıklama |
| :--- | :--- |
| **📁 Paket İncelemesi** | Wireshark / Tcpdump ile alınmış `.pcap` dosyalarının derin analizi. |
| **🌍 Bölge Tespiti** | IP metadatası üzerinden fiziksel sunucu konumlarının (EU-West, NA-East vb.) belirlenmesi. |
| **⚡ Gecikme Analizi** | Paket zamanlamasına bakarak bağlantı kararlılığı ve olası lag sıçramalarının tahmini. |
| **🔍 Parmak İzi Analizi** | Oyun trafiğini arka plan işletim sistemi trafiğinden ayırmak için sezgisel desenler kullanır. |

---

## 🛠 Kurulum <a name="installation"></a>

> ⚠️ Kurulum adımlarını takip etmeden projeyi çalıştırmaya çalışırsanız sorun yaşarsınız.  
> Lütfen önce **[User Guide](https://github.com/EfeSidal/Oyuncavi/blob/main/User_Guide.md)** dosyasını okuyun.
