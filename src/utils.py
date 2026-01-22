from ipwhois import IPWhois
import ipaddress
import os


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
    
}


ip_cache = {}
blacklist_ips = set()


def load_blacklist():
    """threat_intel/blacklist.txt dosyasını hafızaya yükler."""
    global blacklist_ips
    try:
        path = os.path.join("threat_intel", "blacklist.txt")
        if os.path.exists(path):
            with open(path, "r") as f:
                
                blacklist_ips = {line.strip() for line in f if line.strip() and not line.startswith("#")}
    except Exception as e:
        print(f"Blacklist hatası: {e}")


load_blacklist()


def get_ip_details(ip, port=0):
    """
    IP sahibini, ülkesini, oyun bilgisini ve kara liste durumunu döndürür.
    """
    
    service_name = GAME_PORTS.get(int(port), "Bilinmiyor")
    
    
    is_blacklisted = ip in blacklist_ips

    
    if ip in ip_cache:
        data = ip_cache[ip].copy()
        data['service'] = service_name 
        data['is_malicious'] = is_blacklisted
        return data

    default_data = {
        'org': 'Bilinmiyor', 
        'country': 'Unknown', 
        'service': service_name,
        'is_malicious': is_blacklisted
    }

    
    try:
        if ipaddress.ip_address(ip).is_private:
            result = default_data.copy()
            result['org'] = 'Yerel Ağ (LAN)'
            result['country'] = 'LAN'
            ip_cache[ip] = result
            return result
    except ValueError:
        return default_data

    
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
