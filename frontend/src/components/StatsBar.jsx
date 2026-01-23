import { BarChart3, Clock } from 'lucide-react'

export default function StatsBar({ data = [], status }) {
    const avgSize = data.length > 0 ? Math.round(data.reduce((a, b) => a + b.length, 0) / data.length) : 0
    const maxSize = data.length > 0 ? Math.max(...data.map(d => d.length)) : 0
    const tcpCount = data.filter(d => d.protocol === 6).length
    const udpCount = data.filter(d => d.protocol === 17).length

    const duration = data.length > 1
        ? ((data[data.length - 1].time - data[0].time)).toFixed(1)
        : '0.0'

    return (
        <div className="glass-card px-4 py-3">
            <div className="flex items-center justify-between gap-6">
                {/* Title */}
                <div className="flex items-center gap-2.5">
                    <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                        <BarChart3 className="w-4 h-4 text-cyan-400" />
                    </div>
                    <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                        Anlık İstatistikler
                    </span>
                </div>

                {/* Stats */}
                <div className="flex items-center gap-6 text-xs">
                    <div className="flex items-center gap-2">
                        <span className="text-slate-500">Ort Boyut:</span>
                        <span className="font-mono text-cyan-400 font-semibold tabular-nums">{avgSize} B</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <span className="text-slate-500">Maks Boyut:</span>
                        <span className="font-mono text-purple-400 font-semibold tabular-nums">{maxSize} B</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <span className="text-slate-500">TCP/UDP:</span>
                        <span className="font-mono tabular-nums">
                            <span className="text-cyan-400">{tcpCount}</span>
                            <span className="text-slate-600">/</span>
                            <span className="text-purple-400">{udpCount}</span>
                        </span>
                    </div>

                    <div className="flex items-center gap-2">
                        <Clock className="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                        <span className="font-mono text-slate-300 tabular-nums">{duration}s</span>
                    </div>

                    {status === 'scanning' && (
                        <div className="flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse flex-shrink-0"></span>
                            <span className="text-green-400">Canlı</span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
