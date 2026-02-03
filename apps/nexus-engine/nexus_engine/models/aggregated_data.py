"""Pydantic models for aggregated data structure"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MarketStreamData(BaseModel):
    """Market stream data from WebSocket"""
    symbol: str = Field(..., description="Trading symbol")
    price: float = Field(..., description="Current price")
    volume: float = Field(..., description="Trading volume")
    change_24h: float = Field(..., description="24-hour price change percentage")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")


class MacroEconData(BaseModel):
    """Macroeconomic indicators from REST API"""
    gdp_growth: Optional[float] = Field(None, description="GDP growth rate")
    inflation_rate: Optional[float] = Field(None, description="Inflation rate")
    unemployment_rate: Optional[float] = Field(None, description="Unemployment rate")
    interest_rate: Optional[float] = Field(None, description="Central bank interest rate")
    region: str = Field(..., description="Geographic region")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")


class NewsSentimentData(BaseModel):
    """News sentiment analysis from AI service"""
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score (-1 to 1)")
    sentiment_label: str = Field(..., description="Sentiment label (positive/negative/neutral)")
    article_count: int = Field(..., ge=0, description="Number of articles analyzed")
    keywords: List[str] = Field(default_factory=list, description="Key terms extracted")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class BlockchainData(BaseModel):
    """Blockchain data from RPC scanner"""
    network: str = Field(..., description="Blockchain network name")
    block_height: int = Field(..., ge=0, description="Current block height")
    transaction_count: int = Field(..., ge=0, description="Transactions in last block")
    gas_price: Optional[float] = Field(None, description="Gas price (if applicable)")
    hash_rate: Optional[float] = Field(None, description="Network hash rate")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Block timestamp")


class UserActivityData(BaseModel):
    """User activity data from internal database"""
    active_users: int = Field(..., ge=0, description="Number of active users")
    transactions_24h: int = Field(..., ge=0, description="Transactions in last 24 hours")
    total_volume_24h: float = Field(..., ge=0.0, description="Total volume in last 24 hours")
    top_symbols: List[str] = Field(default_factory=list, description="Most traded symbols")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Activity timestamp")


class AggregatedData(BaseModel):
    """Normalized aggregated data from all sources"""
    market_stream: MarketStreamData = Field(..., description="Market stream data")
    macro_econ: MacroEconData = Field(..., description="Macroeconomic data")
    news_sentiment: NewsSentimentData = Field(..., description="News sentiment analysis")
    blockchain: BlockchainData = Field(..., description="Blockchain scanner data")
    user_activity: UserActivityData = Field(..., description="User activity metrics")
    aggregated_at: datetime = Field(default_factory=datetime.utcnow, description="Aggregation timestamp")
    version: str = Field(default="1.0.0", description="Data schema version")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
