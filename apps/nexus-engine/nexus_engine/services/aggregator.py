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
        websocket_url: Optional[str] = None,
        market_api_key: Optional[str] = None,
        # Macro Econ config
        macro_api_url: Optional[str] = None,
        macro_api_key: Optional[str] = None,
        # News Sentiment config
        sentiment_api_url: Optional[str] = None,
        sentiment_api_key: Optional[str] = None,
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
            websocket_url: WebSocket URL for market stream
            market_api_key: API key for market stream
            macro_api_url: REST API URL for macroeconomic data
            macro_api_key: API key for macroeconomic API
            sentiment_api_url: AI service URL for sentiment analysis
            sentiment_api_key: API key for sentiment service
            rpc_url: RPC endpoint URL for blockchain scanner
            rpc_key: RPC authentication key
            db_url: Database connection URL for user activity
            db_credentials: Database credentials dict
        """
        # Initialize all service instances
        self.market_stream = MarketStreamService(
            websocket_url=websocket_url,
            api_key=market_api_key
        )
        
        self.macro_econ = MacroEconService(
            api_url=macro_api_url,
            api_key=macro_api_key
        )
        
        self.news_sentiment = NewsSentimentService(
            ai_api_url=sentiment_api_url,
            api_key=sentiment_api_key
        )
        
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
