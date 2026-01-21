import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
from sklearn.ensemble import IsolationForest
from colorama import Fore

def detect_anomalies(pcap_file):
    print(Fore.CYAN + "[*] AI Modeli yükleniyor ve trafik analiz ediliyor..." + Fore.RESET)
    
    try:
        packets = rdpcap(pcap_file)
    except FileNotFoundError:
        print(Fore.RED + "[!] Dosya bulunamadı." + Fore.RESET)
        return

    # Veri setini oluştur (Feature Extraction)
    data = []
    for pkt in packets:
        if IP in pkt:
            # Deepsearch raporuna göre şifreli trafikte metadatalara (boyut, zaman) bakıyoruz
            pkt_len = pkt.len
            pkt_proto = pkt[IP].proto
            pkt_time = float(pkt.time)
            data.append([pkt_len, pkt_proto, pkt_time])

    if not data:
        print(Fore.YELLOW + "[!] Analiz edilecek IP paketi bulunamadı." + Fore.RESET)
        return

    df = pd.DataFrame(data, columns=["length", "protocol", "time"])

    # Model Eğitimi (Isolation Forest - Anomali Tespiti)
    # Contamination=0.05 -> Verinin %5'inin anomali olduğunu varsayıyoruz.
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(df[['length', 'time']])

    # Sonuçları Filtrele (-1 anomali demektir)
    anomalies = df[df['anomaly'] == -1]
    
    print(Fore.GREEN + f"[+] Analiz Bitti. Toplam Paket: {len(df)}" + Fore.RESET)
    print(Fore.RED + f"[!] Tespit Edilen Şüpheli Paket Sayısı: {len(anomalies)}" + Fore.RESET)
    
    if len(anomalies) > 0:
        print("\n--- Şüpheli Paket Örnekleri ---")
        print(anomalies.head())
        return df # Görselleştirme için veriyi döndür
    return df
