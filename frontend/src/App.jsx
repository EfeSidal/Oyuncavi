import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Shield, Play, Activity, AlertTriangle, Server } from 'lucide-react'

// Backend Adresi (FastAPI varsayılan portu)
const API_URL = "http://127.0.0.1:8000"

function App() {
  const [interfaceName, setInterfaceName] = useState("Wi-Fi")
  const [status, setStatus] = useState("idle") // idle, scanning, completed
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)

  // Polling: Her 2 saniyede bir sonuçları kontrol et
  useEffect(() => {
    let interval
    if (status === "scanning") {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`${API_URL}/results`)
          if (res.data.status === "completed" || (res.data.data && res.data.data.length > 0)) {
            setData(res.data.data)
            if(res.data.status === "completed") {
                setStatus("completed")
                setLoading(false)
                clearInterval(interval)
            }
          }
        } catch (error) {
          console.error("Backend hatası:", error)
        }
      }, 2000)
    }
    return () => clearInterval(interval)
  }, [status])

  const startScan = async () => {
    setLoading(true)
    setStatus("scanning")
    setData([]) 
    try {
      // Backend'e "Başla" emri ver
      await axios.post(`${API_URL}/start/${interfaceName}?packet_count=200`)
    } catch (error) {
      alert("Hata: Backend (FastAPI) çalışmıyor olabilir! 'python main.py' yaptın mı?")
      setLoading(false)
      setStatus("idle")
    }
  }

  // Anomalileri filtrele
  const anomalies = data.filter(d => d.anomaly === -1)

  return (
    <div className="min-h-screen p-8 font-sans bg-slate-900 text-slate-100">
      {/* BAŞLIK */}
      <header className="flex items-center justify-between mb-10 border-b border-gray-700 pb-4">
        <div className="flex items-center gap-3">
          <Shield className="w-10 h-10 text-cyan-400" />
          <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-600 bg-clip-text text-transparent">
            OyuncuAvi v2.0
          </h1>
        </div>
        <div className="text-sm text-gray-400">
          Durum: <span className={status === "scanning" ? "text-yellow-400 animate-pulse" : "text-green-400"}>{status.toUpperCase()}</span>
        </div>
      </header>

      {/* KONTROL PANELİ */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 col-span-1 shadow-lg">
          <label className="block text-sm text-gray-400 mb-2">Ağ Arayüzü</label>
          <div className="flex gap-2">
            <input 
              type="text" 
              value={interfaceName}
              onChange={(e) => setInterfaceName(e.target.value)}
              className="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
            />
            <button 
              onClick={startScan}
              disabled={loading}
              className={`p-2 rounded font-bold transition-all flex items-center justify-center w-12 ${loading ? 'bg-gray-600 cursor-not-allowed' : 'bg-cyan-600 hover:bg-cyan-500'}`}
            >
              {loading ? <Activity className="animate-spin" /> : <Play />}
            </button>
          </div>
        </div>

        {/* KPI KARTLARI */}
        <KpiCard title="Toplam Paket" value={data.length} icon={<Server />} color="text-blue-400" />
        <KpiCard title="Tehdit Sayısı" value={anomalies.length} icon={<AlertTriangle />} color="text-red-500" />
        <KpiCard title="Risk Oranı" value={`%${data.length > 0 ? ((anomalies.length/data.length)*100).toFixed(1) : 0}`} icon={<Activity />} color="text-yellow-400" />
      </div>

      {/* GRAFİK ALANI */}
      {data.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* SOL: GRAFİK */}
          <div className="lg:col-span-2 bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
            <h3 className="text-xl font-bold mb-4 text-cyan-100 flex items-center gap-2">
              <Activity className="w-5 h-5" /> Trafik Analizi (Boyut / Zaman)
            </h3>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="time" hide />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Line type="monotone" dataKey="length" stroke="#22d3ee" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* SAĞ: TEHDİT LİSTESİ */}
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 overflow-hidden shadow-lg">
            <h3 className="text-xl font-bold mb-4 text-red-400 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" /> Tespit Edilen Tehditler
            </h3>
            <div className="overflow-y-auto h-[300px]">
              <table className="w-full text-left text-sm">
                <thead className="sticky top-0 bg-slate-800">
                  <tr className="text-gray-400 border-b border-gray-700">
                    <th className="pb-2">Kaynak IP</th>
                    <th className="pb-2">Hedef</th>
                    <th className="pb-2">Boyut</th>
                  </tr>
                </thead>
                <tbody>
                  {anomalies.length === 0 ? (
                    <tr><td colSpan="3" className="text-center py-10 text-green-500">✅ Ağ Temiz</td></tr>
                  ) : (
                    anomalies.map((item, idx) => (
                      <tr key={idx} className="border-b border-gray-700/50 hover:bg-slate-700/50">
                        <td className="py-2 text-red-300 font-mono">{item.src_ip}</td>
                        <td className="py-2 text-gray-300 font-mono">{item.dst_ip}</td>
                        <td className="py-2 text-yellow-300">{item.length} B</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// KPI Kart Bileşeni
function KpiCard({ title, value, icon, color }) {
  return (
    <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex items-center gap-4 hover:border-cyan-500/50 transition-all">
      <div className={`p-4 rounded-lg bg-slate-900 ${color}`}>{icon}</div>
      <div>
        <p className="text-sm text-gray-400">{title}</p>
        <p className="text-3xl font-bold text-white">{value}</p>
      </div>
    </div>
  )
}

export default App