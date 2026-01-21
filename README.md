<div align="center">

  

  # 🎮 Oyuncuavi (Gamer Hunt)
  
  **Network Traffic Analysis for Online Gaming**

  <p>
    <a href="https://github.com/EfeSidal/Oyuncavi">
      <img src="https://img.shields.io/github/languages/top/EfeSidal/Oyuncavi?style=flat-square&color=1e90ff" alt="Top Language" />
    </a>
    <a href="https://github.com/EfeSidal/Oyuncavi">
      <img src="https://img.shields.io/github/last-commit/EfeSidal/Oyuncavi?style=flat-square&color=ff69b4" alt="Last Commit" />
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/EfeSidal/Oyuncavi?style=flat-square&color=yellow" alt="License" />
    </a>
    <img src="https://img.shields.io/badge/Focus-Network_Forensics-red?style=flat-square" alt="Focus" />
  </p>

  <p>
    <a href="#about">About</a> •
    <a href="#features">Features</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#threat-model">Threat Model</a>
  </p>
</div>

---

## 🧐 About <a name="about"></a>

**Oyuncuavi** is a specialized network traffic analysis tool designed to demystify the communication patterns of online games. By parsing `.pcap` and `.pcapng` files, it identifies **game server connections**, analyzes **latency characteristics**, and maps **regional server infrastructure**.

Unlike generic traffic analyzers, Oyuncuavi focuses on the specific behaviors of gaming protocols (UDP floods, heartbeat packets, shared CDN usage).

> **Note:** This project focuses strictly on **analysis and observability**, not exploitation or cheating.

---

## 🚀 Features <a name="features"></a>

| Feature | Description |
| :--- | :--- |
| **📁 Packet Inspection** | Deep analysis of `.pcap` files captured via Wireshark/Tcpdump. |
| **🌍 Region Detection** | Identifies physical server locations (EU-West, NA-East, etc.) via IP metadata. |
| **⚡ Latency Analysis** | Estimates connection stability and potential lag spikes based on packet timing. |
| **🔍 Fingerprinting** | Uses heuristic patterns to distinguish game traffic from background OS noise. |

---

## 🛠 Installation <a name="installation"></a>

Clone the repository and install the dependencies.

```bash
# 1. Clone the repo
git clone [https://github.com/EfeSidal/Oyuncavi.git]

# 2. Navigate to the directory
cd Oyuncavi

# 3. Install dependencies (Assuming Python)
pip install -r requirements.txt
