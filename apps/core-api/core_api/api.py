"""API endpoints for Terminal-V Core API"""
import os
import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="Terminal-V Core API",
    description="Core API service for Terminal-V financial platform",
    version="0.1.0"
)

# Enable CORS with explicit headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Session for HTTP requests
_session: Optional[aiohttp.ClientSession] = None


async def get_session() -> aiohttp.ClientSession:
    """Get or create HTTP session"""
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


@app.on_event("shutdown")
async def shutdown():
    """Close HTTP session on shutdown"""
    global _session
    if _session and not _session.closed:
        await _session.close()


@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle OPTIONS requests for CORS preflight"""
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "core-api"}


@app.get("/api/market/{symbol}")
async def get_market_data(symbol: str):
    """
    Get market data for a symbol using CoinGecko and yfinance
    
    Args:
        symbol: Trading symbol (e.g., BTCUSD, BTC, SPY, EURUSD)
    """
    session = await get_session()
    
    # Try CoinGecko for cryptocurrencies
    coin_id_map = {
        'BTCUSD': 'bitcoin',
        'BTC': 'bitcoin',
        'ETHUSD': 'ethereum',
        'ETH': 'ethereum',
    }
    
    coin_id = coin_id_map.get(symbol.upper())
    if coin_id:
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_24hr_vol": "true"
            }
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    data = await response.json()
                    if coin_id in data:
                        coin_data = data[coin_id]
                        return {
                            "symbol": symbol,
                            "price": coin_data.get("usd", 0.0),
                            "volume": coin_data.get("usd_24h_vol", 0.0),
                            "change_24h": coin_data.get("usd_24h_change", 0.0),
                            "timestamp": datetime.utcnow().isoformat()
                        }
        except Exception as e:
            print(f"CoinGecko error: {e}")
    
    # Fallback: Try yfinance (requires server-side call)
    try:
        import yfinance as yf
        
        # Convert symbol format
        ticker_symbol = symbol.replace('/', '')
        if 'BTC' in symbol.upper():
            ticker_symbol = 'BTC-USD'
        elif 'EUR' in symbol.upper():
            ticker_symbol = 'EURUSD=X'
        
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period='1d', interval='1m')
        
        if not hist.empty:
            current_price = float(hist['Close'].iloc[-1])
            prev_close = float(hist['Close'].iloc[0])
            change_24h = ((current_price - prev_close) / prev_close) * 100
            volume = float(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0.0
            
            return {
                "symbol": symbol,
                "price": current_price,
                "volume": volume,
                "change_24h": change_24h,
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        print(f"yfinance error: {e}")
    
    raise HTTPException(status_code=404, detail=f"Could not fetch data for symbol: {symbol}")


@app.get("/api/news/sentiment")
async def get_news_sentiment():
    """Get news sentiment from Reddit and NewsAPI"""
    session = await get_session()
    headlines = []
    
    # Try NewsAPI first (if key is available)
    newsapi_key = os.getenv("NEWSAPI_KEY")
    if newsapi_key:
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": "bitcoin OR cryptocurrency OR stock market OR trading",
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 10,
                "apiKey": newsapi_key
            }
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'ok' and 'articles' in data:
                        headlines = [article.get('title', '') for article in data['articles'][:10] if article.get('title')]
        except Exception as e:
            print(f"NewsAPI error: {e}")
    
    # Fallback to Reddit
    if not headlines:
        try:
            subreddits = ['CryptoCurrency', 'investing']
            for subreddit in subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                headers = {"User-Agent": "Terminal-V/1.0"}
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'data' in data and 'children' in data['data']:
                            for post in data['data']['children'][:5]:
                                title = post.get('data', {}).get('title', '')
                                if title and len(title) > 20:
                                    headlines.append(title)
        except Exception as e:
            print(f"Reddit error: {e}")
    
    # Simple sentiment analysis
    positive_keywords = ['up', 'rise', 'gain', 'bullish', 'growth', 'surge', 'rally', 'positive', 'strong', 'beat']
    negative_keywords = ['down', 'fall', 'drop', 'bearish', 'decline', 'crash', 'loss', 'negative', 'weak', 'miss']
    
    positive_count = 0
    negative_count = 0
    keywords_found = []
    
    for headline in headlines:
        headline_lower = headline.lower()
        for keyword in positive_keywords:
            if keyword in headline_lower:
                positive_count += 1
                if keyword not in keywords_found:
                    keywords_found.append(keyword)
        for keyword in negative_keywords:
            if keyword in headline_lower:
                negative_count += 1
                if keyword not in keywords_found:
                    keywords_found.append(keyword)
    
    total = positive_count + negative_count
    if total == 0:
        sentiment_score = 0.0
        sentiment_label = "neutral"
    else:
        sentiment_score = (positive_count - negative_count) / max(total, 1)
        if sentiment_score > 0.3:
            sentiment_label = "positive"
        elif sentiment_score < -0.3:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
    
    return {
        "sentiment_score": sentiment_score,
        "sentiment_label": sentiment_label,
        "article_count": len(headlines),
        "keywords": keywords_found[:10],
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/blockchain/ethereum")
async def get_blockchain_data():
    """Get Ethereum blockchain data from public RPC endpoints"""
    session = await get_session()
    
    # Public Ethereum RPC endpoints
    rpc_endpoints = [
        "https://eth.llamarpc.com",
        "https://rpc.ankr.com/eth",
        "https://ethereum.publicnode.com",
    ]
    
    for endpoint in rpc_endpoints:
        try:
            # Get block number
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            }
            async with session.post(endpoint, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'result' in data:
                        block_number = int(data['result'], 16)
                        
                        # Get block data
                        block_hex = hex(block_number)
                        block_payload = {
                            "jsonrpc": "2.0",
                            "method": "eth_getBlockByNumber",
                            "params": [block_hex, False],
                            "id": 1
                        }
                        async with session.post(endpoint, json=block_payload, timeout=aiohttp.ClientTimeout(total=10)) as block_response:
                            if block_response.status == 200:
                                block_data = await block_response.json()
                                transaction_count = 0
                                if 'result' in block_data and block_data['result']:
                                    transaction_count = len(block_data['result'].get('transactions', []))
                                
                                # Get gas price
                                gas_payload = {
                                    "jsonrpc": "2.0",
                                    "method": "eth_gasPrice",
                                    "params": [],
                                    "id": 1
                                }
                                async with session.post(endpoint, json=gas_payload, timeout=aiohttp.ClientTimeout(total=10)) as gas_response:
                                    if gas_response.status == 200:
                                        gas_data = await gas_response.json()
                                        gas_price = None
                                        if 'result' in gas_data:
                                            gas_price_wei = int(gas_data['result'], 16)
                                            gas_price = gas_price_wei / 1e9  # Convert to Gwei
                                        
                                        return {
                                            "network": "ethereum",
                                            "block_height": block_number,
                                            "transaction_count": transaction_count,
                                            "gas_price": gas_price,
                                            "hash_rate": None,
                                            "timestamp": datetime.utcnow().isoformat()
                                        }
        except Exception as e:
            print(f"RPC endpoint {endpoint} error: {e}")
            continue
    
    raise HTTPException(status_code=503, detail="All RPC endpoints failed")


@app.get("/api/aggregated")
async def get_aggregated_data(symbol: str = "BTCUSD"):
    """
    Get aggregated data from all sources
    
    Args:
        symbol: Market symbol to fetch (default: BTCUSD)
    """
    import asyncio
    
    # Fetch all data concurrently
    market_task = get_market_data(symbol)
    news_task = get_news_sentiment()
    blockchain_task = get_blockchain_data()
    
    try:
        market_data, news_data, blockchain_data = await asyncio.gather(
            market_task,
            news_task,
            blockchain_task,
            return_exceptions=True
        )
        
        # Handle errors
        if isinstance(market_data, Exception):
            market_data = {"symbol": symbol, "price": 0.0, "volume": 0.0, "change_24h": 0.0, "timestamp": datetime.utcnow().isoformat()}
        if isinstance(news_data, Exception):
            news_data = {"sentiment_score": 0.0, "sentiment_label": "neutral", "article_count": 0, "keywords": [], "timestamp": datetime.utcnow().isoformat()}
        if isinstance(blockchain_data, Exception):
            blockchain_data = {"network": "ethereum", "block_height": 0, "transaction_count": 0, "gas_price": None, "hash_rate": None, "timestamp": datetime.utcnow().isoformat()}
        
        # Mock data for macro_econ and user_activity (can be implemented later)
        macro_econ = {
            "gdp_growth": 2.1,
            "inflation_rate": 3.2,
            "unemployment_rate": 3.7,
            "interest_rate": 5.25,
            "region": "US",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        user_activity = {
            "active_users": 1250,
            "transactions_24h": 8500,
            "total_volume_24h": 125000000,
            "top_symbols": ["BTCUSD", "ETHUSD", "SPY"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "market_stream": market_data,
            "macro_econ": macro_econ,
            "news_sentiment": news_data,
            "blockchain": blockchain_data,
            "user_activity": user_activity,
            "aggregated_at": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error aggregating data: {str(e)}")
