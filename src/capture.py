from scapy.all import sniff, wrpcap
import os
import time

def start_sniffer(interface, count=100):
    """
    Belirtilen arayüzden paket yakalar ve 'data/captures' klasörüne kaydeder.
    """
    base_dir = "data"
    capture_dir = os.path.join(base_dir, "captures")
    
    
    if not os.path.exists(capture_dir):
        os.makedirs(capture_dir)
    
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"capture_{timestamp}.pcap"
    filepath = os.path.join(capture_dir, filename) 
    
    print(f"[*] {interface} uzerinden dinleme baslatildi... ({count} paket)")
    
    try:
       
        packets = sniff(iface=interface, count=count)
        
        
        wrpcap(filepath, packets)
        print(f"[+] Paketler kaydedildi: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"[!] Hata olustu: {e}")
        return None
