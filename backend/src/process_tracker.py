"""
Process Tracking Module for Application-Level Traffic Identification.

This module uses psutil to track active network connections and map them
to their owning processes. This enables accurate identification of which
application (Discord.exe, Steam, game executable, browser) is generating
specific network traffic.
"""

import psutil
from typing import Optional, Dict, Tuple, List
from dataclasses import dataclass
from fnmatch import fnmatch
import time

# --- KNOWN APPLICATION PATTERNS ---
# Maps application categories to their executable patterns (case-insensitive)
KNOWN_APPS: Dict[str, List[str]] = {
    'Discord': [
        'discord.exe',
        'discord ptb.exe',
        'discord canary.exe',
        'update.exe',  # Discord updater
    ],
    'Steam': [
        'steam.exe',
        'steamwebhelper.exe',
        'steamservice.exe',
        'gameoverlayui.exe',
    ],
    'Valve Games': [
        'csgo.exe',
        'cs2.exe',
        'hl2.exe',
        'dota2.exe',
        'tf.exe',
    ],
    'Riot Games': [
        'riotclientservices.exe',
        'riotclientux.exe',
        'riotclientuxrender.exe',
        'league of legends.exe',
        'leagueclient.exe',
        'leagueclientux.exe',
        'valorant.exe',
        'valorant-win64-shipping.exe',
        'riotgamesapi.exe',
    ],
    'Epic Games': [
        'epicgameslauncher.exe',
        'epicwebhelper.exe',
        'fortniteclient-win64-shipping.exe',
        'fortnitelauncher.exe',
        'unrealcefsubprocess.exe',
    ],
    'FiveM': [
        'fivem.exe',
        'fivem_b*.exe',
        'fivem_chromebrowser.exe',
        'citizenfx_ui_browser.exe',
    ],
    'GTA V': [
        'gta5.exe',
        'gtavlauncher.exe',
        'playgtav.exe',
    ],
    'Minecraft': [
        'javaw.exe',  # Minecraft Java runs in javaw
        'minecraft.exe',
        'minecraftlauncher.exe',
    ],
    'Blizzard': [
        'battle.net.exe',
        'battlenet.exe',
        'agent.exe',
        'overwatch.exe',
        'wow.exe',
        'hearthstone.exe',
        'diablo*.exe',
    ],
    'EA/Origin': [
        'origin.exe',
        'originwebhelperservice.exe',
        'eadesktop.exe',
        'eabackgroundservice.exe',
        'apex_legends.exe',
        'bf*.exe',
    ],
    'Ubisoft': [
        'upc.exe',
        'ubisoft connect.exe',
        'ubisoftgamelauncher.exe',
    ],
    'Xbox': [
        'xbox.exe',
        'xboxapp.exe',
        'gamingservices.exe',
        'gamingservicesnet.exe',
    ],
    'Twitch': [
        'twitch.exe',
        'twitchui.exe',
    ],
    'Browser': [
        'chrome.exe',
        'firefox.exe',
        'msedge.exe',
        'opera.exe',
        'brave.exe',
        'vivaldi.exe',
        'iexplore.exe',
    ],
}


@dataclass
class ProcessInfo:
    """Information about a process owning a network connection."""
    pid: int
    name: str
    exe_path: Optional[str]
    app_category: str
    is_verified: bool  # True if matches a known app pattern


# --- GLOBAL CONNECTION CACHE ---
# Maps (local_port, protocol) -> ProcessInfo
_connection_cache: Dict[Tuple[int, str], ProcessInfo] = {}
_cache_timestamp: float = 0
_cache_ttl: float = 5.0  # Cache valid for 5 seconds


def _identify_app_category(process_name: str) -> Tuple[str, bool]:
    """
    Identify the application category from process name.
    
    Args:
        process_name: Name of the process executable
        
    Returns:
        Tuple of (category_name, is_known_app)
    """
    process_name_lower = process_name.lower()
    
    for category, patterns in KNOWN_APPS.items():
        for pattern in patterns:
            pattern_lower = pattern.lower()
            # Use fnmatch for wildcard support (e.g., 'fivem_b*.exe')
            if fnmatch(process_name_lower, pattern_lower):
                return (category, True)
    
    return ("Uygulama Bilinmiyor", False)


def take_connection_snapshot() -> int:
    """
    Take a snapshot of current active network connections.
    Maps local ports to their owning processes.
    
    Returns:
        Number of connections captured
    """
    global _connection_cache, _cache_timestamp
    
    _connection_cache.clear()
    _cache_timestamp = time.time()
    
    try:
        connections = psutil.net_connections(kind='inet')
        
        for conn in connections:
            # Skip if no local address or no PID
            if not conn.laddr or not conn.pid:
                continue
            
            local_port = conn.laddr.port
            protocol = 'tcp' if conn.type == 1 else 'udp'  # SOCK_STREAM=1, SOCK_DGRAM=2
            
            try:
                proc = psutil.Process(conn.pid)
                proc_name = proc.name()
                
                try:
                    exe_path = proc.exe()
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    exe_path = None
                
                category, is_verified = _identify_app_category(proc_name)
                
                process_info = ProcessInfo(
                    pid=conn.pid,
                    name=proc_name,
                    exe_path=exe_path,
                    app_category=category,
                    is_verified=is_verified
                )
                
                _connection_cache[(local_port, protocol)] = process_info
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except psutil.AccessDenied:
        print("[!] Yönetici izinleri gerekli olabilir (psutil.AccessDenied)")
        return 0
    except Exception as e:
        print(f"[!] Bağlantı snapshot hatası: {e}")
        return 0
    
    return len(_connection_cache)


def _refresh_cache_if_needed():
    """Refresh the connection cache if it's stale."""
    global _cache_timestamp
    
    if time.time() - _cache_timestamp > _cache_ttl:
        take_connection_snapshot()


def get_process_by_port(port: int, protocol: str = 'tcp') -> Optional[ProcessInfo]:
    """
    Get process information for a given local port.
    
    Args:
        port: Local port number
        protocol: 'tcp' or 'udp'
        
    Returns:
        ProcessInfo if found, None otherwise
    """
    _refresh_cache_if_needed()
    
    # Try exact match
    key = (port, protocol.lower())
    if key in _connection_cache:
        return _connection_cache[key]
    
    # Try the other protocol
    alt_protocol = 'udp' if protocol == 'tcp' else 'tcp'
    alt_key = (port, alt_protocol)
    if alt_key in _connection_cache:
        return _connection_cache[alt_key]
    
    return None


def get_app_by_port(port: int) -> Optional[str]:
    """
    Get application category for a given port.
    Convenience function for utils.py integration.
    
    Args:
        port: Local port number
        
    Returns:
        Application category string or None
    """
    proc_info = get_process_by_port(port)
    if proc_info:
        return proc_info.app_category
    return None


def get_app_details_by_port(port: int) -> Optional[dict]:
    """
    Get detailed application info for a given port.
    
    Args:
        port: Local port number
        
    Returns:
        Dict with app details or None
    """
    proc_info = get_process_by_port(port)
    if proc_info:
        return {
            'pid': proc_info.pid,
            'process_name': proc_info.name,
            'exe_path': proc_info.exe_path,
            'app_category': proc_info.app_category,
            'is_verified': proc_info.is_verified,
        }
    return None


def is_verified_app(port: int) -> bool:
    """
    Check if traffic on this port comes from a known/verified application.
    
    Args:
        port: Local port number
        
    Returns:
        True if from known app, False otherwise
    """
    proc_info = get_process_by_port(port)
    return proc_info.is_verified if proc_info else False


def get_cache_stats() -> dict:
    """
    Get statistics about the connection cache.
    
    Returns:
        Dict with cache statistics
    """
    categories = {}
    verified_count = 0
    
    for proc_info in _connection_cache.values():
        cat = proc_info.app_category
        categories[cat] = categories.get(cat, 0) + 1
        if proc_info.is_verified:
            verified_count += 1
    
    return {
        'total_connections': len(_connection_cache),
        'verified_apps': verified_count,
        'unknown_apps': len(_connection_cache) - verified_count,
        'categories': categories,
        'cache_age_seconds': time.time() - _cache_timestamp if _cache_timestamp else 0,
    }
