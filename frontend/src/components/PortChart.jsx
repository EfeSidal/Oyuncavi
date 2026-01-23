import { BarChart3 } from 'lucide-react'
import { BarChart, Bar, XAxis, ResponsiveContainer, Tooltip, Cell } from 'recharts'

const PORT_NAMES = {
    80: 'HTTP',
    443: 'HTTPS',
    22: 'SSH',
    53: 'DNS',
    3478: 'STUN',
    3389: 'RDP',
    27015: 'Steam',
    25565: 'MC',
    7777: 'Game'
}

export default function PortChart({ data = [] }) {
    // Count packets per destination port
    const portCounts = {}
    data.forEach(packet => {
        const port = packet.dst_port
        portCounts[port] = (portCounts[port] || 0) + 1
    })

    // Get top 5 ports
    const chartData = Object.entries(portCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([port, count]) => ({
            port: PORT_NAMES[port] || port,
            count
        }))

    return (
        <div className="glass-card p-4 h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center gap-2.5 mb-3">
                <div className="p-2 rounded-xl bg-green-500/10 border border-green-500/20 flex-shrink-0">
                    <BarChart3 className="w-4 h-4 text-green-400" />
                </div>
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Port Dağılımı
                </span>
            </div>

            {chartData.length === 0 ? (
                <div className="flex-1 flex items-center justify-center text-slate-500 text-sm">
                    Veri yok
                </div>
            ) : (
                <div className="flex-1 min-h-[100px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={chartData} layout="vertical" margin={{ left: 0, right: 10 }}>
                            <XAxis type="number" hide />
                            <Tooltip
                                contentStyle={{
                                    background: 'rgba(15,23,42,0.9)',
                                    border: '1px solid rgba(100,116,139,0.3)',
                                    borderRadius: '8px',
                                    fontSize: '12px'
                                }}
                            />
                            <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                                {chartData.map((_, index) => (
                                    <Cell key={`cell-${index}`} fill={`hsl(${180 + index * 30}, 70%, 50%)`} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}
        </div>
    )
}
