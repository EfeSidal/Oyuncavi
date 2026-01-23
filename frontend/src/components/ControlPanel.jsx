import { Network, Play, Pause, Zap, Monitor } from 'lucide-react'
import { useState } from 'react'

export default function ControlPanel({
    interfaceName,
    setInterfaceName,
    onStart,
    onDemo,
    loading,
    status
}) {
    const [packetCount, setPacketCount] = useState(200)

    return (
        <div className="glass-card p-4 space-y-4">
            {/* Header */}
            <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                    <Monitor className="w-4 h-4 text-cyan-400" />
                </div>
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Kontrol Paneli
                </span>
            </div>

            {/* Network Interface */}
            <div className="space-y-1.5">
                <label className="block text-[11px] text-slate-500 font-medium uppercase tracking-wider">
                    Ağ Arayüzü
                </label>
                <div className="relative">
                    <Network className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                    <input
                        type="text"
                        value={interfaceName}
                        onChange={(e) => setInterfaceName(e.target.value)}
                        className="input pl-10 font-mono text-sm"
                        placeholder="Wi-Fi, Ethernet..."
                    />
                </div>
            </div>

            {/* Packet Count Slider */}
            <div className="space-y-1.5">
                <div className="flex justify-between items-center">
                    <label className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">
                        Paket Sayısı
                    </label>
                    <span className="text-sm font-mono text-cyan-400 font-bold tabular-nums">{packetCount}</span>
                </div>
                <input
                    type="range"
                    min="50"
                    max="500"
                    step="50"
                    value={packetCount}
                    onChange={(e) => setPacketCount(parseInt(e.target.value))}
                    className="w-full"
                />
                <div className="flex justify-between text-[10px] text-slate-600 tabular-nums">
                    <span>50</span>
                    <span>250</span>
                    <span>500</span>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-2 pt-1">
                {/* Start Scan Button */}
                <button
                    onClick={() => onStart(packetCount)}
                    disabled={loading || status === 'scanning'}
                    className={`btn w-full relative overflow-hidden group ${loading || status === 'scanning'
                            ? 'bg-slate-700 cursor-not-allowed'
                            : 'btn-primary'
                        }`}
                >
                    {/* Animated Background */}
                    {status === 'scanning' && (
                        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 via-purple-500/20 to-cyan-500/20 animate-shimmer"></div>
                    )}

                    <span className="relative flex items-center justify-center gap-2">
                        {status === 'scanning' ? (
                            <>
                                <Pause className="w-4 h-4 animate-pulse flex-shrink-0" />
                                <span>Taranıyor...</span>
                            </>
                        ) : (
                            <>
                                <Play className="w-4 h-4 group-hover:scale-110 transition-transform flex-shrink-0" />
                                <span>Taramayı Başlat</span>
                            </>
                        )}
                    </span>
                </button>

                {/* Demo Button */}
                <button
                    onClick={onDemo}
                    disabled={loading || status === 'scanning'}
                    className="btn btn-ghost w-full flex items-center justify-center gap-2"
                >
                    <Zap className="w-4 h-4 text-yellow-400 flex-shrink-0" />
                    <span>Demo Modu</span>
                </button>
            </div>

            {/* Status Indicator */}
            {status !== 'idle' && (
                <div className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium animate-fade-in ${status === 'scanning'
                        ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'
                        : 'bg-green-500/10 text-green-400 border border-green-500/20'
                    }`}>
                    <span className={`w-2 h-2 rounded-full flex-shrink-0 ${status === 'scanning' ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'
                        }`}></span>
                    <span>{status === 'scanning' ? 'Ağ paketleri yakalanıyor...' : 'Tarama tamamlandı'}</span>
                </div>
            )}
        </div>
    )
}
