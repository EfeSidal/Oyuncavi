import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
from sklearn.ensemble import IsolationForest
import os

def detect_anomalies(pcap_file):
    if not os.path.exists(pcap_file):
        return None

    try:
        packets = rdpcap(pcap_file)
    except Exception:
        return None

    data = []
    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            pkt_len = len(pkt)
            pkt_proto = pkt[IP].proto
            pkt_time = float(pkt.time)
            
           
            dst_port = 0
            if TCP in pkt:
                dst_port = pkt[TCP].dport
            elif UDP in pkt:
                dst_port = pkt[UDP].dport
            
            data.append([src_ip, dst_ip, pkt_len, pkt_proto, pkt_time, dst_port])

    if not data:
        return None

    
    df = pd.DataFrame(data, columns=["src_ip", "dst_ip", "length", "protocol", "time", "dst_port"])

   
    model = IsolationForest(contamination=0.05, random_state=42)
    try:
        df['anomaly'] = model.fit_predict(df[['length', 'time', 'dst_port']])
    except ValueError:
        df['anomaly'] = 1

    return df
