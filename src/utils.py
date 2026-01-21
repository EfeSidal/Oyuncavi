from ipwhois import IPWhois
import ipaddress

# Cache (Hafıza) - Aynı IP'yi tekrar tekrar sormamak için
ip_cache = {}

def get_ip_details(ip):
    """
    IP adresinin Sahibini, Ülkesini ve Koordinatlarını döndürür.
    Return: {'org': '...', 'country': '...', 'lat': 0.0, 'lon': 0.0}
    """
    # 1. Cache kontrolü
    if ip in ip_cache:
        return ip_cache[ip]

    default_data = {'org': 'Bilinmiyor', 'country': '??', 'lat': None, 'lon': None}

    # 2. Özel IP kontrolü (Yerel Ağ)
    try:
        if ipaddress.ip_address(ip).is_private:
            result = {'org': 'Yerel Ağ (Private)', 'country': 'LAN', 'lat': None, 'lon': None}
            ip_cache[ip] = result
            return result
    except ValueError:
        return default_data

    # 3. İnternetten Sorgula
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap(depth=1)
        
        # Verileri çek
        org = res.get('asn_description') or res.get('network', {}).get('name') or "Bilinmiyor"
        country = res.get('asn_country_code') or "??"
        
        # Koordinat bulmaya çalış (Bazen tam gelmez ama deneyelim)
        # Not: Ücretsiz IPWhois her zaman tam koordinat vermez, 
        # profesyonel projelerde GeoIP2 veritabanı kullanılır. 
        # Şimdilik basit tutmak için 'None' dönüyoruz, harita özelliğini ilerde geliştirebiliriz.
        # Ancak Streamlit map için rastgele veya yaklaşık veri simule edebiliriz.
        
        result = {'org': org, 'country': country, 'lat': None, 'lon': None}
        ip_cache[ip] = result
        return result
        
    except Exception as e:
        return default_data