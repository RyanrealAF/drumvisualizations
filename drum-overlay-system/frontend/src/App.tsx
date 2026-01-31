import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { useTauriIntegration } from './TauriIntegration'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const {
    isOverlayOpen,
    drumEvents,
    openOverlay,
    closeOverlay,
    triggerKickEffect,
    triggerSnareEffect,
    triggerHatsEffect
  } = useTauriIntegration()

  return (
    <>
      <div className="container">
        <div className="header">
          <div className="logos">
            <a href="https://vite.dev" target="_blank" rel="noopener noreferrer">
              <img src={viteLogo} className="logo" alt="Vite logo" />
            </a>
            <a href="https://react.dev" target="_blank" rel="noopener noreferrer">
              <img src={reactLogo} className="logo react" alt="React logo" />
            </a>
          </div>
          <h1>Drum Visualization System</h1>
        </div>

        <div className="controls">
          <div className="card">
            <h2>Overlay Controls</h2>
            <div className="button-group">
              <button 
                onClick={openOverlay} 
                disabled={isOverlayOpen}
                className="btn-primary"
              >
                {isOverlayOpen ? 'Overlay Open' : 'Open Overlay'}
              </button>
              <button 
                onClick={closeOverlay} 
                disabled={!isOverlayOpen}
                className="btn-secondary"
              >
                Close Overlay
              </button>
            </div>
          </div>

          <div className="card">
            <h2>Test Effects</h2>
            <div className="button-group">
              <button 
                onClick={() => triggerKickEffect(0.8)}
                className="btn-kick"
              >
                Test Kick (80%)
              </button>
              <button 
                onClick={() => triggerSnareEffect(0.6)}
                className="btn-snare"
              >
                Test Snare (60%)
              </button>
              <button 
                onClick={() => triggerHatsEffect(0.4)}
                className="btn-hats"
              >
                Test Hats (40%)
              </button>
            </div>
          </div>

          <div className="card">
            <h2>Development</h2>
            <div className="button-group">
              <button onClick={() => setCount((count) => count + 1)}>
                count is {count}
              </button>
              <p>
                Edit <code>src/App.tsx</code> and save to test HMR
              </p>
            </div>
          </div>
        </div>

        {drumEvents.length > 0 && (
          <div className="events">
            <h3>Recent Drum Events</h3>
            <div className="event-list">
              {drumEvents.slice(-10).map((event, index) => (
                <div key={index} className={`event-item event-${event.type}`}>
                  <span className="event-type">{event.type.toUpperCase()}</span>
                  <span className="event-velocity">Velocity: {(event.velocity * 100).toFixed(0)}%</span>
                  <span className="event-time">{new Date(event.timestamp).toLocaleTimeString()}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <p className="read-the-docs">
          Built with Tauri " React " Vite " Three.js
        </p>
      </div>
    </>
  )
}

export default App
