import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os
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

# --- 2. CSS ---
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

# --- 4. DİL SÖZLÜĞÜ ---
TEXTS = {
    "tr": {
        "title": "🛡️ OYUNCUAVI: Ağ Tehdit Analizi & Oyun İstihbaratı",
        "net_iface_label": "Ağ Arayüzü",
        "net_iface_help": "Wi-Fi veya Ethernet ismini yazın.",
        "demo_mode": "🧪 Örnek Veri ile Test Et (Demo Modu)",
        "btn_list_cards": "❓ Ağ Kartlarını Listele",
        "btn_inner_list": "Listele",
        "pkt_count": "Paket Sayısı",
        "loop_mode": "🔄 Otomatik Yenileme",
        "start_btn": "Analizi Başlat",
        "prog_listen": "Paketler Dinleniyor...",
        "prog_ai": "Yapay Zeka & Oyun İmzaları Analiz Ediliyor...",
        "prog_done": "Tamamlandı.",
        "kpi_total": "Toplam Trafik",
        "kpi_threat": "Tehdit Sayısı",
        "kpi_ratio": "Risk Oranı",
        "tab_chart": "📊 Analiz Grafiği",
        "tab_map": "🌍 Dünya Haritası",
        "tab_list": "🚨 Detaylı Tehdit Listesi",
        "map_title": "Saldırı Kaynaklarının Coğrafi Dağılımı",
        "col_src": "Kaynak IP",
        "col_dst": "Hedef IP",
        "col_owner": "Sahip/Kurum",
        "col_country": "Ülke",
        "col_service": "Servis/Oyun",
        "col_len": "Boyut",
        "chart_x": "Zaman (sn)",
        "chart_y": "Boyut (byte)",
        "chart_legend": "Durum",
        "chart_legend_normal": "Normal",
        "chart_legend_threat": "Şüpheli",
        "alert_clean": "✅ Ağ Temiz.",
        "alert_malicious": "⚠️ KARA LİSTE TESPİTİ! Zararlı IP Bulundu:",
        "alert_error": "Veri yok veya analiz edilemedi.",
        "err_nofile": "Hata: Kart bulunamadı veya Npcap yüklü değil.",
        "err_nosample": "Hata: Örnek dosya bulunamadı! Lütfen 'generate_sample.py' dosyasını çalıştırın."
    },
    "en": {
        "title": "🛡️ GAMERHUNT: Network Threat Analysis & Game Intel",
        "net_iface_label": "Network Interface",
        "net_iface_help": "Type Wi-Fi or Ethernet.",
        "demo_mode": "🧪 Test with Sample Data (Demo Mode)",
        "btn_list_cards": "❓ List Interfaces",
        "btn_inner_list": "List Cards",
        "pkt_count": "Packet Count",
        "loop_mode": "🔄 Auto Refresh Loop",
        "start_btn": "Start Analysis",
        "prog_listen": "Listening...",
        "prog_ai": "Analyzing AI & Game Signatures...",
        "prog_done": "Done.",
        "kpi_total": "Total Traffic",
        "kpi_threat": "Threats",
        "kpi_ratio": "Risk Ratio",
        "tab_chart": "📊 Analysis Chart",
        "tab_map": "🌍 World Map",
        "tab_list": "🚨 Detailed Threat List",
        "map_title": "Geographic Distribution of Threats",
        "col_src": "Source IP",
        "col_dst": "Dest IP",
        "col_owner": "Owner",
        "col_country": "Country",
        "col_service": "Service/Game",
        "col_len": "Size",
        "chart_x": "Time (s)",
        "chart_y": "Size (bytes)",
        "chart_legend": "Status",
        "chart_legend_normal": "Normal",
        "chart_legend_threat": "Suspicious",
        "alert_clean": "✅ Network Clean.",
        "alert_malicious": "⚠️ BLACKLIST DETECTED! Malicious IP Found:",
        "alert_error": "No data or analysis failed.",
        "err_nofile": "Error: Interface not found or Npcap missing.",
        "err_nosample": "Error: Sample file not found! Please run 'generate_sample.py'."
    }
}

# --- 5. YAN MENÜ ---
lang_choice = st.sidebar.radio("Dil / Language", ["Türkçe", "English"], horizontal=True)
lang_code = "tr" if lang_choice == "Türkçe" else "en"
t = TEXTS[lang_code]

st.sidebar.markdown("---")

use_demo = st.sidebar.checkbox(t["demo_mode"], value=False)

if not use_demo:
    interface_name = st.sidebar.text_input(t["net_iface_label"], value="Wi-Fi", help=t["net_iface_help"])
    with st.sidebar.expander(t["btn_list_cards"]):
        if st.button(t["btn_inner_list"]):
            try:
                cards = get_if_list()
                st.code("\n".join(cards))
            except:
                st.error("Error")
    packet_count = st.sidebar.slider(t["pkt_count"], 100, 3000, 500, step=100)
    auto_refresh = st.sidebar.checkbox(t["loop_mode"], value=False)
else:
    st.sidebar.info("📂 Demo Modu: 'samples/sample_game_traffic.pcap' dosyası analiz edilecek.")
    auto_refresh = False

btn_start = st.sidebar.button(t["start_btn"], type="primary")

st.sidebar.markdown("---")

# --- 6. MANTIK ---
st.title(t["title"])

if btn_start or auto_refresh:
    pcap_file = None
    
    if use_demo:
        sample_path = os.path.join("samples", "sample_game_traffic.pcap")
        if os.path.exists(sample_path):
            pcap_file = sample_path
            st.toast("Dosya yüklendi: Demo Modu Aktif", icon="🧪")
        else:
            st.error(t["err_nosample"])
    else:
        bar = st.progress(0, text=t["prog_listen"])
        pcap_file = start_sniffer(interface_name, count=packet_count)
        bar.progress(50, text=t["prog_ai"])

    if pcap_file:
        df = detect_anomalies(pcap_file)
        
        if not use_demo:
            bar.progress(100, text=t["prog_done"])
            time.sleep(0.2)
            bar.empty()
        
        if df is not None and not df.empty:
            st.session_state.scan_data = df
        else:
            st.session_state.scan_data = "EMPTY"
    elif not use_demo:
        st.session_state.scan_data = "ERROR"

# --- 7. GÖRSELLEŞTİRME (HATA DÜZELTİLEN KISIM) ---
# Önce 'None' kontrolü, sonra string kontrolü yapıyoruz.
if st.session_state.scan_data is not None:
    
    # Eğer gelen veri bir hata mesajıysa (String ise)
    if isinstance(st.session_state.scan_data, str):
        if st.session_state.scan_data == "ERROR":
            st.error(t["err_nofile"])
        elif st.session_state.scan_data == "EMPTY":
            st.warning(t["alert_error"])
            
    # Eğer gelen veri gerçek bir DataFrame ise
    else:
        df = st.session_state.scan_data
        anomalies = df[df['anomaly'] == -1].copy()
        total = len(df)
        threats = len(anomalies)
        ratio = round((threats / total) * 100, 2) if total > 0 else 0
        
        if 'Service' not in anomalies.columns:
            unique_ips = anomalies['src_ip'].unique()[:20]
            details_map = {}
            for ip in unique_ips:
                try:
                    port = df[df['src_ip'] == ip]['dst_port'].iloc[0]
                except:
                    port = 0
                details_map[ip] = get_ip_details(ip, port)
            
            anomalies['Owner'] = anomalies['src_ip'].map(lambda x: details_map.get(x, {}).get('org', '-'))
            anomalies['Country'] = anomalies['src_ip'].map(lambda x: details_map.get(x, {}).get('country', 'Unknown'))
            anomalies['Service'] = anomalies['src_ip'].map(lambda x: details_map.get(x, {}).get('service', 'Unknown'))
            anomalies['Is_Bad'] = anomalies['src_ip'].map(lambda x: details_map.get(x, {}).get('is_malicious', False))

        k1, k2, k3 = st.columns(3)
        k1.metric(t["kpi_total"], total)
        k2.metric(t["kpi_threat"], threats, delta_color="inverse")
        k3.metric(t["kpi_ratio"], f"%{ratio}", delta_color="inverse")

        malicious_ips = anomalies[anomalies.get('Is_Bad', False) == True]
        if not malicious_ips.empty:
            st.error(f"{t['alert_malicious']} {malicious_ips['src_ip'].unique()}")

        tab1, tab2, tab3 = st.tabs([t["tab_chart"], t["tab_map"], t["tab_list"]])

        with tab1:
            df['Status'] = df['anomaly'].map({1: t["chart_legend_normal"], -1: t["chart_legend_threat"]})
            color_map = {t["chart_legend_normal"]: "#1f77b4", t["chart_legend_threat"]: "#d62728"}
            fig = px.scatter(df, x="time", y="length", color="Status", color_discrete_map=color_map,
                             labels={"time": t["chart_x"], "length": t["chart_y"], "Status": t["chart_legend"]}, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader(t["map_title"])
            if threats > 0:
                cnt = anomalies['Country'].value_counts().reset_index()
                cnt.columns = ['Country', 'Count']
                fig_map = px.choropleth(cnt, locations="Country", locationmode="country names", color="Count", color_continuous_scale="Reds")
                fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info(t["alert_clean"])

        with tab3:
            if threats > 0:
                show = anomalies[['src_ip', 'dst_ip', 'Owner', 'Country', 'Service', 'length']].copy()
                show.columns = [t["col_src"], t["col_dst"], t["col_owner"], t["col_country"], t["col_service"], t["col_len"]]
                st.dataframe(show, use_container_width=True)
            else:
                st.success(t["alert_clean"])

if auto_refresh:
    time.sleep(1)
    st.rerun()