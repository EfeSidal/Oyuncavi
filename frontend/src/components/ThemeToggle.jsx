import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'

export default function ThemeToggle() {
    const { theme, toggleTheme } = useTheme()

    return (
        <button
            onClick={toggleTheme}
            className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
            title={theme === 'dark' ? 'Açık Tema' : 'Koyu Tema'}
        >
            {theme === 'dark' ? (
                <Sun className="w-5 h-5 text-yellow-400" />
            ) : (
                <Moon className="w-5 h-5 text-slate-400" />
            )}
        </button>
    )
}
