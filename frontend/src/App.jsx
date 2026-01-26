import { useState, useEffect } from 'react'
import axios from 'axios'
import { Server, AlertTriangle, Activity, Globe } from 'lucide-react'

// Components
import Header from './components/Header'
import KpiCard from './components/KpiCard'
import ControlPanel from './components/ControlPanel'
import TrafficChart from './components/TrafficChart'
import ThreatTable from './components/ThreatTable'
import ProtocolChart from './components/ProtocolChart'
import ExportPanel from './components/ExportPanel'
import TopTalkers from './components/TopTalkers'
import StatsBar from './components/StatsBar'
import PortChart from './components/PortChart'
import GameServices from './components/GameServices'

// Context
import { useAlerts } from './context/AlertContext'
import { useSettings } from './context/SettingsContext'

// Hooks
import { useGameSocket } from './hooks/useGameSocket'

// Backend URL
const API_URL = "http://127.0.0.1:8000"

// Demo data generator with game services
function generateDemoData() {
  const packets = []
  const now = Date.now() / 1000

  // Game service ports
  const gamePorts = [27015, 27016, 3478, 7777, 443, 80, 53, 3389, 25565, 5223]

  for (let i = 0; i < 200; i++) {
    const isAnomaly = Math.random() < 0.08
    const baseLength = isAnomaly ? 1200 + Math.random() * 800 : 64 + Math.random() * 500
    const isGameTraffic = Math.random() > 0.4

    packets.push({
      src_ip: isAnomaly
        ? `${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`
        : `192.168.1.${Math.floor(Math.random() * 50)}`,
      dst_ip: isGameTraffic
        ? `${['162.254', '104.160', '24.105', '18.188'][Math.floor(Math.random() * 4)]}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`
        : `${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
      src_port: 1024 + Math.floor(Math.random() * 64000),
      dst_port: gamePorts[Math.floor(Math.random() * gamePorts.length)],
      protocol: Math.random() > 0.3 ? 6 : 17,
      length: Math.floor(baseLength),
      time: now + i * 0.1,
      iat: Math.random() * 0.5,
      jitter: Math.random() * 0.1,
      anomaly: isAnomaly ? -1 : 1
    })
  }

  return packets
}

function App() {
  const [interfaceName, setInterfaceName] = useState("Wi-Fi")
  const [status, setStatus] = useState("idle")
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)

  const { addAlert } = useAlerts()
  const { settings } = useSettings()

  // WebSocket bağlantısı
  const { isConnected, lastMessage } = useGameSocket()

  // Socket mesajlarını dinle
  useEffect(() => {
    if (!lastMessage) return

    // Status mesajları
    if (lastMessage.type === "status") {
      if (lastMessage.message === "scanning") {
        setLoading(true)
        setStatus("scanning")
      } else if (lastMessage.message === "completed") {
        setLoading(false)
        setStatus("completed")
      }
    }

    // Yeni veri mesajları
    if (lastMessage.type === "new_data" && lastMessage.data) {
      setData(lastMessage.data)
      setLoading(false)
      setStatus("completed")

      // Alert on completion
      const anomalyCount = lastMessage.data.filter(d => d.anomaly === -1).length
      if (anomalyCount > 0) {
        addAlert({
          type: 'threat',
          message: `Tarama tamamlandı: ${anomalyCount} tehdit tespit edildi!`,
          playSound: settings.soundEnabled
        })
      } else {
        addAlert({
          type: 'success',
          message: 'Tarama tamamlandı: Tehdit bulunamadı.'
        })
      }
    }

    // Hata mesajları
    if (lastMessage.type === "error") {
      setLoading(false)
      setStatus("idle")
      addAlert({
        type: 'threat',
        message: lastMessage.message || 'Bir hata oluştu',
        playSound: true
      })
    }
  }, [lastMessage, addAlert, settings.soundEnabled])

  const startScan = async (packetCount = 200) => {
    setLoading(true)
    setStatus("scanning")
    setData([])
    addAlert({
      type: 'info',
      message: `Tarama başlatıldı: ${interfaceName} üzerinde ${packetCount} paket`
    })
    try {
      const res = await axios.post(`${API_URL}/start/${interfaceName}?packet_count=${packetCount}`)

      // API'den hata dönerse
      if (res.data.status === "error") {
        addAlert({
          type: 'threat',
          message: res.data.message || 'Ağ arayüzü bulunamadı!',
          playSound: true
        })
        setLoading(false)
        setStatus("idle")
        return
      }
    } catch (error) {
      addAlert({
        type: 'threat',
        message: 'Backend bağlantı hatası! python main.py çalıştırın.',
        playSound: true
      })
      setLoading(false)
      setStatus("idle")
      setIsConnected(false)
    }
  }

  const startDemo = () => {
    setLoading(true)
    setStatus("scanning")
    setData([])
    addAlert({
      type: 'info',
      message: 'Demo modu başlatıldı...'
    })

    setTimeout(() => {
      const demoData = generateDemoData()
      setData(demoData)
      setStatus("completed")
      setLoading(false)

      const anomalyCount = demoData.filter(d => d.anomaly === -1).length
      addAlert({
        type: anomalyCount > 0 ? 'threat' : 'success',
        message: `Demo tamamlandı: ${anomalyCount} tehdit tespit edildi!`,
        playSound: anomalyCount > 0 && settings.soundEnabled
      })
    }, 2000)
  }

  const anomalies = data.filter(d => d.anomaly === -1)
  const uniqueIps = new Set(data.map(d => d.src_ip.split('.').slice(0, 2).join('.')))

  return (
    <div className="h-screen max-h-screen overflow-hidden p-5 relative flex flex-col" style={{ background: 'var(--gradient-dark)' }}>
      {/* Cyber Grid Background */}
      <div className="cyber-grid"></div>

      {/* Main Content */}
      <div className="relative z-10 w-full h-full flex flex-col gap-5">
        {/* Header */}
        <Header status={status} isConnected={isConnected} />

        {/* Stats Bar */}
        {data.length > 0 && (
          <div className="animate-fade-in">
            <StatsBar data={data} status={status} />
          </div>
        )}

        {/* Main Grid */}
        <div className="flex-1 grid grid-cols-12 gap-5 min-h-0">

          {/* Left Sidebar */}
          <div className="col-span-2 flex flex-col gap-5 overflow-hidden">
            <ControlPanel
              interfaceName={interfaceName}
              setInterfaceName={setInterfaceName}
              onStart={startScan}
              onDemo={startDemo}
              loading={loading}
              status={status}
            />

            {data.length > 0 && (
              <>
                <ExportPanel data={data} anomalies={anomalies} />
                <div className="flex-1 min-h-0">
                  <ProtocolChart data={data} />
                </div>
              </>
            )}
          </div>

          {/* Main Content Area */}
          <div className="col-span-7 flex flex-col gap-5">
            {/* KPI Cards Row */}
            <div className="grid grid-cols-4 gap-4">
              <KpiCard
                title="Toplam Paket"
                value={data.length}
                icon={<Server className="w-5 h-5" />}
                color="text-cyan-400"
                delay={0}
              />
              <KpiCard
                title="Tespit Edilen Tehdit"
                value={anomalies.length}
                icon={<AlertTriangle className="w-5 h-5" />}
                color="text-red-400"
                delay={100}
              />
              <KpiCard
                title="Risk Oranı"
                value={data.length > 0 ? `%${((anomalies.length / data.length) * 100).toFixed(1)}` : '%0'}
                icon={<Activity className="w-5 h-5" />}
                color="text-yellow-400"
                delay={200}
              />
              <KpiCard
                title="Benzersiz Kaynak"
                value={uniqueIps.size}
                icon={<Globe className="w-5 h-5" />}
                color="text-purple-400"
                delay={300}
              />
            </div>

            {/* Traffic Chart */}
            <div className="flex-1 animate-fade-in min-h-0">
              <TrafficChart data={data} anomalies={anomalies} />
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="col-span-3 flex flex-col gap-5 overflow-hidden">
            {/* Threat Table */}
            <div className="flex-1 min-h-0 overflow-hidden">
              <ThreatTable threats={anomalies} />
            </div>

            {/* Bottom Row */}
            {data.length > 0 && (
              <div className="grid grid-cols-2 gap-4 animate-fade-in">
                <TopTalkers data={data} />
                <GameServices data={data} />
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="py-2 text-center text-xs" style={{ color: 'var(--color-text-muted)' }}>
          OyuncuAvi v2.0 — AI-Powered Network Threat Analysis
        </div>
      </div>
    </div>
  )
}

export default App