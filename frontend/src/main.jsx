import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { ThemeProvider } from './context/ThemeContext'
import { SettingsProvider } from './context/SettingsContext'
import { AlertProvider } from './context/AlertContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider>
      <SettingsProvider>
        <AlertProvider>
          <App />
        </AlertProvider>
      </SettingsProvider>
    </ThemeProvider>
  </StrictMode>,
)
