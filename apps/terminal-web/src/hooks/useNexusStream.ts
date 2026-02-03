import { useEffect, useRef, useState, useCallback } from 'react'
import type { AggregatedData } from '../types/nexus'

interface UseNexusStreamOptions {
  apiUrl?: string
  reconnectInterval?: number
  maxReconnectAttempts?: number
}

interface UseNexusStreamReturn {
  data: AggregatedData | null
  isConnected: boolean
  error: Error | null
  reconnect: () => void
}

/**
 * Custom hook for connecting to Nexus Engine Redis stream via WebSocket/SSE
 * Handles high-frequency updates (10 updates/sec = 200ms) with optimized state management
 */
export function useNexusStream(
  options: UseNexusStreamOptions = {}
): UseNexusStreamReturn {
  const {
    apiUrl = 'http://localhost:8000',
    reconnectInterval = 3000,
    maxReconnectAttempts = 10,
  } = options

  const [data, setData] = useState<AggregatedData | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const reconnectAttemptsRef = useRef(0)
  const isMountedRef = useRef(true)

  // Optimized data update - only update if data actually changed
  const handleMessage = useCallback((event: MessageEvent) => {
    try {
      const parsed = JSON.parse(event.data) as AggregatedData
      
      // Use functional update to avoid stale closures
      setData((prevData) => {
        // Only update if data actually changed (prevent unnecessary re-renders)
        if (prevData?.aggregated_at === parsed.aggregated_at) {
          return prevData
        }
        return parsed
      })
    } catch (err) {
      console.error('Failed to parse Nexus stream data:', err)
      setError(err instanceof Error ? err : new Error('Parse error'))
    }
  }, [])

  const connect = useCallback(() => {
    if (!isMountedRef.current) return

    try {
      // Try WebSocket first (preferred for real-time)
      const wsUrl = apiUrl.replace(/^http/, 'ws') + '/ws/nexus-stream'
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        if (!isMountedRef.current) {
          ws.close()
          return
        }
        setIsConnected(true)
        setError(null)
        reconnectAttemptsRef.current = 0
        console.log('✓ Connected to Nexus stream')
      }

      ws.onmessage = handleMessage

      ws.onerror = (event) => {
        console.error('WebSocket error:', event)
        setError(new Error('WebSocket connection error'))
        setIsConnected(false)
      }

      ws.onclose = () => {
        if (!isMountedRef.current) return
        
        setIsConnected(false)
        
        // Attempt reconnection
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          reconnectAttemptsRef.current++
          reconnectTimeoutRef.current = setTimeout(() => {
            connect()
          }, reconnectInterval)
        } else {
          setError(new Error('Max reconnection attempts reached'))
        }
      }

      wsRef.current = ws
    } catch (err) {
      console.error('Failed to create WebSocket:', err)
      setError(err instanceof Error ? err : new Error('Connection failed'))
      setIsConnected(false)

      // Fallback: Try SSE if WebSocket fails
      // Note: SSE implementation would go here if needed
    }
  }, [apiUrl, reconnectInterval, maxReconnectAttempts, handleMessage])

  const reconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
    }
    reconnectAttemptsRef.current = 0
    connect()
  }, [connect])

  useEffect(() => {
    isMountedRef.current = true
    connect()

    return () => {
      isMountedRef.current = false
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [connect])

  return {
    data,
    isConnected,
    error,
    reconnect,
  }
}
