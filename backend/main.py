from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.capture import start_sniffer
from src.analysis import detect_anomalies
import pandas as pd
import os
import uvicorn

# Windows'ta okunabilir arayüz isimleri için
try:
    from scapy.arch.windows import get_windows_if_list
    WINDOWS = True
except ImportError:
    WINDOWS = False

from scapy.all import get_if_list, conf

app = FastAPI(title="OyuncuAvi API", version="2.0")

# --- CORS AYARLARI ---
# React (Frontend) farklı portta çalışacağı için izin vermemiz lazım
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için ileride "http://localhost:5173" yapacağız
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- GLOBAL DEĞİŞKENLER ---
# Basit tutmak için veriyi hafızada tutuyoruz (Production'da veritabanı gerekir)
STATE = {
    "is_running": False,
    "pcap_file": None,
    "last_analysis": [],
    "error": None
}

# Arayüz isim eşleştirmesi (GUID -> Okunabilir isim)
INTERFACE_MAP = {}

def build_interface_map():
    """Windows arayüzlerinin GUID -> isim eşleştirmesini oluşturur"""
    global INTERFACE_MAP
    INTERFACE_MAP = {}
    if WINDOWS:
        try:
            win_ifaces = get_windows_if_list()
            for iface in win_ifaces:
                guid = iface.get('guid', '')  # Zaten {GUID} formatında
                name = iface.get('name', '') or iface.get('description', '')
                npf_name = "\\Device\\NPF_" + guid  # Süslü parantez ekleme, zaten var
                if name:
                    INTERFACE_MAP[npf_name] = name
                    INTERFACE_MAP[name] = npf_name  # Ters eşleştirme
        except Exception as e:
            print(f"Arayüz haritası oluşturulamadı: {e}")

# Başlangıçta haritayı oluştur
build_interface_map()

@app.get("/")
def read_root():
    return {"status": "OyuncuAvi Backend Calisiyor", "version": "2.0"}

@app.get("/interfaces")
def list_interfaces():
    """
    Sistemdeki mevcut ağ arayüzlerini listeler.
    """
    try:
        # Haritayı güncelle
        build_interface_map()
        
        if WINDOWS:
            # Windows'ta okunabilir isimler kullan
            win_ifaces = get_windows_if_list()
            interfaces = []
            default_iface = None
            
            for iface in win_ifaces:
                name = iface.get('name', '') or iface.get('description', '')
                if name:
                    interfaces.append(name)
                    # IP adresi olan ilk arayüzü varsayılan yap
                    if not default_iface and iface.get('ips'):
                        for ip in iface.get('ips', []):
                            if isinstance(ip, str) and ip.startswith('192.168') or ip.startswith('10.') or ip.startswith('172.'):
                                default_iface = name
                                break
            
            if not default_iface and interfaces:
                default_iface = interfaces[0]
            
            return {
                "status": "success",
                "interfaces": interfaces,
                "default": default_iface
            }
        else:
            # Linux/Mac
            interfaces = get_if_list()
            try:
                default_iface = str(conf.iface) if conf.iface else None
            except:
                default_iface = interfaces[0] if interfaces else None
            
            return {
                "status": "success",
                "interfaces": interfaces,
                "default": default_iface
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Arayüzler listelenemedi: {str(e)}",
            "interfaces": []
        }

@app.post("/start/{interface}")
def start_scan(interface: str, packet_count: int = 500, background_tasks: BackgroundTasks = None):
    """
    Arka planda ağ dinlemeyi başlatır.
    """
    if STATE["is_running"]:
        return {"status": "error", "message": "Zaten calisiyor"}

    # Windows'ta okunabilir ismi GUID'e çevir
    actual_interface = interface
    if WINDOWS:
        build_interface_map()
        if interface in INTERFACE_MAP:
            actual_interface = INTERFACE_MAP[interface]
        else:
            # GUID formatında mı kontrol et
            available_interfaces = get_if_list()
            if interface not in available_interfaces:
                return {
                    "status": "error", 
                    "message": f"Ağ arayüzü bulunamadı: '{interface}'"
                }

    STATE["is_running"] = True
    STATE["error"] = None
    
    # Arka plan görevi (Sniffing işlemi API'yi kilitlemesin diye)
    def scan_task():
        print(f"[*] Dinleme basladi: {actual_interface}")
        try:
            # Not: capture.py fonksiyonun dosya yolunu döndürmeli
            pcap_path = start_sniffer(actual_interface, count=packet_count)
            STATE["pcap_file"] = pcap_path
            
            # Analiz Yap
            if pcap_path and os.path.exists(pcap_path):
                print("[*] Analiz yapiliyor...")
                df = detect_anomalies(pcap_path)
                if df is not None and not df.empty:
                    # DataFrame'i JSON formatına çevirip sakla
                    STATE["last_analysis"] = df.to_dict(orient="records")
                else:
                    STATE["last_analysis"] = []
                    STATE["error"] = "Paket yakalanamadı veya analiz başarısız"
            else:
                STATE["last_analysis"] = []
                STATE["error"] = "Ağ trafiği yakalanamadı. Arayüzü kontrol edin."
        except Exception as e:
            STATE["error"] = f"Tarama hatası: {str(e)}"
            STATE["last_analysis"] = []
        
        STATE["is_running"] = False
        print("[*] Islem tamamlandi.")

    background_tasks.add_task(scan_task)
    return {"status": "started", "message": f"{interface} uzerinde dinleme baslatildi"}

@app.get("/results")
def get_results():
    """
    Son analizin sonuçlarını döndürür.
    """
    if STATE["is_running"]:
        return {"status": "running", "data": [], "error": None}
    
    # Hata varsa error status döndür
    if STATE["error"]:
        return {
            "status": "error",
            "data": [],
            "error": STATE["error"]
        }
    
    return {
        "status": "completed" if STATE["pcap_file"] else "idle",
        "data": STATE["last_analysis"],
        "error": None
    }

# Doğrudan çalıştırma için
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)