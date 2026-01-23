import { Users } from 'lucide-react'

export default function TopTalkers({ data = [] }) {
    // Count packets per source IP
    const ipCounts = {}
    data.forEach(packet => {
        const ip = packet.src_ip
        ipCounts[ip] = (ipCounts[ip] || 0) + 1
    })

    // Sort by count and get top 5
    const topIps = Object.entries(ipCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)

    const maxCount = topIps[0]?.[1] || 1

    return (
        <div className="glass-card p-4 h-full">
            {/* Header */}
            <div className="flex items-center gap-2.5 mb-3">
                <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                    <Users className="w-4 h-4 text-cyan-400" />
                </div>
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Top Kaynaklar
                </span>
            </div>

            {topIps.length === 0 ? (
                <div className="text-center text-slate-500 text-sm py-4">
                    Veri yok
                </div>
            ) : (
                <div className="space-y-2">
                    {topIps.map(([ip, count], idx) => (
                        <div key={ip} className="flex items-center gap-2">
                            <span className={`w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-bold flex-shrink-0 ${idx === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                                    idx === 1 ? 'bg-slate-500/20 text-slate-400' :
                                        idx === 2 ? 'bg-orange-500/20 text-orange-400' :
                                            'bg-slate-700/50 text-slate-500'
                                }`}>
                                {idx + 1}
                            </span>
                            <div className="flex-1 min-w-0">
                                <p className="text-xs font-mono text-slate-300 truncate">{ip}</p>
                                <div className="h-1 bg-slate-700/50 rounded-full mt-1 overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full"
                                        style={{ width: `${(count / maxCount) * 100}%` }}
                                    ></div>
                                </div>
                            </div>
                            <span className="text-xs font-mono text-slate-500 flex-shrink-0 tabular-nums">{count}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
