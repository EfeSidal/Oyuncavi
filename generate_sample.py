from scapy.all import wrpcap, IP, UDP, TCP, Ether
import os
import random
import time

# --- AYARLAR ---
OUTPUT_DIR = "samples"
OUTPUT_FILE = "sample_game_traffic.pcap"
PACKET_COUNT = 2000  # Daha fazla veri, daha güzel grafik

# --- SENARYO IP HAVUZU (Gerçekçi Harita İçin) ---
# Bu IP'ler IPWhois sorgusunda gerçek ülkeleri gösterecek.
LOCATIONS = {
    "TR_Home": "176.88.10.20",       # Türkiye (Bizim Ev)
    "DE_Valve": "146.66.155.1",      # Almanya (CS:GO Sunucusu)
    "US_Riot": "104.160.131.1",      # ABD (Valorant/LoL)
    "US_Google": "8.8.8.8",          # ABD (DNS)
    "CN_Unknown": "203.119.175.75",  # Çin (Şüpheli Trafik)
    "RU_Hacker": "45.89.246.212",    # Rusya (Saldırgan)
    "US_Minecraft": "192.99.14.166", # ABD (Minecraft Server)
    "Cloudflare": "1.1.1.1"          # ABD (Test amaçlı Kara Liste IP'si)
}

def create_advanced_sample():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    packets = []
    start_time = time.time()
    
    print(f"[*] {PACKET_COUNT} adet gelişmiş senaryo paketi üretiliyor...")
    print("[*] Senaryo: Oyun oynarken Çin ve Rusya'dan atak geliyor...")

    # DÖNGÜ: Trafik Akışı
    for i in range(PACKET_COUNT):
        current_time = start_time + (i * 0.05) # Her paket arası 0.05sn
        
        # %60 İHTİMAL: Normal Oyun Trafiği (CS:GO - Almanya)
        # Küçük paketler, hızlı akış
        if random.random() < 0.6:
            pkt = Ether() / IP(src=LOCATIONS["TR_Home"], dst=LOCATIONS["DE_Valve"]) / UDP(dport=27015) / ("GAME_DATA" * 2)
            pkt.time = current_time
            packets.append(pkt)

        # %15 İHTİMAL: Arka Plan Uygulamaları (Discord/Spotify - ABD)
        elif random.random() < 0.15:
            pkt = Ether() / IP(src=LOCATIONS["TR_Home"], dst=LOCATIONS["US_Google"]) / TCP(dport=443) / ("HTTPS_DATA" * 5)
            pkt.time = current_time
            packets.append(pkt)
            
        # %10 İHTİMAL: Minecraft Oynayan Kardeş (Minecraft - ABD)
        elif random.random() < 0.10:
            pkt = Ether() / IP(src=LOCATIONS["TR_Home"], dst=LOCATIONS["US_Minecraft"]) / TCP(dport=25565) / ("BLOCKS" * 10)
            pkt.time = current_time
            packets.append(pkt)

        # %10 İHTİMAL: SALDIRI BAŞLIYOR! (Çin ve Rusya'dan Büyük Paketler)
        # Bu paketler grafikte "Kırmızı" yanmalı ve boyutu büyük olmalı
        elif random.random() < 0.10:
            attacker = random.choice([LOCATIONS["CN_Unknown"], LOCATIONS["RU_Hacker"]])
            # Normalden çok daha büyük paket (1000+ byte)
            payload = "DDOS_ATTACK_PATTERN_" * 50 
            pkt = Ether() / IP(src=attacker, dst=LOCATIONS["TR_Home"]) / UDP(dport=random.choice([80, 443, 27015])) / payload
            pkt.time = current_time
            packets.append(pkt)

        # %5 İHTİMAL: KARA LİSTE TESTİ (1.1.1.1)
        # Dashboard'daki kırmızı alarmı tetiklemek için
        else:
            pkt = Ether() / IP(src=LOCATIONS["Cloudflare"], dst=LOCATIONS["TR_Home"]) / UDP(dport=53) / "DNS_QUERY"
            pkt.time = current_time
            packets.append(pkt)

    # Dosyayı Kaydet
    full_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    wrpcap(full_path, packets)
    print(f"[+] OLUŞTURULDU: {full_path}")
    print("[+] Dashboard'da 'Demo Modu'nu açarak haritayı ve grafikleri test et!")

if __name__ == "__main__":
    create_advanced_sample()