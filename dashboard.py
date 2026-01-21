import streamlit as st
import pandas as pd
import plotly.express as px
import time
from scapy.all import get_if_list
from src.capture import start_sniffer
from src.analysis import detect_anomalies
from src.utils import get_ip_details

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="OyuncuAvi / GamerHunt",
    layout="wide",
    page_icon="🛡️"
)

# --- 2. CSS: DEPLOY BUTONUNU GİZLE ---
hide_menu_style = """
<style>
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'scan_data' not in st.session_state:
    st.session_state.scan_data = None

# --- 4. DİL SÖZLÜĞÜ (GÜNCELLENDİ) ---
TEXTS = {
    "tr": {
        "title": "🛡️ OYUNCUAVI: Ağ Tehdit Analizi",
        "net_iface_label": "Ağ Arayüzü (Interface)",
        "net_iface_help": "Wi-Fi veya Ethernet ismini yazın.",
        "btn_list_cards": "❓ Ağ Kartlarını Listele",
        "btn_inner_list": "Listele",  # <--- YENİ EKLENDİ
        "card_list_title": "Bilgisayardaki Kartlar:",
        "pkt_count": "Paket Sayısı",
        "loop_mode": "🔄 Otomatik Yenileme (Loop)",
        "start_btn": "Analizi Başlat",
        "prog_listen": "Paketler Dinleniyor...",
        "prog_ai": "Analiz Yapılıyor...",
        "prog_done": "Bitti.",
        "kpi_total": "Toplam Trafik",
        "kpi_threat": "Tehdit Sayısı",
        "kpi_ratio": "Risk Oranı",
        "chart_title": "Zaman vs Paket Boyutu",
        "chart_legend_normal": "Normal",
        "chart_legend_threat": "Şüpheli",
        "chart_x": "Zaman (sn)",
        "chart_y": "Boyut (byte)",
        "chart_legend": "Durum",
        "tab_threats": "Tespit Edilen Tehditler",
        "col_src": "Kaynak IP",
        "col_dst": "Hedef IP",
        "col_owner": "Sahip/Kurum",
        "col_country": "Ülke",
        "col_proto": "Protokol",
        "col_len": "Boyut",
        "alert_clean": "✅ Ağ Temiz.",
        "alert_error": "Veri yok veya analiz edilemedi.",
        "err_nofile": "Hata: Kart bulunamadı veya Npcap yüklü değil.",
        "unknown": "Bilinmiyor"
    },
    "en": {
        "title": "🛡️ GAMERHUNT: Network Threat Analysis",
        "net_iface_label": "Network Interface",
        "net_iface_help": "Type Wi-Fi or Ethernet.",
        "btn_list_cards": "❓ List Interfaces",
        "btn_inner_list": "List Cards", # <--- NEW ADDED
        "card_list_title": "Network Cards:",
        "pkt_count": "Packet Count",
        "loop_mode": "🔄 Auto Refresh Loop",
        "start_btn": "Start Analysis",
        "prog_listen": "Listening...",
        "prog_ai": "Analyzing...",
        "prog_done": "Done.",
        "kpi_total": "Total Traffic",
        "kpi_threat": "Threats",
        "kpi_ratio": "Risk Ratio",
        "chart_title": "Time vs Size",
        "chart_legend_normal": "Normal",
        "chart_legend_threat": "Suspicious",
        "chart_x": "Time (s)",
        "chart_y": "Size (bytes)",
        "chart_legend": "Status",
        "tab_threats": "Detected Threats",
        "col_src": "Source IP",
        "col_dst": "Dest IP",
        "col_owner": "Owner",
        "col_country": "Country",
        "col_proto": "Protocol",
        "col_len": "Size",
        "alert_clean": "✅ Network Clean.",
        "alert_error": "No data or analysis failed.",
        "err_nofile": "Error: Interface not found or Npcap missing.",
        "unknown": "Unknown"
    }
}

# --- 5. YAN MENÜ ---
lang_choice = st.sidebar.radio("Dil / Language", ["Türkçe", "English"], horizontal=True)
lang_code = "tr" if lang_choice == "Türkçe" else "en"
t = TEXTS[lang_code]

st.sidebar.markdown("---")

interface_name = st.sidebar.text_input(t["net_iface_label"], value="Wi-Fi", help=t["net_iface_help"])

with st.sidebar.expander(t["btn_list_cards"]):
    # ARTIK BURASI DA DİNAMİK:
    if st.button(t["btn_inner_list"]):
        try:
            cards = get_if_list()
            st.code("\n".join(cards))
        except:
            st.error("Liste alınamadı.")

packet_count = st.sidebar.slider(t["pkt_count"], 100, 3000, 500, step=100)
auto_refresh = st.sidebar.checkbox(t["loop_mode"], value=False)
btn_start = st.sidebar.button(t["start_btn"], type="primary")

st.sidebar.markdown("---")

# --- 6. ANA EKRAN VE MANTIK ---
st.title(t["title"])

PROTOCOL_MAP = { 6: "TCP", 17: "UDP", 1: "ICMP", 53: "DNS", 80: "HTTP", 443: "HTTPS" }

if btn_start or auto_refresh:
    
    bar = st.progress(0, text=t["prog_listen"])
    pcap_file = start_sniffer(interface_name, count=packet_count)
    bar.progress(50, text=t["prog_ai"])
    
    if pcap_file:
        df = detect_anomalies(pcap_file)
        bar.progress(100, text=t["prog_done"])
        time.sleep(0.2)
        bar.empty()
        
        if df is not None and not df.empty:
            st.session_state.scan_data = df
        else:
            st.session_state.scan_data = "EMPTY"
    else:
        st.session_state.scan_data = "ERROR"

# --- 7. GÖRSELLEŞTİRME ---
if st.session_state.scan_data is not None:
    
    if isinstance(st.session_state.scan_data, str):
        if st.session_state.scan_data == "ERROR":
            st.error(t["err_nofile"])
        elif st.session_state.scan_data == "EMPTY":
            st.warning(t["alert_error"])
            
    else:
        df = st.session_state.scan_data
        
        anomalies = df[df['anomaly'] == -1].copy()
        total = len(df)
        threats = len(anomalies)
        ratio = round((threats / total) * 100, 2) if total > 0 else 0
        
        k1, k2, k3 = st.columns(3)
        k1.metric(t["kpi_total"], total)
        k2.metric(t["kpi_threat"], threats, delta_color="inverse")
        k3.metric(t["kpi_ratio"], f"%{ratio}", delta_color="inverse")
        
        st.subheader(t["chart_title"])
        
        df['Status'] = df['anomaly'].map({1: t["chart_legend_normal"], -1: t["chart_legend_threat"]})
        color_map = {t["chart_legend_normal"]: "#1f77b4", t["chart_legend_threat"]: "#d62728"}
        
        fig = px.scatter(
            df, 
            x="time", 
            y="length", 
            color="Status",
            color_discrete_map=color_map,
            labels={
                "time": t["chart_x"], 
                "length": t["chart_y"],
                "Status": t["chart_legend"]
            },
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if threats > 0:
            st.subheader(t["tab_threats"])
            
            anomalies['Protocol_Name'] = anomalies['protocol'].map(PROTOCOL_MAP).fillna(t["unknown"])
            
            if 'Owner' not in anomalies.columns:
                unique_ips = anomalies['src_ip'].unique()[:10]
                ip_details = {ip: get_ip_details(ip) for ip in unique_ips}
                anomalies['Owner'] = anomalies['src_ip'].map(lambda x: ip_details.get(x, {}).get('org', '-'))
                anomalies['Country'] = anomalies['src_ip'].map(lambda x: ip_details.get(x, {}).get('country', '-'))
            
            display_df = anomalies[['src_ip', 'dst_ip', 'Owner', 'Country', 'Protocol_Name', 'length']].copy()
            display_df.columns = [t["col_src"], t["col_dst"], t["col_owner"], t["col_country"], t["col_proto"], t["col_len"]]
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.success(t["alert_clean"])

if auto_refresh:
    time.sleep(1)
    st.rerun()