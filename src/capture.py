import os
from scapy.all import sniff, wrpcap
from colorama import Fore, Style

def start_sniffer(interface, count=1000, output_folder="data"):
    """
    Belirtilen arayüzden paketleri dinler ve .pcap dosyasına kaydeder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    filename = f"{output_folder}/capture.pcap"
    print(Fore.CYAN + f"[*] {interface} üzerinde {count} paket dinleniyor..." + Style.RESET_ALL)
    
    try:
        # Scapy ile dinleme (ROADMAP.md referans alınmıştır)
        packets = sniff(iface=interface, count=count)
        wrpcap(filename, packets)
        print(Fore.GREEN + f"[+] Yakalama tamamlandı! Dosya: {filename}" + Style.RESET_ALL)
        return filename
    except Exception as e:
        print(Fore.RED + f"[!] Hata oluştu: {e}" + Style.RESET_ALL)
        return None
