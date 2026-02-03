"""News Sentiment Service - Investing.com & Google Finance News integration"""
import aiohttp
import re
from typing import Optional, List
from datetime import datetime
from bs4 import BeautifulSoup
from nexus_engine.models.aggregated_data import NewsSentimentData


class NewsSentimentService:
    """Service for managing news sentiment analysis from Investing.com and Google Finance"""
    
    def __init__(self):
        """Initialize News Sentiment Service"""
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
    
    async def _fetch_investing_news(self) -> Optional[List[str]]:
        """
        Fetch financial news headlines from Investing.com
        
        Returns:
            List[str]: List of news headlines or None if failed
        """
        try:
            session = await self._get_session()
            url = "https://www.investing.com/news/"
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    
                    # Find news headlines (structure may vary)
                    headlines = []
                    # Look for article titles
                    articles = soup.find_all(['h3', 'h4', 'a'], class_=re.compile(r'article|news|headline', re.I))
                    
                    for article in articles[:10]:  # Limit to 10 articles
                        text = article.get_text(strip=True)
                        if text and len(text) > 20:  # Filter out short/non-article text
                            headlines.append(text)
                    
                    return headlines if headlines else None
            return None
        except Exception as e:
            print(f"Investing.com news fetch error: {e}")
            return None
    
    def _simple_sentiment_analysis(self, headlines: List[str]) -> dict:
        """
        Simple sentiment analysis based on keywords
        
        Args:
            headlines: List of news headlines
            
        Returns:
            dict: Sentiment analysis results
        """
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
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'keywords': keywords_found[:10]  # Top 10 keywords
        }
    
    async def analyze_sentiment(self, articles: Optional[List[str]] = None) -> NewsSentimentData:
        """
        Analyze news sentiment from Investing.com
        
        Args:
            articles: List of article texts to analyze (optional - will fetch if not provided)
            
        Returns:
            NewsSentimentData: Sentiment analysis results
        """
        # Fetch news if not provided
        if not articles:
            articles = await self._fetch_investing_news()
        
        # If fetch failed, return mock data
        if not articles:
            return NewsSentimentData(
                sentiment_score=0.0,
                sentiment_label="neutral",
                article_count=0,
                keywords=[],
                timestamp=datetime.utcnow()
            )
        
        # Perform simple sentiment analysis
        sentiment_result = self._simple_sentiment_analysis(articles)
        
        return NewsSentimentData(
            sentiment_score=sentiment_result['sentiment_score'],
            sentiment_label=sentiment_result['sentiment_label'],
            article_count=len(articles),
            keywords=sentiment_result['keywords'],
            timestamp=datetime.utcnow()
        )
    
    async def fetch_latest(self) -> NewsSentimentData:
        """
        Fetch latest sentiment analysis from Investing.com
        
        Returns:
            NewsSentimentData: Latest sentiment data
        """
        return await self.analyze_sentiment()
