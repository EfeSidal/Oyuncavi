import matplotlib.pyplot as plt

def plot_traffic(df):
    if df is None or df.empty:
        return

    plt.figure(figsize=(10, 6))
    
    
    normal = df[df['anomaly'] == 1]
    plt.scatter(normal['time'], normal['length'], c='blue', s=10, label='Normal Trafik')
    
    
    anomalies = df[df['anomaly'] == -1]
    plt.scatter(anomalies['time'], anomalies['length'], c='red', s=30, label='Anomali (Şüpheli)')
    
    plt.title("OyuncuAvi: Ağ Trafiği Anomali Analizi")
    plt.xlabel("Zaman (sn)")
    plt.ylabel("Paket Boyutu (bytes)")
    plt.legend()
    plt.show()
