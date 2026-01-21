import argparse
from src.capture import start_sniffer
from src.analysis import detect_anomalies
from src.visualize import plot_traffic
from colorama import init, Fore

# Renklendirmeyi başlat
init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(description="OyuncuAvi - Ağ Analiz Aracı")
    parser.add_argument("-m", "--mode", type=str, required=True, choices=["live", "offline"], help="Mod seçimi: 'live' (canlı dinleme) veya 'offline' (dosya analizi)")
    parser.add_argument("-i", "--iface", type=str, help="Dinlenecek ağ arayüzü (örn: eth0, wlan0)")
    parser.add_argument("-f", "--file", type=str, help="Analiz edilecek .pcap dosyası")
    
    args = parser.parse_args()

    print(Fore.MAGENTA + """
     ____                            _    __     _ 
    / __ \_   _ _   _ _ __   ___ _   _  / \ \   / (_)
   / / _` | | | | | | | '_ \ / __| | | |/ _ \ \ / /| |
  | | (_| | |_| | |_| | | | | (__| |_| / ___ \ V / | |
   \ \__,_|\__, |\__,_|_| |_|\___|\__,_/_/   \_\_/  |_|
    \____/ |___/                                       
    """ + Fore.RESET)

    pcap_file = None

    # 1. MOD: Canlı Dinleme
    if args.mode == "live":
        if not args.iface:
            print(Fore.RED + "[!] Canlı mod için bir arayüz belirtmelisin (-i eth0 gibi).")
            return
        pcap_file = start_sniffer(args.iface)

    # 2. MOD: Çevrimdışı Analiz
    elif args.mode == "offline":
        pcap_file = args.file

    # 3. Analiz ve Görselleştirme
    if pcap_file:
        df_results = detect_anomalies(pcap_file)
        plot_traffic(df_results)

if __name__ == "__main__":
    main()
