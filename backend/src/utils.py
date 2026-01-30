from ipwhois import IPWhois
import ipaddress
import os

# DNS-based service detection
try:
    from src.dns_tracker import get_service_by_ip, get_domain_by_ip
    DNS_LOOKUP_ENABLED = True
except ImportError:
    DNS_LOOKUP_ENABLED = False

# Process-based application detection
try:
    from src.process_tracker import get_app_details_by_port, is_verified_app
    PROCESS_LOOKUP_ENABLED = True
except ImportError:
    PROCESS_LOOKUP_ENABLED = False

# SNI-based HTTPS verification
try:
    from src.sni_extractor import verify_service_by_sni, SERVICE_SNI_KEYWORDS
    SNI_VERIFICATION_ENABLED = True
except ImportError:
    SNI_VERIFICATION_ENABLED = False

# --- 1. OYUN İMZALARI (PORT LISTESI) ---
# Buraya popüler oyunların portlarını ekledik.
GAME_PORTS = {
    27015: "Valve (CS:GO/HL)",
    27016: "Valve (CS:GO/HL)",
    5761: "Spotify (P2P)",
    25565: "Minecraft",
    443: "HTTPS (Web/Secure)",
    80: "HTTP (Web)",
    53: "DNS",
    3074: "Xbox Live / CoD",
    30000: "FiveM (GTA V)",
    5000: "LoL (League of Legends)",
    # Buraya istediğin kadar oyun ekleyebilirsin
}

# Cache
ip_cache = {}
blacklist_ips = set()

# --- 2. KARA LİSTEYİ YÜKLE ---
def load_blacklist():
    """threat_intel/blacklist.txt dosyasını hafızaya yükler."""
    global blacklist_ips
    try:
        path = os.path.join("threat_intel", "blacklist.txt")
        if os.path.exists(path):
            with open(path, "r") as f:
                # Satır satır oku, boşlukları temizle
                blacklist_ips = {line.strip() for line in f if line.strip() and not line.startswith("#")}
    except Exception as e:
        print(f"Blacklist hatası: {e}")

# İlk çalışmada listeyi yükle
load_blacklist()

# --- 3. IP DETAYLARI VE OYUN TESPİTİ ---
def get_ip_details(ip, port=0):
    """
    IP sahibini, ülkesini, oyun bilgisini ve kara liste durumunu döndürür.
    Önce DNS cache'den servis tespiti yapar, bulamazsa port bazlı imza kullanır.
    """
    # Öncelik 1: DNS tabanlı servis tespiti (daha güvenilir)
    service_name = None
    domain_name = None
    
    if DNS_LOOKUP_ENABLED:
        service_name = get_service_by_ip(ip)
        domain_name = get_domain_by_ip(ip)
    
    # Öncelik 2: Port bazlı tespit (fallback)
    if not service_name:
        service_name = GAME_PORTS.get(int(port), "Bilinmiyor")
    
    # Uygulama tespiti (Process tracking)
    app_name = "Bilinmiyor"
    app_verified = False
    process_name = None
    
    if PROCESS_LOOKUP_ENABLED and port:
        app_details = get_app_details_by_port(int(port))
        if app_details:
            app_name = app_details['app_category']
            app_verified = app_details['is_verified']
            process_name = app_details['process_name']
            
            # Eğer uygulama bilinmiyorsa uyarı ekle
            if not app_verified:
                app_name = f"Uygulama Bilinmiyor ({process_name})"
    
    # Kara Liste Kontrolü
    is_blacklisted = ip in blacklist_ips

    # Cache kontrolü
    if ip in ip_cache:
        data = ip_cache[ip].copy()
        data['service'] = service_name # Port değişebileceği için güncelleyelim
        data['is_malicious'] = is_blacklisted
        data['app_name'] = app_name
        data['app_verified'] = app_verified
        data['process_name'] = process_name
        return data

    default_data = {
        'org': 'Bilinmiyor', 
        'country': 'Unknown', 
        'service': service_name,
        'is_malicious': is_blacklisted,
        'app_name': app_name,
        'app_verified': app_verified,
        'process_name': process_name
    }

    # Özel IP kontrolü
    try:
        if ipaddress.ip_address(ip).is_private:
            result = default_data.copy()
            result['org'] = 'Yerel Ağ (LAN)'
            result['country'] = 'LAN'
            ip_cache[ip] = result
            return result
    except ValueError:
        return default_data

    # İnternetten Sorgula
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap(depth=1)
        org = res.get('asn_description') or res.get('network', {}).get('name') or "Bilinmiyor"
        country = res.get('asn_country_code') or "Unknown"
        
        result = {
            'org': org, 
            'country': country, 
            'service': service_name,
            'is_malicious': is_blacklisted
        }
        ip_cache[ip] = result
        return result
        
    except Exception:
        return default_data


def verify_https_service(dns_service: str, sni: str = None, port: int = 443) -> dict:
    """
    Verify HTTPS traffic using SNI and return verified service label.
    
    If port is 443 and SNI doesn't match the DNS-resolved service,
    marks as "Şüpheli/Genel HTTPS" to prevent false labeling.
    
    Args:
        dns_service: Service detected via DNS/IP lookup
        sni: Server Name Indication from TLS handshake
        port: Destination port
        
    Returns:
        Dict with 'service', 'sni', 'verified', 'suspicious' keys
    """
    result = {
        'service': dns_service,
        'sni': sni,
        'verified': False,
        'suspicious': False
    }
    
    # Only verify for HTTPS ports
    if port not in [443, 8443]:
        result['verified'] = True
        return result
    
    # If no SNI, mark as suspicious if claiming to be a known service
    if not sni:
        if dns_service and dns_service not in ["HTTPS (Web/Secure)", "Bilinmiyor"]:
            result['suspicious'] = True
            result['service'] = f"Şüpheli/Genel HTTPS (SNI yok, IP: {dns_service})"
        return result
    
    # Verify SNI matches claimed service using keywords
    if SNI_VERIFICATION_ENABLED and dns_service:
        verified, label = verify_service_by_sni(sni, dns_service)
        result['verified'] = verified
        result['suspicious'] = not verified
        result['service'] = label
    else:
        # No verification available, trust the SNI
        result['service'] = f"HTTPS ({sni})"
        result['verified'] = True
    
    return result