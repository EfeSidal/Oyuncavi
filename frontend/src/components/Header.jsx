import { Shield, Wifi, WifiOff, Zap } from 'lucide-react'
import AlertPanel from './AlertPanel'
import ThemeToggle from './ThemeToggle'
import SettingsPanel from './SettingsPanel'

export default function Header({ status, isConnected = true }) {
  const getStatusBadge = () => {
    switch (status) {
      case 'scanning':
        return (
          <span className="badge badge-warning">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-yellow-400"></span>
            </span>
            Taranıyor
          </span>
        )
      case 'completed':
        return (
          <span className="badge badge-success">
            <span className="w-2 h-2 bg-green-400 rounded-full"></span>
            Tamamlandı
          </span>
        )
      default:
        return (
          <span className="badge badge-primary">
            <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></span>
            Hazır
          </span>
        )
    }
  }

  return (
    <header className="flex items-center justify-between pb-4 border-b border-slate-700/30">
      {/* Logo & Title */}
      <div className="flex items-center gap-5">
        {/* Animated Logo Container */}
        <div className="relative group">
          {/* Outer Glow */}
          <div className="absolute -inset-2 bg-gradient-to-r from-cyan-500 via-purple-500 to-cyan-500 rounded-2xl opacity-20 blur-xl group-hover:opacity-40 transition-all duration-500 animate-pulse"></div>

          {/* Logo Box */}
          <div className="relative p-3.5 bg-gradient-to-br from-cyan-500/10 via-purple-500/10 to-blue-600/10 rounded-2xl border border-cyan-500/20 backdrop-blur-sm">
            <Shield className="w-9 h-9 text-cyan-400 drop-shadow-[0_0_12px_rgba(6,182,212,0.5)]" />

            {/* Scanning Animation */}
            {status === 'scanning' && (
              <div className="absolute inset-0 rounded-2xl overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-cyan-400/20 to-transparent animate-scan"></div>
              </div>
            )}
          </div>
        </div>

        <div>
          <h1 className="text-2xl font-bold text-gradient flex items-center gap-2">
            OyuncuAvi
            <Zap className="w-5 h-5 text-yellow-400 animate-pulse" />
          </h1>
          <p className="text-sm text-slate-500 font-medium tracking-wide">
            AI-Powered Network Threat Analysis
          </p>
        </div>
      </div>

      {/* Right Side - Actions & Status */}
      <div className="flex items-center gap-2">
        {/* Theme Toggle */}
        <ThemeToggle />

        {/* Alerts */}
        <AlertPanel />

        {/* Settings */}
        <SettingsPanel />

        {/* Divider */}
        <div className="w-px h-8 bg-gradient-to-b from-transparent via-slate-600 to-transparent mx-2"></div>

        {/* Connection Status */}
        <div className={`flex items-center gap-2 px-3 py-2 rounded-xl transition-all ${isConnected
            ? 'bg-green-500/10 border border-green-500/20'
            : 'bg-red-500/10 border border-red-500/20'
          }`}>
          {isConnected ? (
            <>
              <div className="relative">
                <Wifi className="w-4 h-4 text-green-400" />
                <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              </div>
              <span className="text-xs font-medium text-green-400">Connected</span>
            </>
          ) : (
            <>
              <WifiOff className="w-4 h-4 text-red-400" />
              <span className="text-xs font-medium text-red-400">Offline</span>
            </>
          )}
        </div>

        {/* Divider */}
        <div className="w-px h-8 bg-gradient-to-b from-transparent via-slate-600 to-transparent mx-2"></div>

        {/* Status Badge */}
        {getStatusBadge()}
      </div>

      <style>{`
        @keyframes scan {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(100%); }
        }
        .animate-scan {
          animation: scan 1.5s ease-in-out infinite;
        }
      `}</style>
    </header>
  )
}
