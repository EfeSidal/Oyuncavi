import { AlertTriangle, ExternalLink, Copy, Check, ChevronDown, ChevronUp, Shield } from 'lucide-react'
import { useState } from 'react'

export default function ThreatTable({ threats = [] }) {
    const [expandedRow, setExpandedRow] = useState(null)
    const [copiedIp, setCopiedIp] = useState(null)

    const copyToClipboard = (ip) => {
        navigator.clipboard.writeText(ip)
        setCopiedIp(ip)
        setTimeout(() => setCopiedIp(null), 2000)
    }

    const getSeverity = (length) => {
        if (length > 1500) return { level: 'Kritik', color: 'text-red-400', bg: 'bg-red-500', glow: 'shadow-red-500/30' }
        if (length > 1000) return { level: 'Yüksek', color: 'text-orange-400', bg: 'bg-orange-500', glow: 'shadow-orange-500/30' }
        return { level: 'Orta', color: 'text-yellow-400', bg: 'bg-yellow-500', glow: 'shadow-yellow-500/30' }
    }

    if (threats.length === 0) {
        return (
            <div className="glass-card h-full flex flex-col">
                <div className="p-4 border-b border-slate-700/30">
                    <div className="flex items-center gap-2.5">
                        <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex-shrink-0">
                            <Shield className="w-4 h-4 text-cyan-400" />
                        </div>
                        <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                            Tespit Edilen Tehditler
                        </span>
                    </div>
                </div>
                <div className="flex-1 flex items-center justify-center p-6">
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                        <div style={{ width: '64px', height: '64px', marginBottom: '16px', borderRadius: '16px', background: 'linear-gradient(to bottom right, rgba(16,185,129,0.1), rgba(6,182,212,0.1))', border: '1px solid rgba(16,185,129,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Check className="w-8 h-8 text-green-400" />
                        </div>
                        <p className="text-green-400 font-semibold">Ağ Temiz</p>
                        <p className="text-xs text-slate-500 mt-1">Herhangi bir tehdit tespit edilmedi</p>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="glass-card h-full flex flex-col overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b border-slate-700/30 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                    <div className="p-2 rounded-xl bg-red-500/10 border border-red-500/20 flex-shrink-0">
                        <AlertTriangle className="w-4 h-4 text-red-400" />
                    </div>
                    <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                        Tespit Edilen Tehditler
                    </span>
                </div>
                <span className="px-2.5 py-1 bg-red-500/15 text-red-400 text-xs font-bold rounded-full border border-red-500/30 tabular-nums">
                    {threats.length} Tehdit
                </span>
            </div>

            {/* Table */}
            <div className="flex-1 overflow-y-auto">
                <div className="divide-y divide-slate-700/20">
                    {threats.slice(0, 50).map((threat, idx) => {
                        const severity = getSeverity(threat.length)
                        const isExpanded = expandedRow === idx

                        return (
                            <div
                                key={idx}
                                className={`transition-all duration-200 ${isExpanded ? 'bg-slate-800/50' : 'hover:bg-slate-800/30'
                                    }`}
                            >
                                {/* Main Row */}
                                <div
                                    className="flex items-center gap-3 p-3 cursor-pointer"
                                    onClick={() => setExpandedRow(isExpanded ? null : idx)}
                                >
                                    {/* Severity Indicator */}
                                    <div className={`relative w-2 h-8 rounded-full ${severity.bg} ${severity.glow} shadow-lg flex-shrink-0`}>
                                        <div className={`absolute inset-0 ${severity.bg} rounded-full animate-pulse opacity-50`}></div>
                                    </div>

                                    {/* IP Address */}
                                    <div className="flex-1 min-w-0">
                                        <p className="font-mono text-sm text-slate-200 truncate">
                                            {threat.src_ip}
                                        </p>
                                        <div className="flex items-center gap-2 mt-0.5">
                                            <span className={`text-xs ${severity.color} font-medium`}>
                                                {severity.level}
                                            </span>
                                            <span className="text-slate-600">•</span>
                                            <span className="text-xs text-slate-500 tabular-nums">
                                                {threat.length} B
                                            </span>
                                        </div>
                                    </div>

                                    {/* Actions */}
                                    <div className="flex items-center gap-1 flex-shrink-0">
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                copyToClipboard(threat.src_ip)
                                            }}
                                            className="p-1.5 hover:bg-slate-700/50 rounded-lg transition-colors"
                                            title="IP adresini kopyala"
                                        >
                                            {copiedIp === threat.src_ip ? (
                                                <Check className="w-3.5 h-3.5 text-green-400" />
                                            ) : (
                                                <Copy className="w-3.5 h-3.5 text-slate-500" />
                                            )}
                                        </button>

                                        {isExpanded ? (
                                            <ChevronUp className="w-4 h-4 text-slate-500" />
                                        ) : (
                                            <ChevronDown className="w-4 h-4 text-slate-500" />
                                        )}
                                    </div>
                                </div>

                                {/* Expanded Details */}
                                {isExpanded && (
                                    <div className="px-4 pb-4 pt-1 animate-fade-in">
                                        <div className="bg-slate-900/50 rounded-xl p-3 space-y-2 border border-slate-700/30">
                                            <div className="grid grid-cols-2 gap-2 text-xs">
                                                <div>
                                                    <span className="text-slate-500">Hedef IP:</span>
                                                    <span className="ml-2 font-mono text-slate-300">{threat.dst_ip}</span>
                                                </div>
                                                <div>
                                                    <span className="text-slate-500">Port:</span>
                                                    <span className="ml-2 font-mono text-slate-300 tabular-nums">{threat.dst_port}</span>
                                                </div>
                                                <div>
                                                    <span className="text-slate-500">Protokol:</span>
                                                    <span className="ml-2 text-slate-300">{threat.protocol === 6 ? 'TCP' : 'UDP'}</span>
                                                </div>
                                                <div>
                                                    <span className="text-slate-500">Boyut:</span>
                                                    <span className="ml-2 text-slate-300 tabular-nums">{threat.length} bytes</span>
                                                </div>
                                            </div>

                                            {/* External Lookup */}
                                            <a
                                                href={`https://www.abuseipdb.com/check/${threat.src_ip}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="flex items-center gap-2 text-xs text-cyan-400 hover:text-cyan-300 mt-2 group"
                                            >
                                                <ExternalLink className="w-3.5 h-3.5" />
                                                <span>AbuseIPDB'de Kontrol Et</span>
                                                <span className="opacity-0 group-hover:opacity-100 transition-opacity">→</span>
                                            </a>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}
