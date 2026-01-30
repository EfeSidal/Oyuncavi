"""
SNI (Server Name Indication) Extractor for TLS Traffic Analysis.

This module extracts the SNI field from TLS ClientHello packets,
allowing accurate identification of HTTPS destinations even when
traffic is encrypted.

SNI is sent in plain text during the TLS handshake, before encryption
is established, making it visible in packet captures.
"""

from typing import Optional, Dict, Tuple, List
from scapy.all import TCP, Raw


def extract_sni(packet) -> Optional[str]:
    """
    Extract SNI (Server Name Indication) from a TLS ClientHello packet.
    
    The SNI is located in the TLS ClientHello extensions:
    - TLS Record Layer: Content Type = 0x16 (Handshake)
    - Handshake Type = 0x01 (ClientHello)
    - Extensions contain SNI (Type = 0x0000)
    
    Args:
        packet: Scapy packet with TCP layer
        
    Returns:
        SNI hostname if found, None otherwise
    """
    if not (TCP in packet and Raw in packet):
        return None
    
    try:
        payload = bytes(packet[Raw].load)
        
        # Minimum TLS record size check
        if len(payload) < 5:
            return None
        
        # Check TLS Record Layer
        # Content Type: 0x16 = Handshake
        content_type = payload[0]
        if content_type != 0x16:
            return None
        
        # TLS Version (we accept any)
        # payload[1:3] = version
        
        # Record length
        record_length = (payload[3] << 8) | payload[4]
        
        # Ensure we have enough data
        if len(payload) < 5 + record_length:
            return None
        
        # Handshake layer starts at byte 5
        handshake_start = 5
        
        # Handshake Type: 0x01 = ClientHello
        handshake_type = payload[handshake_start]
        if handshake_type != 0x01:
            return None
        
        # Handshake length (3 bytes)
        handshake_length = (payload[handshake_start + 1] << 16) | \
                          (payload[handshake_start + 2] << 8) | \
                          payload[handshake_start + 3]
        
        # ClientHello starts after handshake header (4 bytes)
        client_hello_start = handshake_start + 4
        
        # Skip ClientHello fields to reach extensions:
        # - Version: 2 bytes
        # - Random: 32 bytes
        # - Session ID length: 1 byte + Session ID
        # - Cipher Suites length: 2 bytes + Cipher Suites
        # - Compression Methods length: 1 byte + Compression Methods
        # - Extensions length: 2 bytes + Extensions
        
        pos = client_hello_start
        
        # Skip protocol version (2 bytes)
        pos += 2
        
        # Skip random (32 bytes)
        pos += 32
        
        if pos >= len(payload):
            return None
        
        # Session ID
        session_id_length = payload[pos]
        pos += 1 + session_id_length
        
        if pos + 2 > len(payload):
            return None
        
        # Cipher Suites
        cipher_suites_length = (payload[pos] << 8) | payload[pos + 1]
        pos += 2 + cipher_suites_length
        
        if pos + 1 > len(payload):
            return None
        
        # Compression Methods
        compression_methods_length = payload[pos]
        pos += 1 + compression_methods_length
        
        if pos + 2 > len(payload):
            return None
        
        # Extensions
        extensions_length = (payload[pos] << 8) | payload[pos + 1]
        pos += 2
        
        extensions_end = pos + extensions_length
        
        # Parse extensions to find SNI (Type = 0x0000)
        while pos + 4 <= extensions_end and pos + 4 <= len(payload):
            ext_type = (payload[pos] << 8) | payload[pos + 1]
            ext_length = (payload[pos + 2] << 8) | payload[pos + 3]
            pos += 4
            
            if ext_type == 0x0000:  # SNI extension
                # SNI extension structure:
                # - SNI List Length: 2 bytes
                # - SNI Type: 1 byte (0x00 = hostname)
                # - SNI Length: 2 bytes
                # - SNI Value: variable
                
                if pos + 5 > len(payload):
                    return None
                
                # sni_list_length = (payload[pos] << 8) | payload[pos + 1]
                sni_type = payload[pos + 2]
                sni_length = (payload[pos + 3] << 8) | payload[pos + 4]
                
                if sni_type == 0x00:  # hostname
                    sni_start = pos + 5
                    sni_end = sni_start + sni_length
                    
                    if sni_end <= len(payload):
                        sni = payload[sni_start:sni_end].decode('utf-8', errors='ignore')
                        return sni.lower()
                
                return None
            
            pos += ext_length
        
        return None
        
    except Exception:
        return None


def extract_sni_from_packets(packets) -> Dict[Tuple[str, int], str]:
    """
    Extract SNI from all TLS ClientHello packets in a capture.
    
    Args:
        packets: List of Scapy packets
        
    Returns:
        Dictionary mapping (dst_ip, dst_port) → SNI hostname
    """
    from scapy.all import IP
    
    sni_cache: Dict[Tuple[str, int], str] = {}
    
    for pkt in packets:
        if not (IP in pkt and TCP in pkt):
            continue
        
        # Only check port 443 or common TLS ports
        dst_port = pkt[TCP].dport
        if dst_port not in [443, 8443, 993, 995, 465, 587]:
            continue
        
        sni = extract_sni(pkt)
        if sni:
            dst_ip = pkt[IP].dst
            sni_cache[(dst_ip, dst_port)] = sni
    
    return sni_cache


def get_sni_for_connection(sni_cache: Dict, dst_ip: str, dst_port: int) -> Optional[str]:
    """
    Get SNI for a specific connection from cache.
    
    Args:
        sni_cache: SNI cache from extract_sni_from_packets
        dst_ip: Destination IP address
        dst_port: Destination port
        
    Returns:
        SNI hostname if found, None otherwise
    """
    return sni_cache.get((dst_ip, dst_port))


def sni_matches_service(sni: Optional[str], service_keywords: List[str]) -> bool:
    """
    Check if SNI matches any of the service keywords.
    
    Args:
        sni: SNI hostname
        service_keywords: List of keywords to match (e.g., ['discord', 'discordapp'])
        
    Returns:
        True if SNI contains any keyword, False otherwise
    """
    if not sni:
        return False
    
    sni_lower = sni.lower()
    for keyword in service_keywords:
        if keyword.lower() in sni_lower:
            return True
    
    return False


# Service keyword mappings for SNI verification
SERVICE_SNI_KEYWORDS = {
    'Discord': ['discord', 'discordapp'],
    'Valve/Steam': ['steam', 'valve', 'steampowered'],
    'Riot Games': ['riot', 'leagueoflegends', 'valorant', 'pvp.net'],
    'Epic Games': ['epic', 'fortnite', 'unrealengine'],
    'Twitch': ['twitch', 'jtvnw'],
    'Xbox Live': ['xbox', 'xboxlive'],
    'PlayStation': ['playstation', 'sony'],
    'Blizzard': ['blizzard', 'battle.net', 'battlenet'],
    'EA Games': ['ea.com', 'origin'],
    'Google': ['google', 'googleapis', 'gstatic'],
    'Cloudflare': ['cloudflare'],
    'Amazon': ['amazon', 'aws', 'cloudfront'],
    'Microsoft': ['microsoft', 'azure', 'msft'],
}


def verify_service_by_sni(sni: Optional[str], claimed_service: str) -> Tuple[bool, str]:
    """
    Verify if the SNI matches the claimed service.
    
    Args:
        sni: SNI hostname from TLS handshake
        claimed_service: Service claimed by DNS/IP lookup
        
    Returns:
        Tuple of (verified: bool, label: str)
        - If verified, returns (True, claimed_service)
        - If not verified, returns (False, "Şüpheli/Genel HTTPS")
    """
    if not sni:
        # No SNI available, mark as suspicious
        return (False, "Şüpheli/Genel HTTPS (SNI yok)")
    
    # Check if claimed service has keywords
    keywords = SERVICE_SNI_KEYWORDS.get(claimed_service, [])
    
    if not keywords:
        # Unknown service, just return the SNI as label
        return (True, f"HTTPS ({sni})")
    
    if sni_matches_service(sni, keywords):
        return (True, claimed_service)
    else:
        return (False, f"Şüpheli/Genel HTTPS ({sni})")
