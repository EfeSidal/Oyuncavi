from scapy.all import sniff, wrpcap
import os
import time

def start_sniffer(interface, count=100):
    """
    Belirtilen arayüzden paket yakalar ve 'data/captures' klasörüne kaydeder.
    """
    # 1. Klasör Yolunu Belirle (data/captures)
    base_dir = "data"
    capture_dir = os.path.join(base_dir, "captures")
    
    # 2. Klasör Yoksa Oluştur (Hata almamak için)
    if not os.path.exists(capture_dir):
        os.makedirs(capture_dir)
    
    # 3. Dosya İsmi Oluştur (Zaman damgalı: capture_20250121_1530.pcap)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"capture_{timestamp}.pcap"
    filepath = os.path.join(capture_dir, filename) # Tam yol: data/captures/capture_...
    
    print(f"[*] {interface} uzerinden dinleme baslatildi... ({count} paket)")
    
    try:
        # Paketleri Yakala
        packets = sniff(iface=interface, count=count)
        
        # Dosyayı Kaydet
        wrpcap(filepath, packets)
        print(f"[+] Paketler kaydedildi: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"[!] Hata olustu: {e}")
        return None