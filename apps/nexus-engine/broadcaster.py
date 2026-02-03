#!/usr/bin/env python3
"""
Broadcaster Script - Aggregates data from 5 sources and pushes to Redis every 200ms

Usage:
    python broadcaster.py [--redis-url REDIS_URL] [--redis-channel CHANNEL]

Environment Variables:
    REDIS_URL: Redis connection URL (default: redis://localhost:6379/0)
    REDIS_CHANNEL: Redis channel name (default: terminal-v:data)
    
    # Data source configuration (optional)
    MARKET_SYMBOLS: Comma-separated list of symbols to track (default: BTCUSD,SPX,EURUSD)
    MACRO_REGION: Geographic region for macroeconomic data (default: US)
    BLOCKCHAIN_RPC_URL: RPC endpoint URL for blockchain scanner
    BLOCKCHAIN_RPC_KEY: RPC authentication key
    DB_URL: Database connection URL for user activity
    
    Note: Market data comes from TradingView & Google Finance (yfinance)
          Macro data comes from Investing.com & FRED API
          News sentiment comes from Investing.com
"""
import asyncio
import json
import os
import signal
import sys
from typing import Optional

import redis.asyncio as redis
from nexus_engine.services.aggregator import DataAggregatorService


class Broadcaster:
    """Broadcaster that aggregates and publishes data to Redis"""
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        redis_channel: str = "terminal-v:data",
        aggregator: Optional[DataAggregatorService] = None
    ):
        """
        Initialize Broadcaster
        
        Args:
            redis_url: Redis connection URL
            redis_channel: Redis channel name for publishing
            aggregator: DataAggregatorService instance (creates default if None)
        """
        self.redis_url = redis_url
        self.redis_channel = redis_channel
        self.redis_client: Optional[redis.Redis] = None
        self.aggregator = aggregator or self._create_default_aggregator()
        self.running = False
    
    def _create_default_aggregator(self) -> DataAggregatorService:
        """Create default aggregator with environment variable configuration"""
        # Parse market symbols from env or use defaults
        market_symbols_str = os.getenv("MARKET_SYMBOLS", "BTCUSD,SPX,EURUSD")
        market_symbols = [s.strip() for s in market_symbols_str.split(",")]
        
        return DataAggregatorService(
            # Market Stream - gets data from TradingView & Google Finance
            market_symbols=market_symbols,
            # Macro Econ - gets data from Investing.com & FRED API
            macro_region=os.getenv("MACRO_REGION", "US"),
            # News Sentiment - gets data from Investing.com (no config needed)
            # Blockchain
            rpc_url=os.getenv("BLOCKCHAIN_RPC_URL"),
            rpc_key=os.getenv("BLOCKCHAIN_RPC_KEY"),
            # User Activity
            db_url=os.getenv("DB_URL"),
            db_credentials=self._parse_db_credentials(),
        )
    
    def _parse_db_credentials(self) -> Optional[dict]:
        """Parse database credentials from environment variables"""
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        
        if db_user and db_password and db_name:
            return {
                "user": db_user,
                "password": db_password,
                "database": db_name,
            }
        return None
    
    async def connect(self) -> None:
        """Connect to Redis"""
        try:
            self.redis_client = await redis.from_url(
                self.redis_url,
                decode_responses=False  # We'll encode JSON ourselves
            )
            # Test connection
            await self.redis_client.ping()
            print(f"✓ Connected to Redis at {self.redis_url}")
        except Exception as e:
            print(f"✗ Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            print("✓ Disconnected from Redis")
    
    async def publish(self, data: dict) -> None:
        """
        Publish aggregated data to Redis channel
        
        Args:
            data: Aggregated data dictionary
        """
        if not self.redis_client:
            raise RuntimeError("Redis client not connected")
        
        # Serialize to JSON
        json_data = json.dumps(data, default=str)
        
        # Publish to Redis channel
        await self.redis_client.publish(self.redis_channel, json_data)
    
    async def run(self, interval_ms: int = 200) -> None:
        """
        Run broadcaster loop - aggregates and publishes every interval_ms
        
        Args:
            interval_ms: Publishing interval in milliseconds
        """
        await self.aggregator.initialize()
        self.running = True
        
        print(f"✓ Starting broadcaster (interval: {interval_ms}ms)")
        print(f"✓ Publishing to channel: {self.redis_channel}")
        print("Press Ctrl+C to stop...")
        
        try:
            while self.running:
                # Aggregate data from all sources
                aggregated_data = await self.aggregator.aggregate()
                
                # Convert to dict for JSON serialization
                data_dict = aggregated_data.model_dump()
                
                # Publish to Redis
                await self.publish(data_dict)
                
                # Wait for next interval
                await asyncio.sleep(interval_ms / 1000.0)
        
        except KeyboardInterrupt:
            print("\n✓ Shutting down...")
        except Exception as e:
            print(f"✗ Error in broadcaster loop: {e}")
            raise
        finally:
            await self.aggregator.shutdown()
            await self.disconnect()
    
    def stop(self) -> None:
        """Stop the broadcaster"""
        self.running = False


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Terminal-V Data Broadcaster")
    parser.add_argument(
        "--redis-url",
        default=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        help="Redis connection URL"
    )
    parser.add_argument(
        "--redis-channel",
        default=os.getenv("REDIS_CHANNEL", "terminal-v:data"),
        help="Redis channel name"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=200,
        help="Publishing interval in milliseconds (default: 200)"
    )
    
    args = parser.parse_args()
    
    # Create broadcaster
    broadcaster = Broadcaster(
        redis_url=args.redis_url,
        redis_channel=args.redis_channel
    )
    
    # Setup signal handlers
    def signal_handler(sig, frame):
        broadcaster.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Connect and run
        await broadcaster.connect()
        await broadcaster.run(interval_ms=args.interval)
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
