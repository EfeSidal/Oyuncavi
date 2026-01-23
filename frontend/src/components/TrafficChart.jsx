import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceDot } from 'recharts'
import { Activity, TrendingUp, Zap } from 'lucide-react'

const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload
        const isAnomaly = data.anomaly === -1

        return (
            <div className={`glass-card p-3 border ${isAnomaly ? 'border-red-500/30' : 'border-cyan-500/30'
                }`}>
                <div className="flex items-center gap-2 mb-2">
                    {isAnomaly && <span className="text-lg">⚠️</span>}
                    <span className={`text-xs font-semibold uppercase ${isAnomaly ? 'text-red-400' : 'text-cyan-400'
                        }`}>
                        {isAnomaly ? 'Anomali Tespit Edildi!' : 'Normal Trafik'}
                    </span>
                </div>
                <div className="space-y-1 text-xs">
                    <p className="text-slate-400">
                        Boyut: <span className="text-slate-200 font-mono font-semibold">{data.length} B</span>
                    </p>
                    <p className="text-slate-400">
                        Protokol: <span className="text-slate-200">{data.protocol === 6 ? 'TCP' : 'UDP'}</span>
                    </p>
                    <p className="text-slate-400">
                        Kaynak: <span className="text-slate-200 font-mono">{data.src_ip}</span>
                    </p>
                </div>
            </div>
        )
    }
    return null
}

export default function TrafficChart({ data = [], anomalies = [] }) {
    const chartData = data.map((d, i) => ({
        ...d,
        index: i,
        length: d.length
    }))

    const avgSize = data.length > 0
        ? Math.round(data.reduce((a, b) => a + b.length, 0) / data.length)
        : 0
    const maxSize = data.length > 0
        ? Math.max(...data.map(d => d.length))
        : 0

    if (data.length === 0) {
        return (
            <div className="glass-card h-full p-5 flex flex-col">
                <div className="flex items-center gap-2.5 mb-4 pl-1">
                    <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                        <Activity className="w-4 h-4 text-cyan-400" />
                    </div>
                    <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                        Trafik Analizi
                    </span>
                </div>

                <div className="flex-1 flex items-center justify-center">
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                        <div style={{ width: '80px', height: '80px', marginBottom: '16px', borderRadius: '16px', background: 'linear-gradient(to bottom right, rgba(51,65,85,0.5), rgba(30,41,59,0.5))', border: '1px solid rgba(71,85,105,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <TrendingUp className="w-10 h-10 text-slate-500" />
                        </div>
                        <p className="text-slate-400 font-medium">Henüz veri yok</p>
                        <p className="text-xs text-slate-600 mt-1">Taramayı başlatın</p>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="glass-card h-full p-5 flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between mb-4 px-1">
                <div className="flex items-center gap-2.5">
                    <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                        <Activity className="w-4 h-4 text-cyan-400" />
                    </div>
                    <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                        Trafik Analizi
                    </span>
                </div>

                {/* Legend */}
                <div className="flex items-center gap-4 text-xs">
                    <div className="flex items-center gap-1.5">
                        <span className="w-3 h-3 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500"></span>
                        <span className="text-slate-400">Paket Boyutu</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                        <span className="w-3 h-3 rounded-full bg-red-500 animate-pulse"></span>
                        <span className="text-slate-400">Anomali</span>
                    </div>
                </div>
            </div>

            {/* Chart */}
            <div className="flex-1 min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <defs>
                            <linearGradient id="colorLength" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.4} />
                                <stop offset="50%" stopColor="#8b5cf6" stopOpacity={0.2} />
                                <stop offset="100%" stopColor="#06b6d4" stopOpacity={0.05} />
                            </linearGradient>
                            <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                                <stop offset="0%" stopColor="#06b6d4" />
                                <stop offset="50%" stopColor="#8b5cf6" />
                                <stop offset="100%" stopColor="#06b6d4" />
                            </linearGradient>
                        </defs>
                        <XAxis
                            dataKey="index"
                            tick={{ fill: '#64748b', fontSize: 10 }}
                            axisLine={{ stroke: '#334155' }}
                            tickLine={false}
                        />
                        <YAxis
                            tick={{ fill: '#64748b', fontSize: 10 }}
                            axisLine={{ stroke: '#334155' }}
                            tickLine={false}
                            tickFormatter={(v) => `${v}B`}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Area
                            type="monotone"
                            dataKey="length"
                            stroke="url(#lineGradient)"
                            strokeWidth={2}
                            fill="url(#colorLength)"
                            dot={false}
                            activeDot={{
                                r: 6,
                                fill: '#06b6d4',
                                stroke: '#0f172a',
                                strokeWidth: 2,
                                style: { filter: 'drop-shadow(0 0 8px #06b6d4)' }
                            }}
                        />
                        {/* Anomaly Markers */}
                        {anomalies.map((a, i) => {
                            const idx = chartData.findIndex(d => d.time === a.time)
                            if (idx === -1) return null
                            return (
                                <ReferenceDot
                                    key={i}
                                    x={idx}
                                    y={a.length}
                                    r={5}
                                    fill="#ef4444"
                                    stroke="#0f172a"
                                    strokeWidth={2}
                                    style={{ filter: 'drop-shadow(0 0 8px #ef4444)' }}
                                />
                            )
                        })}
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            {/* Stats Footer */}
            <div className="flex items-center justify-between pt-4 mt-4 border-t border-slate-700/30">
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center flex-shrink-0">
                            <span className="text-xs text-cyan-400">E</span>
                        </div>
                        <div>
                            <p className="text-lg font-bold font-mono text-cyan-400 tabular-nums">{avgSize} B</p>
                            <p className="text-[10px] text-slate-500 uppercase">Ortalama</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center flex-shrink-0">
                            <Zap className="w-3.5 h-3.5 text-purple-400" />
                        </div>
                        <div>
                            <p className="text-lg font-bold font-mono text-purple-400 tabular-nums">{maxSize} B</p>
                            <p className="text-[10px] text-slate-500 uppercase">Maksimum</p>
                        </div>
                    </div>
                </div>

                <div className="text-right">
                    <p className="text-2xl font-bold font-mono text-slate-200 tabular-nums">{data.length}</p>
                    <p className="text-[10px] text-slate-500 uppercase">Toplam Paket</p>
                </div>
            </div>
        </div>
    )
}
