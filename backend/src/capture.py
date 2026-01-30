from scapy.all import sniff, wrpcap
import os
import time

# DNS tracking for service identification
try:
    from src.dns_tracker import process_dns_packet, clear_dns_cache, get_cache_stats
    DNS_TRACKING_ENABLED = True
except ImportError:
    DNS_TRACKING_ENABLED = False
    print("[!] DNS tracker not available, service detection will use port-based fallback")

# Process tracking for application identification
try:
    from src.process_tracker import take_connection_snapshot, get_cache_stats as get_process_stats
    PROCESS_TRACKING_ENABLED = True
except ImportError:
    PROCESS_TRACKING_ENABLED = False
    print("[!] Process tracker not available, application identification disabled")

def start_sniffer(interface, count=100):
    """
    Belirtilen arayüzden paket yakalar ve 'data/captures' klasörüne kaydeder.
    DNS paketlerini de işleyerek servis tanımlama için cache oluşturur.
    """
    base_dir = "data"
    capture_dir = os.path.join(base_dir, "captures")
    
    
    if not os.path.exists(capture_dir):
        os.makedirs(capture_dir)
    
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"capture_{timestamp}.pcap"
    filepath = os.path.join(capture_dir, filename) 
    
    print(f"[*] {interface} uzerinden dinleme baslatildi... ({count} paket)")
    
    # Take snapshot of active connections BEFORE sniffing
    if PROCESS_TRACKING_ENABLED:
        conn_count = take_connection_snapshot()
        stats = get_process_stats()
        print(f"[*] Process tracker: {conn_count} aktif bağlantı, {stats['verified_apps']} bilinen uygulama")
    
    # Clear DNS cache before new capture
    if DNS_TRACKING_ENABLED:
        clear_dns_cache()
        print("[*] DNS cache temizlendi, yeni sorgular takip ediliyor...")
    
    try:
        # Sniff packets - process DNS packets via callback if enabled
        if DNS_TRACKING_ENABLED:
            packets = sniff(iface=interface, count=count, prn=process_dns_packet)
            stats = get_cache_stats()
            print(f"[+] DNS cache: {stats['total_entries']} IP adresi eşleştirildi")
        else:
            packets = sniff(iface=interface, count=count)
        
        
        wrpcap(filepath, packets)
        print(f"[+] Paketler kaydedildi: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"[!] Hata olustu: {e}")
        return None

