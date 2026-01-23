import { Gamepad2 } from 'lucide-react'
import { getGameServiceStats } from '../utils/gameServices'

export default function GameServices({ data = [] }) {
    const services = getGameServiceStats(data)

    return (
        <div className="glass-card p-4 h-full">
            {/* Header */}
            <div className="flex items-center gap-2.5 mb-3">
                <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20 flex-shrink-0">
                    <Gamepad2 className="w-4 h-4 text-purple-400" />
                </div>
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Oyun Servisleri
                </span>
            </div>

            {services.length === 0 ? (
                <div className="text-center text-slate-500 text-sm py-4">
                    Tespit edilmedi
                </div>
            ) : (
                <div className="space-y-2">
                    {services.slice(0, 4).map((service) => (
                        <div
                            key={service.key}
                            className={`flex items-center justify-between p-2 rounded-lg ${service.bgColor}`}
                        >
                            <span className={`text-xs font-medium ${service.color}`}>
                                {service.name}
                            </span>
                            <span className="text-[10px] text-slate-400 tabular-nums">{service.count}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
