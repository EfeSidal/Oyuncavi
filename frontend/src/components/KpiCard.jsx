import { useEffect, useState } from 'react'

export default function KpiCard({ title, value, icon, color = 'text-cyan-400', delay = 0, trend = null }) {
    const [displayValue, setDisplayValue] = useState(0)
    const [isVisible, setIsVisible] = useState(false)

    // Animate counter
    useEffect(() => {
        const timer = setTimeout(() => setIsVisible(true), delay)
        return () => clearTimeout(timer)
    }, [delay])

    useEffect(() => {
        if (!isVisible) return

        const numericValue = typeof value === 'number' ? value : parseInt(value) || 0
        if (numericValue === 0) {
            setDisplayValue(0)
            return
        }

        const duration = 1200
        const steps = 40
        const increment = numericValue / steps
        let current = 0

        const timer = setInterval(() => {
            current += increment
            if (current >= numericValue) {
                setDisplayValue(numericValue)
                clearInterval(timer)
            } else {
                setDisplayValue(Math.floor(current))
            }
        }, duration / steps)

        return () => clearInterval(timer)
    }, [value, isVisible])

    const formattedValue = typeof value === 'string' && value.includes('%')
        ? value
        : displayValue.toLocaleString()

    return (
        <div
            className={`glass-card p-6 group hover-lift transition-all duration-300 ${isVisible ? 'animate-slide-up' : 'opacity-0'
                }`}
            style={{ animationDelay: `${delay}ms` }}
        >
            {/* Background Gradient */}
            <div className={`absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-[20px] ${color.includes('cyan') ? 'bg-gradient-to-br from-cyan-500/5 to-transparent' :
                    color.includes('red') ? 'bg-gradient-to-br from-red-500/5 to-transparent' :
                        color.includes('yellow') ? 'bg-gradient-to-br from-yellow-500/5 to-transparent' :
                            'bg-gradient-to-br from-purple-500/5 to-transparent'
                }`}></div>

            <div className="relative flex items-start justify-between gap-4 px-1">
                {/* Icon */}
                <div className={`p-3 rounded-xl ${color.includes('cyan') ? 'bg-cyan-500/10 border border-cyan-500/20' :
                        color.includes('red') ? 'bg-red-500/10 border border-red-500/20' :
                            color.includes('yellow') ? 'bg-yellow-500/10 border border-yellow-500/20' :
                                'bg-purple-500/10 border border-purple-500/20'
                    } group-hover:scale-110 transition-transform duration-300`}>
                    <span className={`${color} group-hover:drop-shadow-[0_0_8px_currentColor] transition-all`}>
                        {icon}
                    </span>
                </div>

                {/* Trend Indicator */}
                {trend !== null && (
                    <div className={`flex items-center gap-1 px-2.5 py-1.5 rounded-full text-xs font-medium ${trend > 0
                            ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                            : 'bg-red-500/10 text-red-400 border border-red-500/20'
                        }`}>
                        {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
                    </div>
                )}
            </div>

            {/* Value */}
            <div className="relative mt-4 px-1">
                <p className={`text-4xl font-bold ${color} font-mono tracking-tight`}>
                    {formattedValue}
                </p>

                {/* Underline Gradient */}
                <div className={`h-1 w-16 rounded-full mt-3 transition-all duration-500 group-hover:w-full ${color.includes('cyan') ? 'bg-gradient-to-r from-cyan-500 to-transparent' :
                        color.includes('red') ? 'bg-gradient-to-r from-red-500 to-transparent' :
                            color.includes('yellow') ? 'bg-gradient-to-r from-yellow-500 to-transparent' :
                                'bg-gradient-to-r from-purple-500 to-transparent'
                    }`}></div>
            </div>

            {/* Title */}
            <p className="text-sm font-medium text-slate-500 mt-3 uppercase tracking-wider px-1">
                {title}
            </p>
        </div>
    )
}
