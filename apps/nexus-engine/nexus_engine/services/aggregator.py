"""Data Aggregator Service - Manages all 5 data sources"""
from typing import Optional
from nexus_engine.models.aggregated_data import AggregatedData
from nexus_engine.services.market_stream import MarketStreamService
from nexus_engine.services.macro_econ import MacroEconService
from nexus_engine.services.news_sentiment import NewsSentimentService
from nexus_engine.services.blockchain_scanner import BlockchainScannerService
from nexus_engine.services.user_activity import UserActivityService


class DataAggregatorService:
    """Service that aggregates data from all 5 sources"""
    
    def __init__(
        self,
        # Market Stream config
        market_symbols: Optional[list] = None,
        # Macro Econ config
        macro_region: str = "US",
        # News Sentiment config (no config needed - uses Investing.com directly)
        # Blockchain config
        rpc_url: Optional[str] = None,
        rpc_key: Optional[str] = None,
        # User Activity config
        db_url: Optional[str] = None,
        db_credentials: Optional[dict] = None,
    ):
        """
        Initialize Data Aggregator Service with all data sources
        
        Args:
            market_symbols: List of trading symbols to track (default: ['BTCUSD', 'SPX', 'EURUSD'])
            macro_region: Geographic region for macroeconomic data (default: "US")
            rpc_url: RPC endpoint URL for blockchain scanner
            rpc_key: RPC authentication key
            db_url: Database connection URL for user activity
            db_credentials: Database credentials dict
        """
        # Initialize all service instances
        # Market Stream - gets data from TradingView & Google Finance
        self.market_stream = MarketStreamService(
            symbols=market_symbols
        )
        
        # Macro Econ - gets data from Investing.com & FRED API
        self.macro_econ = MacroEconService(
            region=macro_region
        )
        
        # News Sentiment - gets data from Investing.com
        self.news_sentiment = NewsSentimentService()
        
        self.blockchain_scanner = BlockchainScannerService(
            rpc_url=rpc_url,
            rpc_key=rpc_key
        )
        
        self.user_activity = UserActivityService(
            db_url=db_url,
            db_credentials=db_credentials
        )
    
    async def initialize(self) -> None:
        """Initialize all data source connections"""
        await self.market_stream.connect()
        # Other services don't need explicit connection (REST/DB)
    
    async def shutdown(self) -> None:
        """Shutdown all data source connections"""
        await self.market_stream.disconnect()
        await self.macro_econ.close()
        await self.news_sentiment.close()
    
    async def aggregate(self, region: str = "US", network: str = "ethereum") -> AggregatedData:
        """
        Aggregate data from all 5 sources into normalized structure
        
        Args:
            region: Geographic region for macroeconomic data (default: "US")
            network: Blockchain network name (default: "ethereum")
        
        Returns:
            AggregatedData: Normalized aggregated data object
        """
        # Fetch data from all sources concurrently
        market_data = await self.market_stream.fetch_latest()
        macro_data = await self.macro_econ.fetch_latest(region=region)
        sentiment_data = await self.news_sentiment.fetch_latest()
        blockchain_data = await self.blockchain_scanner.fetch_latest(network=network)
        activity_data = await self.user_activity.fetch_latest()
        
        # Combine into normalized structure
        return AggregatedData(
            market_stream=market_data,
            macro_econ=macro_data,
            news_sentiment=sentiment_data,
            blockchain=blockchain_data,
            user_activity=activity_data
        )
