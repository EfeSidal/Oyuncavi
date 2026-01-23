import { Download, FileJson, FileSpreadsheet } from 'lucide-react'

export default function ExportPanel({ data = [], anomalies = [] }) {
    const exportJSON = () => {
        const exportData = {
            timestamp: new Date().toISOString(),
            totalPackets: data.length,
            anomalyCount: anomalies.length,
            packets: data.map(p => ({
                src_ip: p.src_ip,
                dst_ip: p.dst_ip,
                src_port: p.src_port,
                dst_port: p.dst_port,
                protocol: p.protocol === 6 ? 'TCP' : 'UDP',
                length: p.length,
                isAnomaly: p.anomaly === -1
            }))
        }

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `oyuncuavi_export_${Date.now()}.json`
        a.click()
        URL.revokeObjectURL(url)
    }

    const exportCSV = () => {
        const headers = ['src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'length', 'is_anomaly']
        const rows = data.map(p => [
            p.src_ip,
            p.dst_ip,
            p.src_port,
            p.dst_port,
            p.protocol === 6 ? 'TCP' : 'UDP',
            p.length,
            p.anomaly === -1 ? 'YES' : 'NO'
        ])

        const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
        const blob = new Blob([csv], { type: 'text/csv' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `oyuncuavi_export_${Date.now()}.csv`
        a.click()
        URL.revokeObjectURL(url)
    }

    return (
        <div className="glass-card p-4">
            {/* Header */}
            <div className="flex items-center gap-2.5 mb-3">
                <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20 flex-shrink-0">
                    <Download className="w-4 h-4 text-purple-400" />
                </div>
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Dışa Aktar
                </span>
            </div>

            {/* Export Buttons */}
            <div className="grid grid-cols-2 gap-2">
                <button
                    onClick={exportJSON}
                    disabled={data.length === 0}
                    className="btn btn-ghost text-xs py-2.5 flex items-center justify-center gap-1.5"
                >
                    <FileJson className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                    <span>JSON</span>
                </button>
                <button
                    onClick={exportCSV}
                    disabled={data.length === 0}
                    className="btn btn-ghost text-xs py-2.5 flex items-center justify-center gap-1.5"
                >
                    <FileSpreadsheet className="w-4 h-4 text-green-400 flex-shrink-0" />
                    <span>CSV</span>
                </button>
            </div>
        </div>
    )
}
