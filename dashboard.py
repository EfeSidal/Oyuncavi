import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
# Scapy'den ağ kartlarını çeken fonksiyonu ekledik
from scapy.all import get_if_list
from src.capture import start_sniffer
from src.analysis import detect_anomalies
from src.utils import get_ip_owner

# --- 1. AYARLAR VE SABİTLER ---
st.set_page_config(
    page_title="OyuncuAvi Kontrol Paneli",
    layout="wide",
    page_icon="🎮"
)

PROTOCOL_MAP = {
    6: "TCP",
    17: "UDP",
    1: "ICMP",
    58: "ICMPv6"
}

# --- 2. YAN MENÜ (SIDEBAR) ---
st.sidebar.title("🛠️ Kontrol Paneli")
st.sidebar.markdown("---")

# --- YENİ EKLENEN KISIM: OTOMATİK AĞ LİSTESİ ---
try:
    # Bilgisayardaki ağ kartlarını otomatik bul
    iface_list = get_if_list()
    
    # Eğer liste boş gelirse (Driver hatası vs.) manuel girişe düş
    if not iface_list:
        interface_name = st.sidebar.text_input("Ağ Arayüzü (Interface)", value="Wi-Fi")
    else:
        # Listeyi kullanıcıya göster
        st.sidebar.success(f"✅ {len(iface_list)} Ağ Kartı Bulundu")
        interface_name = st.sidebar.selectbox(
            "Ağ Kartını Seç", 
            iface_list, 
            index=0,
            help="İnternete bağlı olduğun kartı seç (Genelde Wi-Fi veya Ethernet)"
        )
except Exception as e:
    st.sidebar.error("Kart listesi alınamadı, manuel giriniz.")
    interface_name = st.sidebar.text_input("Ağ Arayüzü (Interface)", value="Wi-Fi")
# -----------------------------------------------

packet_count = st.sidebar.slider("Paket Sayısı (Her Tarama)", min_value=100, max_value=2000, value=500, step=100)

st.sidebar.markdown("---")
# Mod Seçimi
auto_refresh = st.sidebar.checkbox("🔴 Canlı İzleme Modu (Loop)", value=False, help="Otomatik olarak sürekli tarama yapar.")
btn_start = st.sidebar.button("🔍 Tek Seferlik Analiz Başlat")

st.sidebar.markdown("---")
st.sidebar.info("Bu araç eğitim amaçlıdır. Veriler yerel olarak işlenir.")

# --- 3. ANA EKRAN TASARIMI ---
st.title("🎮 OyuncuAvi: Siber Güvenlik Analiz Paneli")
st.markdown(f"**Durum:** `Sistem Aktif` | **Hedef:** `{interface_name}` | **Mod:** `{'Canlı Akış' if auto_refresh else 'Manuel'}`")

# --- 4. ANALİZ MANTIĞI ---
if btn_start or auto_refresh:
    
    with st.status(f"🚀 {interface_name} üzerinden {packet_count} paket taranıyor...", expanded=True) as status:
        
        # A. TRAFİĞİ YAKALA
        st.write("📡 Paketler dinleniyor...")
        # Seçilen arayüz ismini fonksiyona gönderiyoruz
        pcap_file = start_sniffer(interface_name, count=packet_count)
        
        if pcap_file:
            st.write("🧠 Yapay Zeka analizi yapılıyor...")
            # B. ANALİZ ET
            df = detect_anomalies(pcap_file)
            
            status.update(label="Analiz Tamamlandı!", state="complete", expanded=False)
            
            if df is not None and not df.empty:
                # --- 5. METRİKLER (KPI) ---
                total_pkts = len(df)
                anomalies = df[df['anomaly'] == -1].copy()
                anomaly_count = len(anomalies)
                
                ratio = 0
                if total_pkts > 0:
                    ratio = round((anomaly_count / total_pkts) * 100, 2)
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Toplam Trafik", f"{total_pkts} pkt")
                col2.metric("Tespit Edilen Tehdit", anomaly_count, delta_color="inverse")
                col3.metric("Tehdit Oranı", f"%{ratio}")
                col4.metric("Ağ Durumu", "Kritik" if ratio > 5 else "Stabil", delta_color="normal" if ratio < 5 else "inverse")

                # --- 6. GRAFİK ALANI ---
                st.subheader("📊 Trafik Anomalisi Görselleştirme")
                
                fig, ax = plt.subplots(figsize=(12, 4))
                normal = df[df['anomaly'] == 1]
                ax.scatter(normal['time'], normal['length'], c='#1f77b4', s=15, label='Normal Trafik', alpha=0.6)
                anomalies = df[df['anomaly'] == -1].copy() # Copy uyarısını önlemek için
                ax.scatter(anomalies['time'], anomalies['length'], c='#d62728', s=40, label='Şüpheli Aktivite', edgecolors='black')
                
                ax.set_title(f"{interface_name} Üzerindeki Paket Boyutu Dağılımı")
                ax.set_xlabel("Zaman (sn)")
                ax.set_ylabel("Paket Boyutu (bytes)")
                ax.legend(loc="upper right")
                ax.grid(True, linestyle='--', alpha=0.3)
                st.pyplot(fig)

                # --- 7. DETAYLI TABLO ---
                if anomaly_count > 0:
                    st.subheader("🚨 Tespit Edilen Şüpheli Kaynaklar")
                    
                    if 'Owner' not in anomalies.columns:
                        st.caption("🔍 IP sahipleri sorgulanıyor (WHOIS)...")
                        unique_ips = anomalies['src_ip'].unique()
                        ip_owner_map = {ip: get_ip_owner(ip) for ip in unique_ips}
                        anomalies['Owner'] = anomalies['src_ip'].map(ip_owner_map)
                    
                    anomalies['protocol_name'] = anomalies['protocol'].map(PROTOCOL_MAP).fillna("Diğer")
                    
                    display_df = anomalies[['time', 'src_ip', 'dst_ip', 'Owner', 'protocol_name', 'length']].sort_values(by='length', ascending=False)
                    
                    st.dataframe(
                        display_df,
                        column_config={
                            "src_ip": "Saldırgan IP",
                            "dst_ip": "Hedef IP",
                            "Owner": "Kurum/Sahip",
                            "protocol_name": "Protokol",
                            "length": st.column_config.NumberColumn("Boyut", format="%d byte"),
                            "time": "Zaman Damgası"
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.success("✅ Ağ temiz. Herhangi bir anomali tespit edilmedi.")
            else:
                st.warning("Veri yakalandı ancak analiz edilemedi (Boş veri).")

    # --- 8. CANLI DÖNGÜ ---
    if auto_refresh:
        time.sleep(1)
        st.rerun()