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
 * Custom hook for fetching aggregated data from Core API
 * Handles high-frequency updates (10 updates/sec = 200ms) with optimized state management
 */
export function useNexusStream(
  options: UseNexusStreamOptions = {}
): UseNexusStreamReturn {
  // Use environment variable for API URL, fallback to localhost for development
  const envApiUrl = import.meta.env.VITE_API_URL
  const defaultApiUrl = envApiUrl && envApiUrl.trim() !== '' 
    ? envApiUrl 
    : (import.meta.env.DEV ? 'http://localhost:8000' : 'https://terminal-v-api.onrender.com')
  
  const {
    apiUrl = defaultApiUrl,
    reconnectInterval = 3000,
    maxReconnectAttempts = 10,
  } = options

  const [data, setData] = useState<AggregatedData | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const reconnectAttemptsRef = useRef(0)
  const fetchIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const isMountedRef = useRef(true)

  // Fetch data from REST API
  const fetchData = useCallback(async () => {
    if (!apiUrl || !isMountedRef.current) return
    
    try {
      const response = await fetch(`${apiUrl}/api/aggregated?symbol=BTCUSD`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const aggregatedData = await response.json() as AggregatedData
      
      if (isMountedRef.current) {
        setData(aggregatedData)
        setIsConnected(true)
        setError(null)
        reconnectAttemptsRef.current = 0
      }
    } catch (err) {
      if (isMountedRef.current) {
        setError(err instanceof Error ? err : new Error('Failed to fetch data'))
        setIsConnected(false)
        
        // Attempt reconnection
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          reconnectAttemptsRef.current++
          reconnectTimeoutRef.current = setTimeout(() => {
            fetchData()
          }, reconnectInterval)
        }
      }
    }
  }, [apiUrl, reconnectInterval, maxReconnectAttempts])

  const connect = useCallback(() => {
    if (!isMountedRef.current) return

    if (!apiUrl || apiUrl.trim() === '') {
      setError(new Error('API URL not configured'))
      setIsConnected(false)
      return
    }
    
    // Clear any existing interval
    if (fetchIntervalRef.current) {
      clearInterval(fetchIntervalRef.current)
    }
    
    // Fetch immediately
    fetchData()
    
    // Set up polling every 200ms for real-time updates
    fetchIntervalRef.current = setInterval(() => {
      if (isMountedRef.current) {
        fetchData()
      }
    }, 200)
  }, [apiUrl, fetchData])

  const reconnect = useCallback(() => {
    if (fetchIntervalRef.current) {
      clearInterval(fetchIntervalRef.current)
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
      if (fetchIntervalRef.current) {
        clearInterval(fetchIntervalRef.current)
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
