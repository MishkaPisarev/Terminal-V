/**
 * Type definitions matching Nexus Engine Pydantic models
 */

export interface MarketStreamData {
  symbol: string
  price: number
  volume: number
  change_24h: number
  timestamp: string
}

export interface MacroEconData {
  gdp_growth: number | null
  inflation_rate: number | null
  unemployment_rate: number | null
  interest_rate: number | null
  region: string
  timestamp: string
}

export interface NewsSentimentData {
  sentiment_score: number
  sentiment_label: string
  article_count: number
  keywords: string[]
  timestamp: string
}

export interface BlockchainData {
  network: string
  block_height: number
  transaction_count: number
  gas_price: number | null
  hash_rate: number | null
  timestamp: string
}

export interface UserActivityData {
  active_users: number
  transactions_24h: number
  total_volume_24h: number
  top_symbols: string[]
  timestamp: string
}

export interface AggregatedData {
  market_stream: MarketStreamData
  macro_econ: MacroEconData
  news_sentiment: NewsSentimentData
  blockchain: BlockchainData
  user_activity: UserActivityData
  aggregated_at: string
  version: string
}
