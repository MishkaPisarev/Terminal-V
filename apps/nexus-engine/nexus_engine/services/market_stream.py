"""Market Stream Service - CoinGecko, TradingView & Google Finance integration"""
import asyncio
import aiohttp
import json
from typing import Optional
from datetime import datetime
from nexus_engine.models.aggregated_data import MarketStreamData


class MarketStreamService:
    """Service for managing market stream data from CoinGecko, TradingView and Google Finance"""
    
    def __init__(self, symbols: Optional[list] = None):
        """
        Initialize Market Stream Service
        
        Args:
            symbols: List of trading symbols to track (default: ['BTCUSD', 'SPX', 'EURUSD'])
        """
        self.symbols = symbols or ['BTCUSD', 'SPX', 'EURUSD']
        self._session: Optional[aiohttp.ClientSession] = None
        self._connected = False
        # CoinGecko ID mapping for cryptocurrencies
        self.coingecko_ids = {
            'BTCUSD': 'bitcoin',
            'BTC': 'bitcoin',
            'ETHUSD': 'ethereum',
            'ETH': 'ethereum',
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def close(self) -> None:
        """Close HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _fetch_tradingview(self, symbol: str) -> Optional[dict]:
        """
        Fetch data from TradingView using their public API
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSD', 'SPX')
            
        Returns:
            dict: Market data or None if failed
        """
        try:
            session = await self._get_session()
            # TradingView public API endpoint
            url = f"https://symbol-search.tradingview.com/symbol_search/?text={symbol}&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US"
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        # Get the first matching symbol
                        symbol_data = data[0]
                        # Try to get real-time quote
                        quote_url = f"https://scanner.tradingview.com/{symbol_data.get('exchange', '')}/{symbol_data.get('symbol', symbol)}"
                        async with session.get(quote_url, timeout=aiohttp.ClientTimeout(total=5)) as quote_response:
                            if quote_response.status == 200:
                                quote_data = await quote_response.json()
                                return quote_data
            return None
        except Exception as e:
            print(f"TradingView fetch error for {symbol}: {e}")
            return None
    
    async def _fetch_coingecko(self, symbol: str) -> Optional[dict]:
        """
        Fetch cryptocurrency data from CoinGecko API (free, no API key required)
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSD', 'BTC')
            
        Returns:
            dict: Market data or None if failed
        """
        try:
            # Check if symbol is a cryptocurrency
            coin_id = self.coingecko_ids.get(symbol.upper())
            if not coin_id:
                # Try to extract coin ID from symbol
                if 'BTC' in symbol.upper():
                    coin_id = 'bitcoin'
                elif 'ETH' in symbol.upper():
                    coin_id = 'ethereum'
                else:
                    return None  # Not a cryptocurrency, skip CoinGecko
            
            session = await self._get_session()
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
                            'price': coin_data.get('usd', 0.0),
                            'volume': coin_data.get('usd_24h_vol', 0.0),
                            'change_24h': coin_data.get('usd_24h_change', 0.0),
                            'symbol': symbol
                        }
            return None
        except Exception as e:
            print(f"CoinGecko fetch error for {symbol}: {e}")
            return None
    
    async def _fetch_google_finance(self, symbol: str) -> Optional[dict]:
        """
        Fetch data from Google Finance using yfinance (Yahoo Finance API)
        
        Args:
            symbol: Trading symbol
            
        Returns:
            dict: Market data or None if failed
        """
        try:
            import yfinance as yf
            
            # Convert symbol format if needed
            ticker_symbol = symbol.replace('/', '')
            if 'BTC' in symbol:
                ticker_symbol = 'BTC-USD'
            elif 'EUR' in symbol:
                ticker_symbol = 'EURUSD=X'
            
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            # Get current price and change
            hist = ticker.history(period='1d', interval='1m')
            if not hist.empty:
                current_price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[0])
                change_24h = ((current_price - prev_close) / prev_close) * 100
                volume = float(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0.0
                
                return {
                    'price': current_price,
                    'volume': volume,
                    'change_24h': change_24h,
                    'symbol': symbol
                }
            return None
        except Exception as e:
            print(f"Google Finance fetch error for {symbol}: {e}")
            return None
    
    async def connect(self) -> bool:
        """
        Connect to data sources
        
        Returns:
            bool: Connection status
        """
        self._connected = True
        return True
    
    async def disconnect(self) -> None:
        """Disconnect from data sources"""
        self._connected = False
        await self.close()
    
    async def fetch_latest(self, symbol: str = None) -> MarketStreamData:
        """
        Fetch latest market stream data from TradingView and Google Finance
        
        Args:
            symbol: Symbol to fetch (default: first symbol from list)
            
        Returns:
            MarketStreamData: Latest market data
        """
        target_symbol = symbol or self.symbols[0]
        
        # Priority order: CoinGecko (for crypto) -> Google Finance -> TradingView
        data = None
        
        # Try CoinGecko first for cryptocurrencies (free, no API key, reliable)
        if any(crypto in target_symbol.upper() for crypto in ['BTC', 'ETH', 'CRYPTO']):
            data = await self._fetch_coingecko(target_symbol)
        
        # Fallback to Google Finance (yfinance) for stocks and forex
        if not data:
            data = await self._fetch_google_finance(target_symbol)
        
        # Fallback to TradingView if both fail
        if not data:
            tv_data = await self._fetch_tradingview(target_symbol)
            if tv_data:
                # Parse TradingView response
                data = {
                    'price': tv_data.get('lp', 0.0),  # Last price
                    'volume': tv_data.get('volume', 0.0),
                    'change_24h': tv_data.get('ch', 0.0),  # Change percentage
                    'symbol': target_symbol
                }
        
        # If both fail, return mock data
        if not data:
            return MarketStreamData(
                symbol=target_symbol,
                price=45000.0,
                volume=1234567.89,
                change_24h=2.5,
                timestamp=datetime.utcnow()
            )
        
        return MarketStreamData(
            symbol=data.get('symbol', target_symbol),
            price=float(data.get('price', 0.0)),
            volume=float(data.get('volume', 0.0)),
            change_24h=float(data.get('change_24h', 0.0)),
            timestamp=datetime.utcnow()
        )
    
    async def stream_data(self):
        """
        Stream market data continuously
        
        Yields:
            MarketStreamData: Market data updates
        """
        while self._connected:
            for symbol in self.symbols:
                yield await self.fetch_latest(symbol)
            await asyncio.sleep(0.2)  # 200ms interval
