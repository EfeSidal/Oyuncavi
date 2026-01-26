import { Network, Play, Pause, Zap, Settings, ChevronDown, RefreshCw } from 'lucide-react'
import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = "http://127.0.0.1:8000"

export default function ControlPanel({
    interfaceName,
    setInterfaceName,
    onStart,
    onDemo,
    loading,
    status
}) {
    const [packetCount, setPacketCount] = useState(200)
    const [interfaces, setInterfaces] = useState([])
    const [loadingInterfaces, setLoadingInterfaces] = useState(false)

    // Arayüzleri yükle
    const fetchInterfaces = async () => {
        setLoadingInterfaces(true)
        try {
            const res = await axios.get(`${API_URL}/interfaces`)
            if (res.data.status === "success" && res.data.interfaces) {
                setInterfaces(res.data.interfaces)
                // Varsayılan arayüzü ayarla
                if (res.data.default && !interfaceName) {
                    setInterfaceName(res.data.default)
                } else if (res.data.interfaces.length > 0 && !interfaceName) {
                    setInterfaceName(res.data.interfaces[0])
                }
            }
        } catch (error) {
            console.error("Arayüzler yüklenemedi:", error)
        }
        setLoadingInterfaces(false)
    }

    useEffect(() => {
        fetchInterfaces()
    }, [])

    return (
        <div className="glass-card p-8">
            {/* Header */}
            <div className="flex items-center gap-4 px-2 pb-6 mb-8 border-b border-slate-700/30">
                <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                    <Settings className="w-5 h-5 text-cyan-400" />
                </div>
                <span className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
                    Kontrol Paneli
                </span>
            </div>

            {/* Content with increased spacing */}
            <div className="space-y-8 px-2">
                {/* Network Interface */}
                <div className="space-y-3">
                    <div className="flex items-center justify-between">
                        <label className="block text-xs text-slate-500 font-medium uppercase tracking-wider">
                            Ağ Arayüzü
                        </label>
                        <button
                            onClick={fetchInterfaces}
                            disabled={loadingInterfaces}
                            className="p-1 rounded hover:bg-slate-700/50 transition-colors"
                            title="Arayüzleri yenile"
                        >
                            <RefreshCw className={`w-3 h-3 text-slate-500 ${loadingInterfaces ? 'animate-spin' : ''}`} />
                        </button>
                    </div>
                    <div className="relative">
                        <Network className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                        <select
                            value={interfaceName}
                            onChange={(e) => setInterfaceName(e.target.value)}
                            className="input pl-12 pr-10 py-3.5 font-mono text-sm appearance-none cursor-pointer w-full"
                        >
                            {interfaces.length === 0 ? (
                                <option value="">Yükleniyor...</option>
                            ) : (
                                interfaces.map((iface) => (
                                    <option key={iface} value={iface}>
                                        {iface}
                                    </option>
                                ))
                            )}
                        </select>
                        <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                    </div>
                    {interfaces.length === 0 && !loadingInterfaces && (
                        <p className="text-xs text-red-400">Ağ arayüzü bulunamadı!</p>
                    )}
                </div>

                {/* Packet Count Slider */}
                <div className="space-y-3">
                    <div className="flex justify-between items-center">
                        <label className="text-xs text-slate-500 font-medium uppercase tracking-wider">
                            Paket Sayısı
                        </label>
                        <span className="text-lg font-mono text-cyan-400 font-bold tabular-nums">{packetCount}</span>
                    </div>
                    <input
                        type="range"
                        min="50"
                        max="500"
                        step="50"
                        value={packetCount}
                        onChange={(e) => setPacketCount(parseInt(e.target.value))}
                        className="w-full h-2"
                    />
                    <div className="flex justify-between text-xs text-slate-600 tabular-nums pt-1">
                        <span>50</span>
                        <span>250</span>
                        <span>500</span>
                    </div>
                </div>

                {/* Action Buttons with clear separation */}
                <div className="pt-4 space-y-6">
                    {/* Start Scan Button */}
                    <button
                        onClick={() => onStart(packetCount)}
                        disabled={loading || status === 'scanning'}
                        className={`btn w-full py-4 text-base relative overflow-hidden group ${loading || status === 'scanning'
                            ? 'bg-slate-700 cursor-not-allowed'
                            : 'btn-primary'
                            }`}
                    >
                        {/* Animated Background */}
                        {status === 'scanning' && (
                            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 via-purple-500/20 to-cyan-500/20 animate-shimmer"></div>
                        )}

                        <span className="relative flex items-center justify-center gap-3">
                            {status === 'scanning' ? (
                                <>
                                    <Pause className="w-5 h-5 animate-pulse flex-shrink-0" />
                                    <span>Taranıyor...</span>
                                </>
                            ) : (
                                <>
                                    <Play className="w-5 h-5 group-hover:scale-110 transition-transform flex-shrink-0" />
                                    <span>Taramayı Başlat</span>
                                </>
                            )}
                        </span>
                    </button>

                    {/* Divider */}
                    <div className="flex items-center gap-3">
                        <div className="flex-1 h-px bg-slate-700/50"></div>
                        <span className="text-[10px] text-slate-600 uppercase">veya</span>
                        <div className="flex-1 h-px bg-slate-700/50"></div>
                    </div>

                    {/* Demo Button */}
                    <button
                        onClick={onDemo}
                        disabled={loading || status === 'scanning'}
                        className="btn btn-ghost w-full py-4 text-base flex items-center justify-center gap-3"
                    >
                        <Zap className="w-5 h-5 text-yellow-400 flex-shrink-0" />
                        <span>Demo Modu</span>
                    </button>
                </div>
            </div>

            {/* Status Indicator */}
            {status !== 'idle' && (
                <div className="mt-8 mx-2 space-y-4">
                    {/* Divider */}
                    <div className="flex items-center gap-3">
                        <div className="flex-1 h-px bg-slate-700/50"></div>
                        <span className="text-[10px] text-slate-600 uppercase">durum</span>
                        <div className="flex-1 h-px bg-slate-700/50"></div>
                    </div>

                    {/* Status Box */}
                    <div className={`flex items-center gap-3 px-5 py-4 rounded-xl text-sm font-medium animate-fade-in ${status === 'scanning'
                        ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'
                        : 'bg-green-500/10 text-green-400 border border-green-500/20'
                        }`}>
                        <span className={`w-3 h-3 rounded-full flex-shrink-0 ${status === 'scanning' ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'
                            }`}></span>
                        <span>{status === 'scanning' ? 'Ağ paketleri yakalanıyor...' : 'Tarama tamamlandı'}</span>
                    </div>
                </div>
            )}
        </div>
    )
}
