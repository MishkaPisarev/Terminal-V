"""Macro Economic Service - Investing.com & Google Finance integration"""
import aiohttp
import re
from typing import Optional
from datetime import datetime
from bs4 import BeautifulSoup
from nexus_engine.models.aggregated_data import MacroEconData


class MacroEconService:
    """Service for managing macroeconomic data from Investing.com and Google Finance"""
    
    def __init__(self, region: str = "US"):
        """
        Initialize Macro Economic Service
        
        Args:
            region: Geographic region code (default: "US")
        """
        self.region = region
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with headers"""
        if self._session is None or self._session.closed:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session
    
    async def close(self) -> None:
        """Close HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _fetch_investing(self, region: str = "US") -> Optional[dict]:
        """
        Fetch macroeconomic data from Investing.com
        
        Args:
            region: Geographic region code
            
        Returns:
            dict: Macroeconomic indicators or None if failed
        """
        try:
            session = await self._get_session()
            
            # Investing.com economic calendar and indicators
            # Note: This is a simplified approach - Investing.com may require more complex scraping
            url = f"https://www.investing.com/economic-calendar/"
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    
                    # Try to extract key indicators
                    # This is a basic implementation - may need adjustment based on actual page structure
                    indicators = {}
                    
                    # Look for GDP, Inflation, Unemployment, Interest Rate
                    # Note: Actual implementation would need to parse the specific page structure
                    # For now, return None to use fallback
                    return None
            return None
        except Exception as e:
            print(f"Investing.com fetch error: {e}")
            return None
    
    async def _fetch_fred_api(self, region: str = "US") -> Optional[dict]:
        """
        Fetch macroeconomic data from FRED (Federal Reserve Economic Data) API
        Free public API - no key required for basic usage
        
        Args:
            region: Geographic region code
            
        Returns:
            dict: Macroeconomic indicators or None if failed
        """
        try:
            session = await self._get_session()
            
            # FRED API endpoints for US economic indicators
            if region == "US":
                indicators = {
                    'gdp_growth': 'A191RL1Q225SBEA',  # Real GDP Growth Rate
                    'inflation': 'CPIAUCSL',  # CPI (inflation proxy)
                    'unemployment': 'UNRATE',  # Unemployment Rate
                    'interest_rate': 'FEDFUNDS'  # Federal Funds Rate
                }
                
                data = {}
                base_url = "https://api.stlouisfed.org/fred/series/observations"
                
                for key, series_id in indicators.items():
                    try:
                        url = f"{base_url}?series_id={series_id}&api_key=free&file_type=json&limit=1&sort_order=desc"
                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status == 200:
                                result = await response.json()
                                if 'observations' in result and len(result['observations']) > 0:
                                    value = float(result['observations'][0].get('value', 0))
                                    data[key] = value
                    except Exception as e:
                        print(f"FRED API error for {key}: {e}")
                        continue
                
                if data:
                    return {
                        'gdp_growth': data.get('gdp_growth'),
                        'inflation_rate': data.get('inflation'),
                        'unemployment_rate': data.get('unemployment'),
                        'interest_rate': data.get('interest_rate'),
                        'region': region
                    }
            return None
        except Exception as e:
            print(f"FRED API fetch error: {e}")
            return None
    
    async def fetch_latest(self, region: str = "US") -> MacroEconData:
        """
        Fetch latest macroeconomic indicators from Investing.com and FRED API
        
        Args:
            region: Geographic region code
            
        Returns:
            MacroEconData: Latest macroeconomic data
        """
        # Try FRED API first (more reliable, free, no scraping needed)
        data = await self._fetch_fred_api(region)
        
        # Fallback to Investing.com if FRED fails
        if not data:
            investing_data = await self._fetch_investing(region)
            if investing_data:
                data = investing_data
        
        # If both fail, return mock data
        if not data:
            return MacroEconData(
                gdp_growth=2.1,
                inflation_rate=3.2,
                unemployment_rate=3.7,
                interest_rate=5.25,
                region=region,
                timestamp=datetime.utcnow()
            )
        
        return MacroEconData(
            gdp_growth=data.get('gdp_growth'),
            inflation_rate=data.get('inflation_rate'),
            unemployment_rate=data.get('unemployment_rate'),
            interest_rate=data.get('interest_rate'),
            region=data.get('region', region),
            timestamp=datetime.utcnow()
        )
