# Windows Setup Guide для Nexus Engine

## Шаг 1: Установка Python 3.11+

### Вариант A: Через официальный сайт (рекомендуется)

1. Перейдите на https://www.python.org/downloads/
2. Скачайте Python 3.11 или новее (Windows installer 64-bit)
3. **ВАЖНО**: При установке отметьте галочку **"Add Python to PATH"**
4. Выберите "Install Now" или "Customize installation"
5. Дождитесь завершения установки

### Вариант B: Через Microsoft Store

1. Откройте Microsoft Store
2. Найдите "Python 3.11" или "Python 3.12"
3. Нажмите "Установить"
4. После установки перезапустите PowerShell/Terminal

### Проверка установки

Откройте **новый** PowerShell и выполните:

```powershell
python --version
# Должно показать: Python 3.11.x или Python 3.12.x
```

Если команда не работает, попробуйте:
```powershell
py --version
```

## Шаг 2: Установка зависимостей

После установки Python, выполните следующие команды:

```powershell
# Перейдите в директорию nexus-engine
cd C:\Users\MishkaPisarev\git-repo\MishkaPisarev\Terminal-V\apps\nexus-engine

# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
.\venv\Scripts\Activate.ps1

# Если возникает ошибка "execution of scripts is disabled", выполните:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Обновите pip
python -m pip install --upgrade pip

# Установите зависимости
pip install pydantic pydantic-settings "redis[hiredis]" aiohttp yfinance beautifulsoup4 lxml requests
```

## Шаг 3: Установка Redis (опционально, для локального тестирования)

### Вариант A: Docker (рекомендуется)

Если у вас установлен Docker Desktop:

```powershell
docker run -d -p 6379:6379 --name redis redis
```

### Вариант B: Memurai (Windows-native)

1. Скачайте Memurai: https://www.memurai.com/get-memurai
2. Установите с настройками по умолчанию
3. Redis будет доступен на `localhost:6379`

### Вариант C: WSL2 (Windows Subsystem for Linux)

Если у вас установлен WSL2:

```bash
wsl
sudo apt-get update
sudo apt-get install redis-server
redis-server
```

## Шаг 4: Настройка переменных окружения (опционально)

Создайте файл `.env` в директории `nexus-engine`:

```env
# Market Stream
MARKET_SYMBOLS=BTC-USD,SPY,EURUSD=X,TSLA

# Macro Economic Data (FRED API - опционально)
FRED_API_KEY=your_fred_api_key_here

# News Sentiment
NEWS_URL=https://www.investing.com/news/stock-market-news

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_CHANNEL=terminal-v:data

# Blockchain (опционально)
BLOCKCHAIN_RPC_URL=your_rpc_url
BLOCKCHAIN_RPC_KEY=your_rpc_key

# User Activity Database (опционально)
DB_URL=your_database_url
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

## Шаг 5: Запуск Broadcaster

```powershell
# Убедитесь, что виртуальное окружение активировано
.\venv\Scripts\Activate.ps1

# Запустите broadcaster
python broadcaster.py
```

Или с параметрами:

```powershell
python broadcaster.py --redis-url redis://localhost:6379/0 --interval 200
```

## Устранение проблем

### Ошибка: "execution of scripts is disabled"

Выполните в PowerShell (от администратора):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Ошибка: "pip is not recognized"

Убедитесь, что Python установлен и добавлен в PATH:

```powershell
python -m pip --version
```

Если работает, используйте `python -m pip install ...` вместо `pip install ...`

### Ошибка: "Redis connection failed"

Убедитесь, что Redis запущен:

```powershell
# Для Docker
docker ps | findstr redis

# Для Memurai
# Проверьте службу "Memurai" в Services (services.msc)
```

### Ошибка: "ModuleNotFoundError"

Убедитесь, что виртуальное окружение активировано и зависимости установлены:

```powershell
.\venv\Scripts\Activate.ps1
pip list
```

## Быстрый старт (после установки Python)

```powershell
cd C:\Users\MishkaPisarev\git-repo\MishkaPisarev\Terminal-V\apps\nexus-engine
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install pydantic pydantic-settings "redis[hiredis]" aiohttp yfinance beautifulsoup4 lxml requests
python broadcaster.py
```

## Следующие шаги

После успешного запуска broadcaster:

1. Broadcaster будет публиковать данные в Redis каждые 200ms
2. Запустите `core-api` для создания WebSocket endpoint
3. Настройте `VITE_API_URL` в GitHub Secrets для подключения фронтенда

См. также:
- `QUICK_START.md` - быстрый старт
- `DATA_SOURCES.md` - описание источников данных
- `README.md` - общая документация
