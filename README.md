<div align="center">
  <img src="https://img.shields.io/github/languages/count/EfeSidal/Oyuncavi?style=flat-square&color=blueviolet" alt="Language Count">
  <img src="https://img.shields.io/github/languages/top/EfeSidal/Oyuncavi?style=flat-square&color=1e90ff" alt="Top Language">
  <img src="https://img.shields.io/github/last-commit/EfeSidal/Oyuncavi?style=flat-square&color=ff69b4" alt="Last Commit">
  <img src="https://img.shields.io/github/license/EfeSidal/Oyuncavi?style=flat-square&color=yellow" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-green?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square" alt="Contributions">
</div>

# Gamer Hunt Project (EN)
*Oyuncu Avı* (turkce)

In this project, we analyze the network connections of users in some games using wirehark and identify the IP addresses, servers and ports used. (EN)  
*bu projede bazı oyunlardaki kullanıcıların ağ bağlantılarını wireshark kullanarak analiz edip, kullanılan IP adreslerini, sunucuları ve portları tespit edeceğim. (TR).*

---

## Features / *Özellikler*

**1. Real-Time Network Traffic Analysis**:
The project utilizes Wireshark to monitor and analyze network traffic in real time while users are playing games. It identifies which IP addresses are being used, the destination servers, and which ports are active during the connection.

-**1. Real-Time Network Traffic Analysis**:
The project utilizes Wireshark to monitor and analyze network traffic in real time while users are playing games. It identifies which IP addresses are being used, the destination servers, and which ports are active during the connection.
-**1. Gerçek Zamanlı Ağ Trafiği Analizi**:
Proje, Wireshark ile kullanıcıların oynadığı oyunlar sırasında gerçekleşen ağ trafiğini gerçek zamanlı olarak izleyerek, istemci-sunucu arasındaki veri alışverişini analiz eder. Bu sayede hangi IP adreslerinin kullanıldığı, hangi sunuculara bağlanıldığı ve veri iletimi için hangi portların açık olduğu tespit edilir.

-**2. Game-Specific Traffic Identification**:
The project is capable of distinguishing traffic patterns specific to different games. By recognizing unique data packet structures, protocols, or server communication behaviors, it provides detailed insights into how each game connects and communicates over the network.  
-**2. Oyunlara Özgü Trafik Tanıma**:
Proje, farklı oyunlara özgü ağ davranışlarını ayırt edebilir. Belirli oyunlara ait karakteristik veri paketleri, protokoller veya sunucu bağlantı desenleri tanımlanarak analiz detaylandırılır. Böylece oyunların bağlantı yapılarına dair özgün bilgiler elde edilir.

-**3. Security and Performance Assessment**:
Based on the collected IP, port, and server data, the project can offer evaluations related to network security and performance. It can determine which server regions players are connecting to, measure latency, and assess the overall efficiency and reliability of the game's network infrastructure. 
-**3. Güvenlik ve Performans Değerlendirmesi**:
Elde edilen IP, port ve sunucu verileriyle, oyunların ağ güvenliği ve performansı hakkında çıkarımlar yapılabilir. Örneğin, oyuncuların hangi ülkedeki sunuculara bağlandığı, bağlantı süresi ve gecikmeler (latency) gibi metrikler üzerinden performans analizi yapılabilir.

---

## Team / *Ekip*

-2420191004 -Efe Sidal: Project Owner/Proje Sahibi

---

## Roadmap / *Yol Haritası*

See our plans in [ROADMAP.md](ROADMAP.md).  
*Yolculuğu görmek için [ROADMAP.md](ROADMAP.md) dosyasına göz atın.*

---

## Research / *Araştırmalar*

| Topic / *Başlık*        | Link                                    | Description / *Açıklama*                        |
|-------------------------|-----------------------------------------|------------------------------------------------|
| Aircrack Deep Dive      | [researchs/aircrack.md](researchs/aircrack.md) | In-depth analysis of Aircrack-ng suite. / *Aircrack-ng paketinin derinlemesine analizi.* |
| Example Research Topic  | [researchs/your-research-file.md](researchs/your-research-file.md) | Brief overview of this research. / *Bu araştırmanın kısa bir özeti.* |
| Add More Research       | *Link to your other research files*     | *Description of the research*                  |

---

## Installation / *Kurulum*

1. **Clone the Repository / *Depoyu Klonlayın***:  
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

2. **Set Up Virtual Environment / *Sanal Ortam Kurulumu*** (Recommended):  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies / *Bağımlılıkları Yükleyin***:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage / *Kullanım*

Run the project:  
*Projeyi çalıştırın:*

```bash
python main.py --input your_file.pcap --output results.txt
```

**Steps**:  
1. Prepare input data (*explain data needed*).  
2. Run the script with arguments (*explain key arguments*).  
3. Check output (*explain where to find results*).  

*Adımlar*:  
1. Giriş verilerini hazırlayın (*ne tür verilere ihtiyaç duyulduğunu açıklayın*).  
2. Betiği argümanlarla çalıştırın (*önemli argümanları açıklayın*).  
3. Çıktıyı kontrol edin (*sonuçları nerede bulacağınızı açıklayın*).

---

## Contributing / *Katkıda Bulunma*

We welcome contributions! To help:  
1. Fork the repository.  
2. Clone your fork (`git clone git@github.com:YOUR_USERNAME/YOUR_REPO.git`).  
3. Create a branch (`git checkout -b feature/your-feature`).  
4. Commit changes with clear messages.  
5. Push to your fork (`git push origin feature/your-feature`).  
6. Open a Pull Request.  

Follow our coding standards (see [CONTRIBUTING.md](CONTRIBUTING.md)).  

*Topluluk katkilerini memnuniyetle karşılıyoruz! Katkıda bulunmak için yukarıdaki adımları izleyin ve kodlama standartlarımıza uyun.*

---

## License / *Lisans*

Licensed under the [MIT License](LICENSE.md).  
*MIT Lisansı altında lisanslanmıştır.*

---

## Contact / *İletişim* (Optional)

Project Maintainer: [Efe Sidal/Istinye University] - [sidalefe2005@gmail.com]  
Found a bug? Open an issue.  

*Proje Sorumlusu: [Efe Sidal/Istinye University] - [sidalefe2005@gmail.com]. Hata bulursanız bir sorun bildirin.*

---

*Replace placeholders (e.g., YOUR_USERNAME/YOUR_REPO) with your project details.*
