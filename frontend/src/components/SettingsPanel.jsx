import { Settings, X, RotateCcw, Bell, Volume2, Monitor, Sliders } from 'lucide-react'
import { useState } from 'react'
import { useSettings } from '../context/SettingsContext'
import { useTheme } from '../context/ThemeContext'

export default function SettingsPanel() {
    const [isOpen, setIsOpen] = useState(false)
    const { settings, updateSetting, resetSettings } = useSettings()
    const { theme, toggleTheme } = useTheme()

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="btn btn-ghost p-2"
                title="Ayarlar"
            >
                <Settings className="w-5 h-5" />
            </button>
        )
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="glass-card w-full max-w-md p-6 m-4 animate-fade-in">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                        <Settings className="w-5 h-5 text-cyan-400" />
                        Ayarlar
                    </h2>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
                    >
                        <X className="w-5 h-5 text-slate-400" />
                    </button>
                </div>

                <div className="space-y-6">
                    {/* Theme */}
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Monitor className="w-5 h-5 text-slate-400" />
                            <div>
                                <p className="text-sm font-medium text-slate-200">Tema</p>
                                <p className="text-xs text-slate-500">Arayüz temasını değiştir</p>
                            </div>
                        </div>
                        <button
                            onClick={toggleTheme}
                            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${theme === 'dark'
                                    ? 'bg-slate-700 text-slate-300'
                                    : 'bg-yellow-500/20 text-yellow-400'
                                }`}
                        >
                            {theme === 'dark' ? '🌙 Koyu' : '☀️ Açık'}
                        </button>
                    </div>

                    {/* Anomaly Sensitivity */}
                    <div>
                        <div className="flex items-center gap-3 mb-2">
                            <Sliders className="w-5 h-5 text-slate-400" />
                            <div>
                                <p className="text-sm font-medium text-slate-200">Anomali Hassasiyeti</p>
                                <p className="text-xs text-slate-500">
                                    Yüksek = Daha fazla tehdit tespit eder ({(settings.anomalySensitivity * 100).toFixed(0)}%)
                                </p>
                            </div>
                        </div>
                        <input
                            type="range"
                            min="1"
                            max="20"
                            value={settings.anomalySensitivity * 100}
                            onChange={(e) => updateSetting('anomalySensitivity', parseInt(e.target.value) / 100)}
                            className="w-full accent-cyan-500"
                        />
                        <div className="flex justify-between text-xs text-slate-500 mt-1">
                            <span>Düşük</span>
                            <span>Yüksek</span>
                        </div>
                    </div>

                    {/* Notifications */}
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Bell className="w-5 h-5 text-slate-400" />
                            <div>
                                <p className="text-sm font-medium text-slate-200">Bildirimler</p>
                                <p className="text-xs text-slate-500">Tehdit bildirimleri al</p>
                            </div>
                        </div>
                        <button
                            onClick={() => updateSetting('notificationsEnabled', !settings.notificationsEnabled)}
                            className={`w-12 h-6 rounded-full transition-colors relative ${settings.notificationsEnabled ? 'bg-cyan-500' : 'bg-slate-600'
                                }`}
                        >
                            <span className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${settings.notificationsEnabled ? 'left-7' : 'left-1'
                                }`}></span>
                        </button>
                    </div>

                    {/* Sound */}
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Volume2 className="w-5 h-5 text-slate-400" />
                            <div>
                                <p className="text-sm font-medium text-slate-200">Ses Efektleri</p>
                                <p className="text-xs text-slate-500">Anomali tespit sesini aç</p>
                            </div>
                        </div>
                        <button
                            onClick={() => updateSetting('soundEnabled', !settings.soundEnabled)}
                            className={`w-12 h-6 rounded-full transition-colors relative ${settings.soundEnabled ? 'bg-cyan-500' : 'bg-slate-600'
                                }`}
                        >
                            <span className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${settings.soundEnabled ? 'left-7' : 'left-1'
                                }`}></span>
                        </button>
                    </div>

                    {/* Default Interface */}
                    <div>
                        <div className="flex items-center gap-3 mb-2">
                            <Monitor className="w-5 h-5 text-slate-400" />
                            <div>
                                <p className="text-sm font-medium text-slate-200">Varsayılan Arayüz</p>
                                <p className="text-xs text-slate-500">Ağ arayüzü adı</p>
                            </div>
                        </div>
                        <input
                            type="text"
                            value={settings.defaultInterface}
                            onChange={(e) => updateSetting('defaultInterface', e.target.value)}
                            className="input text-sm"
                            placeholder="Wi-Fi, Ethernet..."
                        />
                    </div>
                </div>

                {/* Footer */}
                <div className="mt-6 pt-4 border-t border-slate-700 flex justify-between">
                    <button
                        onClick={resetSettings}
                        className="btn btn-ghost text-sm flex items-center gap-2"
                    >
                        <RotateCcw className="w-4 h-4" />
                        Sıfırla
                    </button>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="btn btn-primary text-sm"
                    >
                        Kaydet
                    </button>
                </div>
            </div>
        </div>
    )
}
