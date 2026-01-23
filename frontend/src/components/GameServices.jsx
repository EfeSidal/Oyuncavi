import { Gamepad2 } from 'lucide-react'
import { getGameServiceStats } from '../utils/gameServices'

export default function GameServices({ data = [] }) {
    const services = getGameServiceStats(data)

    return (
        <div className="glass-card p-6 h-full">
            {/* Header */}
            <div className="flex items-center gap-3 mb-5 px-1">
                <div className="p-2.5 rounded-xl bg-purple-500/10 border border-purple-500/20 flex-shrink-0">
                    <Gamepad2 className="w-5 h-5 text-purple-400" />
                </div>
                <span className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
                    Oyun Servisleri
                </span>
            </div>

            {services.length === 0 ? (
                <div className="text-center text-slate-500 text-sm py-6 px-1">
                    Tespit edilmedi
                </div>
            ) : (
                <div className="space-y-3 px-1">
                    {services.slice(0, 4).map((service) => (
                        <div
                            key={service.key}
                            className={`flex items-center justify-between p-3 rounded-xl ${service.bgColor}`}
                        >
                            <span className={`text-sm font-medium ${service.color}`}>
                                {service.name}
                            </span>
                            <span className="text-xs text-slate-400 tabular-nums">{service.count}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
