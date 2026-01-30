import pandas as pd
import numpy as np
from scapy.all import rdpcap, IP, TCP, UDP
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# LSTM detector import (lazy loading to avoid TensorFlow overhead)
_lstm_detector_module = None

# SNI extractor for HTTPS traffic verification
try:
    from src.sni_extractor import extract_sni_from_packets, verify_service_by_sni
    SNI_EXTRACTION_ENABLED = True
except ImportError:
    SNI_EXTRACTION_ENABLED = False

def extract_features(pcap_file):
    """
    PCAP dosyasından gelişmiş özellikler (ETA - Encrypted Traffic Analysis) çıkarır.
    Eski özellikler korunur, üzerine istatistiksel veriler eklenir.
    """
    packets = []
    
    try:
        # Scapy ile paketleri oku (Hata yönetimi ile)
        scapy_packets = rdpcap(pcap_file)
    except Exception as e:
        return pd.DataFrame() # Boş dönerse dashboard hata vermez, uyarı verir.

    # Build SNI cache for HTTPS verification
    sni_cache = {}
    if SNI_EXTRACTION_ENABLED:
        try:
            sni_cache = extract_sni_from_packets(scapy_packets)
        except Exception as e:
            print(f"[!] SNI extraction failed: {e}")

    for pkt in scapy_packets:
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            length = len(pkt)
            time = float(pkt.time)
            proto = pkt[IP].proto
            
            # Port bilgisini al (TCP/UDP varsa)
            sport = 0
            dport = 0
            if TCP in pkt:
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
            elif UDP in pkt:
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
            
            # Get SNI for HTTPS connections
            sni = None
            if dport == 443 or dport == 8443:
                sni = sni_cache.get((dst, dport))
            
            packets.append({
                'src_ip': src,
                'dst_ip': dst,
                'src_port': sport,
                'dst_port': dport,
                'protocol': proto,
                'length': length,
                'time': time,
                'sni': sni
            })

    df = pd.DataFrame(packets)
    
    if df.empty:
        return df

    # --- YENİ EKLENEN KISIM: ZENGİNLEŞTİRME (ENRICHMENT) ---
    
    # 1. Veriyi Akışlara Göre Sırala (Kaynak IP -> Hedef IP)
    df = df.sort_values(by=['src_ip', 'dst_ip', 'dst_port', 'time'])
    
    # 2. IAT (Inter-Arrival Time) Hesapla
    # Her paketin kendinden önceki paketle arasındaki zaman farkı
    df['iat'] = df.groupby(['src_ip', 'dst_ip', 'dst_port'])['time'].diff().fillna(0)
    
    # 3. Akış Bazlı İstatistikler (Rolling Window)
    # Son 10 paketin ortalama boyutu ve hızı
    df['rolling_mean_len'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
    df['rolling_std_len'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform(lambda x: x.rolling(window=10, min_periods=1).std().fillna(0))
    
    # 4. Jitter (Gecikme Sapması)
    # IAT'nin standart sapması bize Jitter'ı verir.
    df['jitter'] = df.groupby(['src_ip', 'dst_ip'])['iat'].transform(lambda x: x.rolling(window=10, min_periods=1).std().fillna(0))

    return df

def detect_anomalies(pcap_file):
    """
    Gelişmiş Isolation Forest kullanarak anomali tespiti yapar.
    """
    df = extract_features(pcap_file)
    
    if df.empty:
        return None

    # --- AI MODEL EĞİTİMİ ---
    
    # Modelin bakacağı özellikler (Eskiden sadece 'length' vardı)
    # Şimdi zamanlamayı ve akış karakteristiğini de ekledik.
    features = ['length', 'iat', 'jitter', 'rolling_mean_len']
    
    # Veriyi ölçeklendir (Normalization) - AI performansını artırır
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])

    # Isolation Forest Modeli
    # contamination=0.05 -> Verinin %5'ini anomali olarak işaretle (Agresiflik ayarı)
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    
    # Tahmin Yap (-1: Anomali, 1: Normal)
    df['anomaly'] = model.fit_predict(X)

    return df


def detect_anomalies_lstm(pcap_file, sequence_length=20, threshold=0.7):
    """
    LSTM tabanlı anomali tespiti yapar.
    Speedhack ve lag switch gibi zamanlama manipülasyonlarını tespit eder.
    
    Args:
        pcap_file: PCAP dosya yolu
        sequence_length: Her analiz penceresindeki paket sayısı
        threshold: Anomali sınıflandırma eşiği (0.0 - 1.0)
        
    Returns:
        DataFrame with 'suspicion_score' (0.0 - 1.0) ve 'lstm_anomaly' sütunları
    """
    global _lstm_detector_module
    
    # Lazy load to avoid TensorFlow overhead on import
    if _lstm_detector_module is None:
        try:
            from src import lstm_detector
            _lstm_detector_module = lstm_detector
        except ImportError as e:
            print(f"[!] LSTM modülü yüklenemedi: {e}")
            print("[*] TensorFlow kurulumu gerekli: pip install tensorflow>=2.10.0")
            return None
    
    df = extract_features(pcap_file)
    
    if df is None or df.empty:
        return None
    
    try:
        detector = _lstm_detector_module.LSTMDetector(
            sequence_length=sequence_length, 
            threshold=threshold
        )
        result_df = detector.detect(df, train_first=True)
        return result_df
    except Exception as e:
        print(f"[!] LSTM analizi başarısız: {e}")
        return df