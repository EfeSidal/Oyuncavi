import { Bell, X, AlertTriangle, Info, CheckCircle } from 'lucide-react'
import { useState } from 'react'
import { useAlerts } from '../context/AlertContext'

export default function AlertPanel() {
    const [isOpen, setIsOpen] = useState(false)
    const { alerts, unreadCount, markAsRead, clearAlerts } = useAlerts()

    const getAlertIcon = (type) => {
        switch (type) {
            case 'threat': return <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0" />
            case 'success': return <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />
            default: return <Info className="w-4 h-4 text-cyan-400 flex-shrink-0" />
        }
    }

    const getAlertColor = (type) => {
        switch (type) {
            case 'threat': return 'border-l-red-500 bg-red-500/5'
            case 'success': return 'border-l-green-500 bg-green-500/5'
            default: return 'border-l-cyan-500 bg-cyan-500/5'
        }
    }

    const formatTime = (date) => {
        const now = new Date()
        const diff = now - date
        const minutes = Math.floor(diff / 60000)
        const hours = Math.floor(diff / 3600000)

        if (minutes < 1) return 'Şimdi'
        if (minutes < 60) return `${minutes} dk önce`
        if (hours < 24) return `${hours} sa önce`
        return date.toLocaleDateString('tr-TR')
    }

    return (
        <div className="relative" style={{ position: 'relative' }}>
            {/* Bell Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="relative p-2 hover:bg-slate-700 rounded-lg transition-colors"
                style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            >
                <Bell className="w-5 h-5 text-slate-400" />
                {unreadCount > 0 && (
                    <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs font-bold text-white flex items-center justify-center animate-pulse">
                        {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                )}
            </button>

            {/* Dropdown */}
            {isOpen && (
                <div
                    className="absolute right-0 mt-2 w-80 glass-card border border-slate-700 rounded-xl overflow-hidden shadow-2xl"
                    style={{
                        position: 'absolute',
                        top: '100%',
                        right: 0,
                        zIndex: 9999
                    }}
                >
                    {/* Backdrop - clicks outside close the panel */}
                    <div
                        className="fixed inset-0"
                        style={{ zIndex: -1 }}
                        onClick={() => setIsOpen(false)}
                    ></div>

                    {/* Header */}
                    <div className="flex items-center justify-between p-3 border-b border-slate-700 bg-slate-800/50">
                        <h3 className="text-sm font-semibold text-slate-200">
                            Bildirimler {unreadCount > 0 && `(${unreadCount})`}
                        </h3>
                        {alerts.length > 0 && (
                            <button
                                onClick={clearAlerts}
                                className="p-1.5 hover:bg-slate-700 rounded text-xs text-slate-400"
                                title="Tümünü temizle"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        )}
                    </div>

                    {/* Alerts List */}
                    <div className="max-h-80 overflow-y-auto">
                        {alerts.length === 0 ? (
                            <div className="p-6 text-center text-slate-500">
                                <Bell className="w-8 h-8 mx-auto mb-2 opacity-30" />
                                <p className="text-sm">Henüz bildirim yok</p>
                            </div>
                        ) : (
                            alerts.map(alert => (
                                <div
                                    key={alert.id}
                                    className={`p-3 border-l-2 ${getAlertColor(alert.type)} ${!alert.read ? 'bg-slate-800/50' : ''
                                        } hover:bg-slate-700/30 transition-colors cursor-pointer`}
                                    onClick={() => markAsRead(alert.id)}
                                >
                                    <div className="flex items-start gap-3">
                                        {getAlertIcon(alert.type)}
                                        <div className="flex-1 min-w-0">
                                            <p className="text-sm text-slate-200 line-clamp-2">
                                                {alert.message}
                                            </p>
                                            <p className="text-xs text-slate-500 mt-1">
                                                {formatTime(alert.timestamp)}
                                            </p>
                                        </div>
                                        {!alert.read && (
                                            <span className="w-2 h-2 bg-cyan-400 rounded-full flex-shrink-0 mt-1"></span>
                                        )}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}
