# Quick Start Guide - Nexus Engine

## 🚀 Быстрый старт

### Вариант 1: С Poetry (рекомендуется)

```bash
# 1. Установите Poetry (если еще не установлен)
# Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Или через pip:
pip install poetry

# 2. Установите зависимости
cd apps/nexus-engine
poetry install

# 3. Запустите broadcaster
poetry run python broadcaster.py
```

### Вариант 2: Без Poetry (с pip)

```bash
# 1. Создайте виртуальное окружение
cd apps/nexus-engine
python -m venv venv

# 2. Активируйте виртуальное окружение
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 3. Установите зависимости
pip install pydantic pydantic-settings redis[hiredis] aiohttp yfinance beautifulsoup4 lxml requests

# 4. Запустите broadcaster
python broadcaster.py
```

### Вариант 3: Установка Poetry на Windows

```powershell
# Способ 1: Через pip
pip install poetry

# Способ 2: Через официальный установщик
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# После установки добавьте Poetry в PATH (если нужно)
# Обычно: %APPDATA%\Python\Scripts или %LOCALAPPDATA%\pypoetry\Cache
```

---

## ⚙️ Настройка

### Установка переменных окружения (Windows PowerShell)

```powershell
# Символы для отслеживания
$env:MARKET_SYMBOLS="BTCUSD,SPX,EURUSD,TSLA"

# Регион для макроэкономики
$env:MACRO_REGION="US"

# Redis (если не localhost)
$env:REDIS_URL="redis://localhost:6379/0"
$env:REDIS_CHANNEL="terminal-v:data"

# Запуск
poetry run python broadcaster.py
```

### Установка переменных окружения (Windows CMD)

```cmd
set MARKET_SYMBOLS=BTCUSD,SPX,EURUSD,TSLA
set MACRO_REGION=US
set REDIS_URL=redis://localhost:6379/0
set REDIS_CHANNEL=terminal-v:data
poetry run python broadcaster.py
```

---

## 📋 Требования

- Python 3.11+
- Redis (для публикации данных)
  - Установка: https://redis.io/download
  - Или используйте Docker: `docker run -d -p 6379:6379 redis`

---

## ✅ Проверка работы

После запуска вы должны увидеть:

```
✓ Connected to Redis at redis://localhost:6379/0
✓ Starting broadcaster (interval: 200ms)
✓ Publishing to channel: terminal-v:data
Press Ctrl+C to stop...
```

Если видите ошибки:
1. Проверьте, что Redis запущен
2. Проверьте, что все зависимости установлены
3. Проверьте интернет-соединение (для получения данных с сайтов)

---

## 🐛 Troubleshooting

### "poetry: command not found"
**Решение:** Установите Poetry (см. Вариант 3 выше)

### "Redis connection failed"
**Решение:** 
- Убедитесь, что Redis запущен: `redis-cli ping` (должен вернуть PONG)
- Или установите Redis: https://redis.io/download

### "Module not found: yfinance"
**Решение:**
```bash
pip install yfinance beautifulsoup4 lxml requests
```

### "Failed to fetch data"
**Решение:**
- Проверьте интернет-соединение
- Некоторые сайты могут блокировать запросы - это нормально, используется fallback на mock data
