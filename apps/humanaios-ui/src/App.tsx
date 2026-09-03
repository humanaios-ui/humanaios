import React, { useState, useEffect } from 'react'
import { WaveformRenderer, MarkerEvent } from './WaveformRenderer'
import { MarkerConsumer, MarkerEventData } from './MarkerConsumer'
import './App.css'

export const App: React.FC = () => {
  const [consumer, setConsumer] = useState<MarkerConsumer | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [queueSize, setQueueSize] = useState(0)
  const [markers, setMarkers] = useState<MarkerEvent[]>([])
  const [lastEvent, setLastEvent] = useState<MarkerEventData | null>(null)

  useEffect(() => {
    const markerConsumer = new MarkerConsumer(
      process.env.REACT_APP_API_URL || '/api/v1'
    )

    // Listen for connection status
    const checkStatus = setInterval(() => {
      setIsConnected(markerConsumer.isConnected())
      setQueueSize(markerConsumer.getQueueSize())
    }, 500)

    // Subscribe to marker events
    const unsubscribe = markerConsumer.on((event) => {
      setLastEvent(event)

      // Convert to MarkerEvent for waveform renderer
      const marker: MarkerEvent = {
        type: event.marker_type as MarkerEvent['type'],
        timestamp: Date.parse(event.timestamp),
        frequency: event.frequency_hz,
        severity: event.severity,
        icon: event.icon,
      }

      setMarkers((prev) => [
        ...prev,
        marker,
      ].slice(-100)) // Keep last 100 markers
    })

    setConsumer(markerConsumer)

    return () => {
      clearInterval(checkStatus)
      unsubscribe()
      markerConsumer.disconnect()
    }
  }, [])

  const handleMarkerClick = (marker: MarkerEvent) => {
    console.log('Marker clicked:', marker)
    // Future: show details panel
  }

  return (
    <div className="app">
      <header>
        <h1>HumanAIOS — Sonification Waveform</h1>
        <div className="status">
          <span className={`indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
          <span className="status-text">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
          <span className="queue-size">Queue: {queueSize}</span>
        </div>
      </header>

      <main>
        <section className="waveform-section">
          <h2>Epistemic State Visualization</h2>
          <div className="waveform-container">
            <WaveformRenderer
              width={1000}
              height={400}
              windowSeconds={30}
              onMarkerClick={handleMarkerClick}
            />
          </div>
          <div className="legend">
            <div className="legend-item">
              <span className="color" style={{ backgroundColor: '#4f46e5' }}></span>
              <span>Know (Certainty)</span>
            </div>
            <div className="legend-item">
              <span className="color" style={{ backgroundColor: '#06b6d4' }}></span>
              <span>Context (Information)</span>
            </div>
            <div className="legend-item">
              <span className="color" style={{ backgroundColor: '#f59e0b' }}></span>
              <span>Clarity (Confidence)</span>
            </div>
            <div className="legend-item">
              <span className="color" style={{ backgroundColor: '#ef4444' }}></span>
              <span>Uncertainty</span>
            </div>
          </div>
        </section>

        {lastEvent && (
          <section className="event-panel">
            <h3>Latest Marker Event</h3>
            <div className="event-details">
              <p><strong>Type:</strong> {lastEvent.marker_type}</p>
              <p><strong>Frequency:</strong> {lastEvent.frequency_hz} Hz</p>
              <p><strong>Severity:</strong> {lastEvent.severity}</p>
              <p><strong>Description:</strong> {lastEvent.description}</p>
              <p><strong>Timestamp:</strong> {lastEvent.timestamp}</p>
            </div>
          </section>
        )}
      </main>

      <footer>
        <p>Phase 1b UI Implementation • Sep 11, 2026 Deadline</p>
      </footer>
    </div>
  )
}
