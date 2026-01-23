import { createContext, useContext, useState, useCallback } from 'react'

const AlertContext = createContext()

export function AlertProvider({ children }) {
    const [alerts, setAlerts] = useState([])

    const addAlert = useCallback((alert) => {
        const id = Date.now()
        const newAlert = {
            id,
            timestamp: new Date(),
            read: false,
            ...alert
        }

        setAlerts(prev => [newAlert, ...prev].slice(0, 50)) // Keep last 50 alerts

        // Browser notification
        if (Notification.permission === 'granted' && alert.type === 'threat') {
            new Notification('OyuncuAvi - Tehdit Tespit Edildi!', {
                body: alert.message,
                icon: '/shield.png',
                tag: `alert-${id}`
            })
        }

        // Sound effect
        if (alert.playSound) {
            const audio = new Audio('/alert.mp3')
            audio.volume = 0.3
            audio.play().catch(() => { }) // Ignore if autoplay blocked
        }

        return id
    }, [])

    const markAsRead = useCallback((id) => {
        setAlerts(prev =>
            prev.map(a => a.id === id ? { ...a, read: true } : a)
        )
    }, [])

    const clearAlerts = useCallback(() => {
        setAlerts([])
    }, [])

    const requestNotificationPermission = useCallback(async () => {
        if ('Notification' in window) {
            const permission = await Notification.requestPermission()
            return permission === 'granted'
        }
        return false
    }, [])

    const unreadCount = alerts.filter(a => !a.read).length

    return (
        <AlertContext.Provider value={{
            alerts,
            addAlert,
            markAsRead,
            clearAlerts,
            unreadCount,
            requestNotificationPermission
        }}>
            {children}
        </AlertContext.Provider>
    )
}

export function useAlerts() {
    const context = useContext(AlertContext)
    if (!context) {
        throw new Error('useAlerts must be used within an AlertProvider')
    }
    return context
}
