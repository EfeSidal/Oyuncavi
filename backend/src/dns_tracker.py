"""
DNS Tracking Module for Service Identification.

This module captures DNS query responses and maintains a mapping of
IP addresses to their resolved domain names. This allows accurate
service identification (Discord, Steam, Riot, etc.) based on DNS
rather than just port numbers.

Now with process verification: If a service like Discord is detected
via DNS but Discord.exe is not running, it will be marked as
"Şüpheli/Tarayıcı Trafiği" instead.
"""

from scapy.all import DNS, DNSRR, IP
from typing import Optional, Dict, Tuple
import re
import time

# --- PROCESS VERIFICATION ---
# Check if detected services have corresponding running processes
try:
    from src.process_tracker import get_cache_stats as get_process_cache_stats
    PROCESS_VERIFICATION_ENABLED = True
except ImportError:
    PROCESS_VERIFICATION_ENABLED = False

# Services that require process verification (must have app running)
APPS_REQUIRING_VERIFICATION = frozenset({
    'Discord', 'Steam', 'Valve/Steam', 'Riot Games', 
    'Epic Games', 'Blizzard', 'EA Games', 'Ubisoft', 'Twitch',
})

# Map service names to process tracker category names (constant, avoids re-creation)
SERVICE_TO_CATEGORY = {
    'Discord': 'Discord',
    'Valve/Steam': 'Steam',
    'Steam': 'Steam',
    'Riot Games': 'Riot Games',
    'Epic Games': 'Epic Games',
    'Blizzard': 'Blizzard',
    'EA Games': 'EA/Origin',
    'Ubisoft': 'Ubisoft',
    'Twitch': 'Twitch',
}

# Cache for running apps check (avoid repeated psutil calls)
_running_apps_cache: Dict[str, bool] = {}
_running_apps_cache_time: float = 0
_RUNNING_APPS_CACHE_TTL: float = 2.0  # 2 seconds cache


def is_app_running(service_name: str) -> bool:
    """Check if the application for a service is currently running."""
    global _running_apps_cache, _running_apps_cache_time
    
    if not PROCESS_VERIFICATION_ENABLED:
        return True
    
    # Check cache validity
    now = time.time()
    if now - _running_apps_cache_time > _RUNNING_APPS_CACHE_TTL:
        # Refresh cache
        try:
            stats = get_process_cache_stats()
            running_categories = stats.get('categories', {})
            _running_apps_cache = {svc: SERVICE_TO_CATEGORY.get(svc, svc) in running_categories 
                                   for svc in APPS_REQUIRING_VERIFICATION}
            _running_apps_cache_time = now
        except Exception:
            return True
    
    return _running_apps_cache.get(service_name, True)

# --- SERVICE DOMAIN PATTERNS ---
# Maps service names to their known domain patterns (regex)
SERVICE_DOMAINS: Dict[str, list] = {
    'Discord': [
        r'discord\.com$',
        r'discordapp\.net$',
        r'discordapp\.com$',
        r'discord\.gg$',
        r'discord\.media$',
        r'discordcdn\.com$',
    ],
    'Valve/Steam': [
        r'steamcontent\.com$',
        r'steampowered\.com$',
        r'steamserver\.net$',
        r'steamstatic\.com$',
        r'valve\.net$',
        r'valvesoftware\.com$',
        r'steam\.io$',
        r'steamcommunity\.com$',
    ],
    'Riot Games': [
        r'riotgames\.com$',
        r'leagueoflegends\.com$',
        r'valorant\.com$',
        r'playvalorant\.com$',
        r'riotcdn\.net$',
        r'pvp\.net$',
    ],
    'Epic Games': [
        r'epicgames\.com$',
        r'fortnite\.com$',
        r'unrealengine\.com$',
        r'epicgames\.dev$',
        r'easyanticheat\.net$',
    ],
    'Xbox Live': [
        r'xboxlive\.com$',
        r'xbox\.com$',
        r'xboxab\.com$',
        r'xboxservices\.com$',
    ],
    'PlayStation': [
        r'playstation\.net$',
        r'playstation\.com$',
        r'sonyentertainmentnetwork\.com$',
        r'sie\.com$',
    ],
    'Blizzard': [
        r'blizzard\.com$',
        r'battle\.net$',
        r'battlenet\.com\.cn$',
        r'blizzard\.cn$',
    ],
    'EA Games': [
        r'ea\.com$',
        r'origin\.com$',
        r'eacdn\.net$',
    ],
    'Ubisoft': [
        r'ubisoft\.com$',
        r'ubi\.com$',
        r'uplaypc\.s3\.amazonaws\.com$',
    ],
    'Twitch': [
        r'twitch\.tv$',
        r'twitchcdn\.net$',
        r'jtvnw\.net$',
    ],
    'Cloudflare': [
        r'cloudflare\.com$',
        r'cloudflare-dns\.com$',
        r'cloudflareinsights\.com$',
    ],
    'Google': [
        r'google\.com$',
        r'googleapis\.com$',
        r'gstatic\.com$',
        r'googlevideo\.com$',
    ],
    'Amazon AWS': [
        r'amazonaws\.com$',
        r'amazon\.com$',
        r'cloudfront\.net$',
    ],
    'Microsoft Azure': [
        r'azure\.com$',
        r'azureedge\.net$',
        r'microsoft\.com$',
        r'msftconnecttest\.com$',
    ],
    'FiveM': [
        r'fivem\.net$',
        r'cfx\.re$',
    ],
    'Minecraft': [
        r'minecraft\.net$',
        r'mojang\.com$',
    ],
}

# Compile regex patterns for performance
_compiled_patterns: Dict[str, list] = {}
for service, patterns in SERVICE_DOMAINS.items():
    _compiled_patterns[service] = [re.compile(p, re.IGNORECASE) for p in patterns]


# --- GLOBAL DNS CACHE ---
# Maps IP address -> (domain_name, service_name, timestamp)
dns_cache: Dict[str, Tuple[str, str, float]] = {}


def identify_service(domain: str) -> Optional[str]:
    """
    Identify the service name from a domain.
    
    Args:
        domain: Domain name to check
        
    Returns:
        Service name if matched, None otherwise
    """
    domain = domain.lower().rstrip('.')
    
    for service, patterns in _compiled_patterns.items():
        for pattern in patterns:
            if pattern.search(domain):
                return service
    
    return None


def process_dns_packet(packet) -> None:
    """
    Process a packet and extract DNS response data.
    Call this as a callback during sniffing.
    
    Args:
        packet: Scapy packet to process
    """
    import time
    
    # Only process DNS response packets with answers
    if not (DNS in packet and packet[DNS].ancount > 0):
        return
    
    try:
        # Iterate through DNS answers
        for i in range(packet[DNS].ancount):
            rr = packet[DNS].an[i]
            
            # Only process A records (IPv4) and AAAA records (IPv6)
            if not isinstance(rr, DNSRR):
                continue
            
            if rr.type not in [1, 28]:  # A = 1, AAAA = 28
                continue
            
            # Extract domain name (query name)
            domain = rr.rrname.decode() if isinstance(rr.rrname, bytes) else str(rr.rrname)
            domain = domain.rstrip('.')
            
            # Extract resolved IP
            ip = str(rr.rdata)
            
            # Identify service
            service = identify_service(domain)
            
            # Store in cache
            dns_cache[ip] = (domain, service or 'Unknown', time.time())
            
    except Exception as e:
        # Silently ignore malformed packets
        pass


def get_service_by_ip(ip: str, verify_process: bool = True) -> Optional[str]:
    """
    Look up service name for an IP address from DNS cache.
    
    If verify_process is True, checks if the corresponding app is actually
    running. If not, returns None or a browser traffic indicator.
    
    Args:
        ip: IP address to look up
        verify_process: Whether to verify app is running
        
    Returns:
        Service name if found and verified, None otherwise
    """
    if ip in dns_cache:
        domain, service, _ = dns_cache[ip]
        if service != 'Unknown':
            # Verify that the app is actually running
            if verify_process and service in APPS_REQUIRING_VERIFICATION:
                if not is_app_running(service):
                    # App not running, this is likely browser traffic
                    return f"Tarayıcı ({service} sitesi)"
            return service
    return None


def get_verified_service_by_ip(ip: str) -> Tuple[Optional[str], bool, Optional[str]]:
    """
    Look up service with verification status.
    
    Args:
        ip: IP address to look up
        
    Returns:
        Tuple of (service_name, is_verified, domain)
        - service_name: Detected service or None
        - is_verified: True if app is running, False if browser traffic
        - domain: Original domain name
    """
    if ip not in dns_cache:
        return (None, False, None)
    
    domain, service, _ = dns_cache[ip]
    
    if service == 'Unknown':
        return (None, False, domain)
    
    # Check if verification is needed
    if service in APPS_REQUIRING_VERIFICATION:
        app_running = is_app_running(service)
        if app_running:
            return (service, True, domain)
        else:
            return (f"Tarayıcı ({service} sitesi)", False, domain)
    
    # Services not requiring verification
    return (service, True, domain)


def get_domain_by_ip(ip: str) -> Optional[str]:
    """
    Look up domain name for an IP address from DNS cache.
    
    Args:
        ip: IP address to look up
        
    Returns:
        Domain name if found in cache, None otherwise
    """
    if ip in dns_cache:
        domain, _, _ = dns_cache[ip]
        return domain
    return None


def get_dns_cache() -> Dict[str, Tuple[str, str, float]]:
    """
    Get the current DNS cache.
    
    Returns:
        Dictionary mapping IP -> (domain, service, timestamp)
    """
    return dns_cache.copy()


def clear_dns_cache() -> None:
    """Clear the DNS cache."""
    global dns_cache
    dns_cache.clear()


def get_cache_stats() -> dict:
    """
    Get statistics about the DNS cache.
    
    Returns:
        Dict with cache statistics
    """
    services = {}
    for ip, (domain, service, _) in dns_cache.items():
        services[service] = services.get(service, 0) + 1
    
    return {
        'total_entries': len(dns_cache),
        'services': services
    }
