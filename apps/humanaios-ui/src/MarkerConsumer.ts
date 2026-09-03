/**
 * SSE Marker Consumer — Cortex Event Stream
 *
 * Connects to backend /api/v1/sonify/markers/stream (Server-Sent Events)
 * Consumes acoustic marker events (proposal, SER, CHECK gate, POSTFLIGHT)
 * Queues events async, fires haptic + audio playback
 *
 * Markers: 9 types → 9 frequencies (523-1174 Hz), severity levels (info/warning/urgent)
 * Latency target: <200ms event → visual marker rendered
 * Bandwidth: ~5 events/minute peak (transitions + proposals)
 */

export interface MarkerEventData {
  marker_type: string
  source_id: string
  timestamp: string
  frequency_hz: number
  severity: 'info' | 'warning' | 'urgent'
  icon: string
  description: string
  metadata: Record<string, unknown>
}

export class MarkerConsumer {
  private eventSource: EventSource | null = null
  private queue: MarkerEventData[] = []
  private listeners: Array<(event: MarkerEventData) => void> = []
  private connected = false
  private reconnectInterval = 3000
  private maxReconnectAttempts = 5
  private reconnectAttempts = 0

  constructor(
    private apiBaseUrl: string = '/api/v1',
    private autoStart = true
  ) {
    if (autoStart) {
      this.connect()
    }
  }

  /**
   * Connect to SSE stream
   */
  connect(): void {
    if (this.connected || this.eventSource) {
      console.warn('[MarkerConsumer] Already connected')
      return
    }

    const url = `${this.apiBaseUrl}/sonify/markers/stream`
    console.log(`[MarkerConsumer] Connecting to ${url}`)

    this.eventSource = new EventSource(url)

    this.eventSource.addEventListener('message', (event) => {
      try {
        const data = JSON.parse(event.data) as MarkerEventData
        this.handleMarkerEvent(data)
      } catch (e) {
        console.error('[MarkerConsumer] Failed to parse event', e, event.data)
      }
    })

    this.eventSource.addEventListener('error', () => {
      this.handleError()
    })

    this.eventSource.onopen = () => {
      console.log('[MarkerConsumer] Connected')
      this.connected = true
      this.reconnectAttempts = 0
    }
  }

  /**
   * Disconnect from stream
   */
  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
    this.connected = false
    console.log('[MarkerConsumer] Disconnected')
  }

  /**
   * Handle marker event
   */
  private handleMarkerEvent(event: MarkerEventData): void {
    // Add to queue
    this.queue.push(event)

    // Fire listeners immediately (non-blocking)
    this.listeners.forEach((listener) => {
      try {
        listener(event)
      } catch (e) {
        console.error('[MarkerConsumer] Listener error', e)
      }
    })

    // Emit haptic feedback for urgent markers
    if (event.severity === 'urgent') {
      this.emitHaptic(event)
    }

    // Emit audio playback (Web Audio API)
    this.playAudioMarker(event)
  }

  /**
   * Emit haptic feedback (W3C Vibration API)
   */
  private emitHaptic(event: MarkerEventData): void {
    if (!navigator.vibrate) {
      console.debug(
        '[MarkerConsumer] Haptic feedback not available on this device'
      )
      return
    }

    // Vibration pattern: urgent = double pulse
    const pattern =
      event.severity === 'urgent'
        ? [50, 100, 50] // double tap
        : event.severity === 'warning'
          ? [30, 80]
          : [20]

    navigator.vibrate(pattern)
  }

  /**
   * Play audio marker via Web Audio API (simple sine wave)
   */
  private playAudioMarker(event: MarkerEventData): void {
    try {
      const audioContext = new (window.AudioContext ||
        (window as any).webkitAudioContext)()

      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(audioContext.destination)

      oscillator.frequency.value = event.frequency_hz
      oscillator.type = 'sine'

      // Envelope: quick attack, exponential decay
      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5)

      oscillator.start(audioContext.currentTime)
      oscillator.stop(audioContext.currentTime + 0.5)
    } catch (e) {
      console.error('[MarkerConsumer] Audio playback failed', e)
    }
  }

  /**
   * Handle connection error (auto-reconnect with backoff)
   */
  private handleError(): void {
    console.warn('[MarkerConsumer] Connection error')
    this.connected = false

    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1)
      console.log(
        `[MarkerConsumer] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`
      )
      setTimeout(() => this.connect(), delay)
    } else {
      console.error('[MarkerConsumer] Max reconnection attempts reached')
    }
  }

  /**
   * Subscribe to marker events
   */
  on(listener: (event: MarkerEventData) => void): () => void {
    this.listeners.push(listener)
    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener)
    }
  }

  /**
   * Get queue size
   */
  getQueueSize(): number {
    return this.queue.length
  }

  /**
   * Clear queue
   */
  clearQueue(): void {
    this.queue = []
  }

  /**
   * Get connection status
   */
  isConnected(): boolean {
    return this.connected
  }
}
