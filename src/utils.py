from ipwhois import IPWhois
import ipaddress

# Sorgulanan IP'leri hafızada tutalım ki tekrar tekrar sorup vakit kaybetmeyelim (Cache)
ip_cache = {}

def get_ip_owner(ip):
    """
    Verilen IP adresinin sahibini (Organizasyon ismini) döndürür.
    """
    # 1. IP zaten hafızada mı?
    if ip in ip_cache:
        return ip_cache[ip]

    # 2. Özel (Private) IP mi? (192.168.x.x gibi yerel ağ IP'lerinin sahibi olmaz)
    try:
        if ipaddress.ip_address(ip).is_private:
            return "Yerel Ağ (Private)"
    except ValueError:
        return "Gecersiz IP"

    # 3. İnternetten sorgula
    try:
        obj = IPWhois(ip)
        # Hızlı sonuç için sadece temel bilgileri çekiyoruz
        res = obj.lookup_rdap(depth=1)
        # Organizasyon adını bulmaya çalış
        org = res.get('asn_description') or res.get('network', {}).get('name') or "Bilinmiyor"
        
        # Sonucu kaydet ve döndür
        ip_cache[ip] = org
        return org
    except Exception as e:
        return "Sorgu Hatasi"