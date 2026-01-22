from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.capture import start_sniffer
from src.analysis import detect_anomalies
import pandas as pd
import os
import uvicorn

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
    "last_analysis": []
}

@app.get("/")
def read_root():
    return {"status": "OyuncuAvi Backend Calisiyor", "version": "2.0"}

@app.post("/start/{interface}")
def start_scan(interface: str, packet_count: int = 500, background_tasks: BackgroundTasks = None):
    """
    Arka planda ağ dinlemeyi başlatır.
    """
    if STATE["is_running"]:
        return {"status": "error", "message": "Zaten calisiyor"}

    STATE["is_running"] = True
    
    # Arka plan görevi (Sniffing işlemi API'yi kilitlemesin diye)
    def scan_task():
        print(f"[*] Dinleme basladi: {interface}")
        # Not: capture.py fonksiyonun dosya yolunu döndürmeli
        pcap_path = start_sniffer(interface, count=packet_count)
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
        return {"status": "running", "data": []}
    
    return {
        "status": "completed" if STATE["pcap_file"] else "idle",
        "data": STATE["last_analysis"]
    }

# Doğrudan çalıştırma için
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)