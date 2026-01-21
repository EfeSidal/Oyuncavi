import pandas as pd
from scapy.all import rdpcap, IP
from sklearn.ensemble import IsolationForest
from colorama import Fore
from src.utils import get_ip_owner  # <--- Yeni eklediğimiz fonksiyonu çağırdık

def detect_anomalies(pcap_file):
    print(Fore.CYAN + "[*] AI Modeli yükleniyor ve trafik analiz ediliyor..." + Fore.RESET)
    
    try:
        packets = rdpcap(pcap_file)
    except FileNotFoundError:
        print(Fore.RED + "[!] Dosya bulunamadı." + Fore.RESET)
        return None

    data = []
    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            pkt_len = pkt.len
            pkt_proto = pkt[IP].proto
            pkt_time = float(pkt.time)
            data.append([src_ip, dst_ip, pkt_len, pkt_proto, pkt_time])

    if not data:
        print(Fore.YELLOW + "[!] Analiz edilecek IP paketi bulunamadı." + Fore.RESET)
        return None

    df = pd.DataFrame(data, columns=["src_ip", "dst_ip", "length", "protocol", "time"])

    # Model Eğitimi
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(df[['length', 'time', 'protocol']])

    # Anomali Filtreleme
    anomalies = df[df['anomaly'] == -1].copy() # Kopyasını alıyoruz uyarı vermesin diye
    
    print(Fore.GREEN + f"[+] Analiz Bitti. Toplam Paket: {len(df)}" + Fore.RESET)
    print(Fore.RED + f"[!] Tespit Edilen Şüpheli Paket Sayısı: {len(anomalies)}" + Fore.RESET)
    
    if len(anomalies) > 0:
        print(Fore.YELLOW + "[*] Şüpheli IP adresleri için WHOIS sorgusu yapılıyor (Biraz sürebilir)..." + Fore.RESET)
        
        # Sadece şüpheli paketlerin sahiplerini bul
        # apply fonksiyonu ile her satıra get_ip_owner uyguluyoruz
        anomalies['Owner'] = anomalies['src_ip'].apply(get_ip_owner)

        print("\n" + Fore.RED + "--- ŞÜPHELİ PAKET KAYNAKLARI VE SAHİPLERİ ---" + Fore.RESET)
        # Ekrana Owner sütununu da basıyoruz
        print(anomalies[['src_ip', 'Owner', 'length', 'protocol']].head(10).to_string(index=False))
        
    return df