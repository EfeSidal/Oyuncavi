import pandas as pd
from scapy.all import rdpcap, IP
from sklearn.ensemble import IsolationForest
from colorama import Fore

def detect_anomalies(pcap_file):
    print(Fore.CYAN + "[*] AI Modeli yükleniyor ve trafik analiz ediliyor..." + Fore.RESET)
    
    try:
        packets = rdpcap(pcap_file)
    except FileNotFoundError:
        print(Fore.RED + "[!] Dosya bulunamadı." + Fore.RESET)
        return None

    # Veri setini oluştur (Feature Extraction)
    data = []
    for pkt in packets:
        if IP in pkt:
            # ARTIK IP ADRESLERINI DE ALIYORUZ
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            pkt_len = pkt.len
            pkt_proto = pkt[IP].proto
            pkt_time = float(pkt.time)
            
            # Listeye ekle
            data.append([src_ip, dst_ip, pkt_len, pkt_proto, pkt_time])

    if not data:
        print(Fore.YELLOW + "[!] Analiz edilecek IP paketi bulunamadı." + Fore.RESET)
        return None

    # DataFrame sütunlarını güncelle
    df = pd.DataFrame(data, columns=["src_ip", "dst_ip", "length", "protocol", "time"])

    # Model Eğitimi (Sadece sayısal verileri kullanıyoruz: length, time, protocol)
    model = IsolationForest(contamination=0.05, random_state=42)
    # IP string olduğu için eğitime katmıyoruz, sadece sonuçta göstereceğiz
    df['anomaly'] = model.fit_predict(df[['length', 'time', 'protocol']])

    # Sonuçları Filtrele (-1 anomali demektir)
    anomalies = df[df['anomaly'] == -1]
    
    print(Fore.GREEN + f"[+] Analiz Bitti. Toplam Paket: {len(df)}" + Fore.RESET)
    print(Fore.RED + f"[!] Tespit Edilen Şüpheli Paket Sayısı: {len(anomalies)}" + Fore.RESET)
    
    if len(anomalies) > 0:
        print("\n" + Fore.RED + "--- ŞÜPHELİ PAKET KAYNAKLARI (SALDIRGAN ADAYLARI) ---" + Fore.RESET)
        # Sadece ilgili sütunları yazdır
        print(anomalies[['src_ip', 'dst_ip', 'length', 'protocol']].head(10))
        
    return df