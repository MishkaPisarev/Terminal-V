# Nexus Engine

Data processing and computation engine for Terminal-V financial platform.

## Architecture

This service handles data processing, calculations, and business logic computations. It communicates with Core API to provide processed data.

## Data Sources

The Nexus Engine aggregates data from 5 distinct sources:

1. **Market Stream** - WebSocket-based real-time market data
2. **Macro Econ** - REST API for macroeconomic indicators
3. **News Sentiment** - AI-powered sentiment analysis
4. **Blockchain Scanner** - RPC-based blockchain metrics
5. **User Activity** - Internal database user metrics

## Setup

```bash
poetry install
```

## Running the Broadcaster

The broadcaster aggregates data from all 5 sources and publishes to Redis every 200ms:

```bash
# Using default Redis connection (redis://localhost:6379/0)
poetry run python broadcaster.py

# Custom Redis URL and channel
poetry run python broadcaster.py --redis-url redis://localhost:6379/0 --redis-channel terminal-v:data

# Custom interval (in milliseconds)
poetry run python broadcaster.py --interval 500
```

### Environment Variables

Configure data sources via environment variables:

```bash
# Market Stream
export MARKET_WEBSOCKET_URL="wss://api.example.com/stream"
export MARKET_API_KEY="your-api-key"

# Macro Economic
export MACRO_API_URL="https://api.example.com/macro"
export MACRO_API_KEY="your-api-key"

# News Sentiment
export SENTIMENT_API_URL="https://api.example.com/sentiment"
export SENTIMENT_API_KEY="your-api-key"

# Blockchain Scanner
export BLOCKCHAIN_RPC_URL="https://eth-mainnet.g.alchemy.com/v2/..."
export BLOCKCHAIN_RPC_KEY="your-rpc-key"

# User Activity Database
export DB_URL="postgresql://user:pass@localhost/dbname"
export DB_USER="username"
export DB_PASSWORD="password"
export DB_NAME="database"

# Redis Configuration
export REDIS_URL="redis://localhost:6379/0"
export REDIS_CHANNEL="terminal-v:data"
```

## Current Status

**All data sources are currently stubs** - they return mock data. 

To implement real data fetching:
1. Provide API keys/credentials via environment variables
2. Update the service classes in `nexus_engine/services/` to replace stub implementations
3. The broadcaster will automatically use the new implementations

## Data Structure

All aggregated data follows the `AggregatedData` Pydantic model:

```python
{
    "market_stream": {
        "symbol": "BTC/USD",
        "price": 45000.0,
        "volume": 1234567.89,
        "change_24h": 2.5,
        "timestamp": "2024-01-01T00:00:00"
    },
    "macro_econ": {
        "gdp_growth": 2.1,
        "inflation_rate": 3.2,
        "unemployment_rate": 3.7,
        "interest_rate": 5.25,
        "region": "US",
        "timestamp": "2024-01-01T00:00:00"
    },
    "news_sentiment": {
        "sentiment_score": 0.65,
        "sentiment_label": "positive",
        "article_count": 42,
        "keywords": ["bitcoin", "crypto", "bullish"],
        "timestamp": "2024-01-01T00:00:00"
    },
    "blockchain": {
        "network": "ethereum",
        "block_height": 18500000,
        "transaction_count": 150,
        "gas_price": 25.5,
        "hash_rate": 350.2,
        "timestamp": "2024-01-01T00:00:00"
    },
    "user_activity": {
        "active_users": 1234,
        "transactions_24h": 5678,
        "total_volume_24h": 9876543.21,
        "top_symbols": ["BTC/USD", "ETH/USD", "SOL/USD"],
        "timestamp": "2024-01-01T00:00:00"
    },
    "aggregated_at": "2024-01-01T00:00:00",
    "version": "1.0.0"
}
```

## Testing Redis Output

To verify the broadcaster is working, subscribe to the Redis channel:

```bash
# Using redis-cli
redis-cli SUBSCRIBE terminal-v:data

# Or using Python
python -c "import redis; r = redis.Redis(); p = r.pubsub(); p.subscribe('terminal-v:data'); [print(msg) for msg in p.listen()]"
```
