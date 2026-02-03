/**
 * Mock data generator for demo mode when backend is not configured
 */
import type { AggregatedData } from '../types/nexus'

/**
 * Generate mock aggregated data for demonstration
 * Updates values slightly on each call to simulate real-time updates
 */
export function generateMockData(): AggregatedData {
  const now = new Date().toISOString()
  
  // Generate slightly varying values for realism
  const basePrice = 45000 + Math.random() * 2000 - 1000 // BTC price around $45k
  const baseChange = (Math.random() - 0.5) * 4 // -2% to +2%
  
  return {
    market_stream: {
      symbol: 'BTC-USD',
      price: basePrice,
      volume: 1234567.89 + Math.random() * 100000,
      change_24h: baseChange,
      timestamp: now,
    },
    macro_econ: {
      gdp_growth: 2.1 + (Math.random() - 0.5) * 0.2,
      inflation_rate: 3.2 + (Math.random() - 0.5) * 0.3,
      unemployment_rate: 3.7 + (Math.random() - 0.5) * 0.2,
      interest_rate: 5.25 + (Math.random() - 0.5) * 0.1,
      region: 'US',
      timestamp: now,
    },
    news_sentiment: {
      sentiment_score: (Math.random() - 0.5) * 0.6, // -0.3 to +0.3
      sentiment_label: Math.random() > 0.5 ? 'positive' : Math.random() > 0.5 ? 'negative' : 'neutral',
      article_count: 15 + Math.floor(Math.random() * 10),
      keywords: ['bitcoin', 'market', 'trading', 'crypto', 'finance'].slice(0, 3 + Math.floor(Math.random() * 3)),
      timestamp: now,
    },
    blockchain: {
      network: 'ethereum',
      block_height: 18500000 + Math.floor(Math.random() * 100),
      transaction_count: 1200000 + Math.floor(Math.random() * 50000),
      gas_price: 20 + Math.random() * 10,
      hash_rate: 350 + Math.random() * 50,
      timestamp: now,
    },
    user_activity: {
      active_users: 1250 + Math.floor(Math.random() * 200),
      transactions_24h: 8500 + Math.floor(Math.random() * 1000),
      total_volume_24h: 125000000 + Math.random() * 10000000,
      top_symbols: ['BTC-USD', 'ETH-USD', 'SPY', 'TSLA', 'AAPL'].slice(0, 3 + Math.floor(Math.random() * 2)),
      timestamp: now,
    },
    aggregated_at: now,
    version: '1.0.0-demo',
  }
}
