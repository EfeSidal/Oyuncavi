import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import { Layers } from 'lucide-react'

const COLORS = {
    TCP: '#06b6d4',
    UDP: '#8b5cf6'
}

const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
        const data = payload[0]
        return (
            <div className="glass-card p-3 border border-slate-700/50 text-xs">
                <p className="font-semibold" style={{ color: data.payload.fill }}>
                    {data.name}
                </p>
                <p className="text-slate-400 tabular-nums">
                    {data.value} paket ({data.payload.percentage}%)
                </p>
            </div>
        )
    }
    return null
}

export default function ProtocolChart({ data = [] }) {
    const tcpCount = data.filter(d => d.protocol === 6).length
    const udpCount = data.filter(d => d.protocol === 17).length
    const total = tcpCount + udpCount

    const chartData = [
        {
            name: 'TCP',
            value: tcpCount,
            fill: COLORS.TCP,
            percentage: total > 0 ? ((tcpCount / total) * 100).toFixed(0) : 0
        },
        {
            name: 'UDP',
            value: udpCount,
            fill: COLORS.UDP,
            percentage: total > 0 ? ((udpCount / total) * 100).toFixed(0) : 0
        }
    ]

    if (data.length === 0) {
        return (
            <div className="glass-card p-6 h-full">
                <div className="flex items-center gap-3 mb-5 px-1">
                    <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                        <Layers className="w-5 h-5 text-cyan-400" />
                    </div>
                    <span className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
                        Protokol Dağılımı
                    </span>
                </div>
                <div className="h-32 flex items-center justify-center text-slate-500 text-sm">
                    Veri bekleniyor...
                </div>
            </div>
        )
    }

    return (
        <div className="glass-card p-6 h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center gap-3 mb-5 px-1">
                <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                    <Layers className="w-5 h-5 text-cyan-400" />
                </div>
                <span className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
                    Protokol Dağılımı
                </span>
            </div>

            {/* Chart */}
            <div className="flex-1 min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            innerRadius="50%"
                            outerRadius="80%"
                            paddingAngle={4}
                            dataKey="value"
                            stroke="none"
                        >
                            {chartData.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={entry.fill}
                                    style={{ filter: 'drop-shadow(0 0 6px currentColor)' }}
                                />
                            ))}
                        </Pie>
                        <Tooltip content={<CustomTooltip />} />
                    </PieChart>
                </ResponsiveContainer>
            </div>

            {/* Legend */}
            <div className="flex items-center justify-center gap-8 pt-4 border-t border-slate-700/30 mt-3 px-1">
                <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full bg-cyan-400 flex-shrink-0" style={{ boxShadow: '0 0 8px #06b6d4' }}></span>
                    <span className="text-sm text-slate-400">TCP</span>
                    <span className="text-sm font-mono font-bold text-cyan-400 tabular-nums">({tcpCount})</span>
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full bg-purple-400 flex-shrink-0" style={{ boxShadow: '0 0 8px #8b5cf6' }}></span>
                    <span className="text-sm text-slate-400">UDP</span>
                    <span className="text-sm font-mono font-bold text-purple-400 tabular-nums">({udpCount})</span>
                </div>
            </div>
        </div>
    )
}
