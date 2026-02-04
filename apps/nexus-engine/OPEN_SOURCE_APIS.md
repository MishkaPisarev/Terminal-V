# 🚀 Open Source APIs для Terminal-V

Список бесплатных и open source API, которые можно использовать **прямо сейчас** для разработки Terminal-V.

---

## 📈 1. Market Stream (Рыночные данные)

### ✅ Уже используется: yfinance (Google Finance/Yahoo Finance)
```python
import yfinance as yf
ticker = yf.Ticker("BTC-USD")
info = ticker.info
```

### 🌟 Альтернативы:

#### **Alpha Vantage** (Бесплатный tier)
- **URL**: `https://www.alphavantage.co/query`
- **Лимит**: 5 запросов/минуту, 500 запросов/день
- **Регистрация**: Бесплатный API ключ
- **Пример**:
```python
import requests
url = "https://www.alphavantage.co/query"
params = {
    "function": "GLOBAL_QUOTE",
    "symbol": "BTCUSD",
    "apikey": "YOUR_API_KEY"
}
response = requests.get(url, params=params)
```

#### **Polygon.io** (Бесплатный tier)
- **URL**: `https://api.polygon.io`
- **Лимит**: 5 запросов/минуту
- **Регистрация**: Бесплатный API ключ
- **Пример**:
```python
import requests
url = f"https://api.polygon.io/v2/aggs/ticker/BTCUSD/prev"
headers = {"Authorization": f"Bearer YOUR_API_KEY"}
response = requests.get(url, headers=headers)
```

#### **Finnhub** (Бесплатный tier)
- **URL**: `https://finnhub.io/api/v1`
- **Лимит**: 60 запросов/минуту
- **Регистрация**: Бесплатный API ключ
- **Пример**:
```python
import requests
url = "https://finnhub.io/api/v1/quote"
params = {"symbol": "BTCUSD", "token": "YOUR_API_KEY"}
response = requests.get(url, params=params)
```

#### **CoinGecko API** (Бесплатный, без ключа)
- **URL**: `https://api.coingecko.com/api/v3`
- **Лимит**: 10-50 запросов/минуту (без ключа)
- **Регистрация**: Не требуется для базового использования
- **Пример**:
```python
import requests
url = "https://api.coingecko.com/api/v3/simple/price"
params = {"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"}
response = requests.get(url, params=params)
```

---

## 🌍 2. Macro Economic (Макроэкономика)

### ✅ Уже используется: FRED API
```python
# FRED API - бесплатный, без ключа для базового использования
url = "https://api.stlouisfed.org/fred/series/observations"
params = {
    "series_id": "UNRATE",  # Unemployment Rate
    "file_type": "json",
    "sort_order": "desc",
    "limit": 1
}
```

### 🌟 Альтернативы:

#### **World Bank API** (Бесплатный, без ключа)
- **URL**: `https://api.worldbank.org/v2`
- **Данные**: GDP, Inflation, Population, и др.
- **Пример**:
```python
import requests
url = "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD"
params = {"format": "json", "date": "2020:2024"}
response = requests.get(url, params=params)
```

#### **OECD API** (Бесплатный, без ключа)
- **URL**: `https://stats.oecd.org/SDMX-JSON/data`
- **Данные**: GDP, Inflation, Employment
- **Пример**:
```python
import requests
url = "https://stats.oecd.org/SDMX-JSON/data/KEI/USA.GDP/all"
response = requests.get(url)
```

#### **IMF Data API** (Бесплатный, без ключа)
- **URL**: `https://www.imf.org/external/datamapper/api/v1`
- **Данные**: Economic indicators
- **Пример**:
```python
import requests
url = "https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH"
params = {"periods": "2020,2021,2022,2023,2024"}
response = requests.get(url, params=params)
```

---

## 📰 3. News Sentiment (Новости и сентимент)

### ✅ Уже используется: Investing.com (веб-скрапинг)

### 🌟 Альтернативы:

#### **NewsAPI** (Бесплатный tier)
- **URL**: `https://newsapi.org/v2`
- **Лимит**: 100 запросов/день
- **Регистрация**: Бесплатный API ключ
- **Пример**:
```python
import requests
url = "https://newsapi.org/v2/everything"
params = {
    "q": "bitcoin OR cryptocurrency",
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": "YOUR_API_KEY"
}
response = requests.get(url, params=params)
```

#### **Alpha Vantage News & Sentiment** (Бесплатный tier)
- **URL**: `https://www.alphavantage.co/query`
- **Функция**: `NEWS_SENTIMENT`
- **Пример**:
```python
import requests
url = "https://www.alphavantage.co/query"
params = {
    "function": "NEWS_SENTIMENT",
    "tickers": "BTC",
    "apikey": "YOUR_API_KEY"
}
response = requests.get(url, params=params)
```

#### **Finnhub News** (Бесплатный tier)
- **URL**: `https://finnhub.io/api/v1/news`
- **Пример**:
```python
import requests
url = "https://finnhub.io/api/v1/news"
params = {"category": "general", "token": "YOUR_API_KEY"}
response = requests.get(url, params=params)
```

#### **Reddit API** (Бесплатный, без ключа для чтения)
- **URL**: `https://www.reddit.com/r/{subreddit}/hot.json`
- **Пример**:
```python
import requests
url = "https://www.reddit.com/r/CryptoCurrency/hot.json"
headers = {"User-Agent": "Terminal-V/1.0"}
response = requests.get(url, headers=headers)
```

---

## ⛓️ 4. Blockchain (Блокчейн данные)

### 🌟 Open Source RPC Endpoints:

#### **Public Ethereum RPC** (Бесплатный, без ключа)
- **Endpoints**:
  - `https://eth.llamarpc.com`
  - `https://rpc.ankr.com/eth`
  - `https://ethereum.publicnode.com`
- **Пример**:
```python
import requests
url = "https://eth.llamarpc.com"
payload = {
    "jsonrpc": "2.0",
    "method": "eth_blockNumber",
    "params": [],
    "id": 1
}
response = requests.post(url, json=payload)
```

#### **Etherscan API** (Бесплатный tier)
- **URL**: `https://api.etherscan.io/api`
- **Лимит**: 5 запросов/секунду
- **Регистрация**: Бесплатный API ключ
- **Пример**:
```python
import requests
url = "https://api.etherscan.io/api"
params = {
    "module": "proxy",
    "action": "eth_blockNumber",
    "apikey": "YOUR_API_KEY"
}
response = requests.get(url, params=params)
```

#### **BlockCypher API** (Бесплатный tier)
- **URL**: `https://api.blockcypher.com/v1`
- **Лимит**: 3 запроса/секунду
- **Регистрация**: Не требуется для базового использования
- **Пример**:
```python
import requests
url = "https://api.blockcypher.com/v1/eth/main"
response = requests.get(url)
```

#### **Moralis API** (Бесплатный tier)
- **URL**: `https://deep-index.moralis.io/api/v2`
- **Лимит**: 40 запросов/секунду
- **Регистрация**: Бесплатный API ключ
- **Пример**:
```python
import requests
url = "https://deep-index.moralis.io/api/v2/block/date"
params = {"chain": "eth", "date": "2024-01-01"}
headers = {"X-API-Key": "YOUR_API_KEY"}
response = requests.get(url, params=params, headers=headers)
```

---

## 👥 5. User Activity (Пользовательская активность)

### 🌟 Open Source Analytics:

#### **PostgreSQL** (Бесплатный, open source)
- **Использование**: Внутренняя база данных
- **Пример**:
```python
import asyncpg
conn = await asyncpg.connect("postgresql://user:pass@localhost/dbname")
rows = await conn.fetch("SELECT * FROM user_activity WHERE date > NOW() - INTERVAL '24 hours'")
```

#### **Supabase** (Бесплатный tier)
- **URL**: `https://{project}.supabase.co`
- **Лимит**: 500MB база данных, 2GB bandwidth
- **Регистрация**: Бесплатный аккаунт
- **Пример**:
```python
import requests
url = f"https://{project}.supabase.co/rest/v1/user_activity"
headers = {
    "apikey": "YOUR_API_KEY",
    "Authorization": f"Bearer YOUR_API_KEY"
}
response = requests.get(url, headers=headers)
```

---

## 🎯 Рекомендации для быстрого старта

### Для Market Stream:
1. **CoinGecko** (без регистрации) - для криптовалют
2. **yfinance** (уже используется) - для акций и валют
3. **Finnhub** (бесплатный ключ) - для более детальных данных

### Для Macro Economic:
1. **FRED API** (уже используется) - лучший выбор для США
2. **World Bank API** (без регистрации) - для международных данных
3. **OECD API** (без регистрации) - для развитых стран

### Для News Sentiment:
1. **NewsAPI** (бесплатный ключ) - самый простой
2. **Reddit API** (без регистрации) - для социальных сигналов
3. **Alpha Vantage News** (бесплатный ключ) - с встроенным сентиментом

### Для Blockchain:
1. **Public Ethereum RPC** (без регистрации) - для базовых данных
2. **Etherscan API** (бесплатный ключ) - для детальной информации
3. **BlockCypher** (без регистрации) - для мульти-блокчейн

---

## 📦 Установка зависимостей

```bash
cd apps/nexus-engine
poetry add requests aiohttp
# или
pip install requests aiohttp
```

---

## 🔑 Получение API ключей (бесплатно)

1. **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
2. **Polygon.io**: https://polygon.io/dashboard/signup
3. **Finnhub**: https://finnhub.io/register
4. **NewsAPI**: https://newsapi.org/register
5. **Etherscan**: https://etherscan.io/apis
6. **Moralis**: https://moralis.io/

---

## ⚡ Пример интеграции

См. файлы в `nexus_engine/services/` для примеров использования:
- `market_stream.py` - пример с yfinance
- `macro_econ.py` - пример с FRED API
- `news_sentiment.py` - пример с Investing.com

---

## 📝 Примечания

- Все перечисленные API имеют бесплатные tier'ы
- Некоторые требуют регистрации для получения API ключа
- Рекомендуется использовать несколько источников для надежности
- Добавьте обработку ошибок и fallback на резервные источники
- Учитывайте rate limits при разработке

---

**Последнее обновление**: 2024
