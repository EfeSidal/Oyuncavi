import { createContext, useContext, useState, useEffect } from 'react'

const SettingsContext = createContext()

const defaultSettings = {
    anomalySensitivity: 0.05, // 5% contamination rate
    autoRefresh: true,
    refreshInterval: 2000,
    defaultInterface: 'Wi-Fi',
    soundEnabled: true,
    notificationsEnabled: true,
}

export function SettingsProvider({ children }) {
    const [settings, setSettings] = useState(() => {
        const saved = localStorage.getItem('oyuncuavi-settings')
        return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings
    })

    useEffect(() => {
        localStorage.setItem('oyuncuavi-settings', JSON.stringify(settings))
    }, [settings])

    const updateSetting = (key, value) => {
        setSettings(prev => ({ ...prev, [key]: value }))
    }

    const resetSettings = () => {
        setSettings(defaultSettings)
    }

    return (
        <SettingsContext.Provider value={{ settings, updateSetting, resetSettings }}>
            {children}
        </SettingsContext.Provider>
    )
}

export function useSettings() {
    const context = useContext(SettingsContext)
    if (!context) {
        throw new Error('useSettings must be used within a SettingsProvider')
    }
    return context
}
