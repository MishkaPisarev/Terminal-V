# Nexus Engine Structure

## Overview

The Nexus Engine aggregates data from 5 distinct sources and publishes normalized JSON to Redis every 200ms.

## File Structure

```
nexus-engine/
├── broadcaster.py              # Main broadcaster script
├── nexus_engine/
│   ├── __init__.py            # Package exports
│   ├── main.py                # Legacy NexusEngine class
│   ├── models/
│   │   ├── __init__.py
│   │   └── aggregated_data.py # Pydantic models for type safety
│   └── services/
│       ├── __init__.py
│       ├── aggregator.py      # Main service managing all 5 sources
│       ├── market_stream.py   # WebSocket stub for market data
│       ├── macro_econ.py      # REST API stub for macro indicators
│       ├── news_sentiment.py  # AI Analysis stub for sentiment
│       ├── blockchain_scanner.py # RPC stub for blockchain data
│       └── user_activity.py   # Internal DB stub for user metrics
├── pyproject.toml             # Poetry dependencies
└── README.md                  # Usage documentation
```

## Data Flow

```
┌─────────────────┐
│ Market Stream   │──┐
│ (WebSocket)     │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │
│ Macro Econ      │──┤
│ (REST API)      │  │
└─────────────────┘  │
                     ├──► DataAggregatorService ──► AggregatedData ──► Redis
┌─────────────────┐  │                              (Pydantic Model)   (200ms)
│ News Sentiment  │──┤
│ (AI Analysis)   │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │
│ Blockchain      │──┤
│ (RPC Scanner)   │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │
│ User Activity   │──┘
│ (Internal DB)   │
└─────────────────┘
```

## Service Classes

### 1. MarketStreamService
- **Type**: WebSocket stub
- **Method**: `fetch_latest()` → `MarketStreamData`
- **Config**: `websocket_url`, `api_key`
- **Status**: Returns mock BTC/USD data

### 2. MacroEconService
- **Type**: REST API stub
- **Method**: `fetch_latest(region)` → `MacroEconData`
- **Config**: `api_url`, `api_key`
- **Status**: Returns mock US economic indicators

### 3. NewsSentimentService
- **Type**: AI Analysis stub
- **Method**: `fetch_latest()` → `NewsSentimentData`
- **Config**: `ai_api_url`, `api_key`
- **Status**: Returns mock sentiment analysis

### 4. BlockchainScannerService
- **Type**: RPC stub
- **Method**: `fetch_latest(network)` → `BlockchainData`
- **Config**: `rpc_url`, `rpc_key`
- **Status**: Returns mock Ethereum metrics

### 5. UserActivityService
- **Type**: Internal DB stub
- **Method**: `fetch_latest()` → `UserActivityData`
- **Config**: `db_url`, `db_credentials`
- **Status**: Returns mock user activity metrics

## Aggregator Service

`DataAggregatorService` manages all 5 sources:
- Initializes all service instances
- Provides `aggregate()` method to fetch from all sources
- Handles connection lifecycle (`initialize()`, `shutdown()`)

## Broadcaster Script

`broadcaster.py`:
- Creates `DataAggregatorService` instance
- Connects to Redis
- Runs aggregation loop every 200ms
- Publishes normalized JSON to Redis channel
- Handles graceful shutdown (Ctrl+C)

## Pydantic Models

All data structures use Pydantic for type safety:

- `MarketStreamData` - Market price, volume, change
- `MacroEconData` - GDP, inflation, unemployment, interest rates
- `NewsSentimentData` - Sentiment score, label, keywords
- `BlockchainData` - Block height, transactions, gas price
- `UserActivityData` - Active users, transactions, volume
- `AggregatedData` - Normalized container for all 5 sources

## Next Steps

To implement real data fetching:

1. **Provide API keys** via environment variables
2. **Update service classes** in `nexus_engine/services/`:
   - Replace stub `fetch_latest()` implementations
   - Add actual WebSocket/REST/RPC/DB calls
   - Handle errors and retries
3. **Test** with `broadcaster.py` and verify Redis output

All services are designed to be drop-in replacements - just update the `fetch_latest()` methods!
