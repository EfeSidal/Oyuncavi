import pandas as pd
from scapy.all import rdpcap, IP
from sklearn.ensemble import IsolationForest
import os

def detect_anomalies(pcap_file):
    """
    Sadece paketleri analiz eder ve anomali tespiti yapar.
    WHOIS veya IP sorgusu yapmaz (Hata riskini azaltmak için).
    """
    
    # Dosya yoksa işlem yapma
    if not os.path.exists(pcap_file):
        return None

    try:
        packets = rdpcap(pcap_file)
    except Exception:
        return None

    # Verileri ayıkla
    data = []
    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            pkt_len = len(pkt)
            pkt_proto = pkt[IP].proto
            pkt_time = float(pkt.time)
            
            data.append([src_ip, dst_ip, pkt_len, pkt_proto, pkt_time])

    if not data:
        return None

    # DataFrame oluştur
    df = pd.DataFrame(data, columns=["src_ip", "dst_ip", "length", "protocol", "time"])

    # Yapay Zeka Modeli (Isolation Forest)
    # Sadece sayısal verileri kullanıyoruz
    model = IsolationForest(contamination=0.05, random_state=42)
    
    try:
        df['anomaly'] = model.fit_predict(df[['length', 'time', 'protocol']])
    except ValueError:
        df['anomaly'] = 1

    return df