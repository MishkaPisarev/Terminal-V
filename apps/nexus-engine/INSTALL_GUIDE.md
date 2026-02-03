# Установка и запуск Nexus Engine

## 📋 Требования

- **Python 3.11+** - [Скачать Python](https://www.python.org/downloads/)
- **Poetry** (рекомендуется) или **pip** + **venv**
- **Redis** - для публикации данных

---

## 🔧 Установка Python

### Windows

1. Скачайте Python: https://www.python.org/downloads/
2. При установке **обязательно отметьте**: "Add Python to PATH"
3. Проверьте установку:
   ```powershell
   python --version
   pip --version
   ```

### Linux/Mac

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip

# Mac (с Homebrew)
brew install python@3.11
```

---

## 📦 Установка Poetry

### Windows (PowerShell)

```powershell
# Способ 1: Через pip (рекомендуется)
pip install poetry

# Способ 2: Официальный установщик
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

После установки добавьте Poetry в PATH (если нужно):
```powershell
# Обычно Poetry устанавливается в:
# %APPDATA%\Python\Scripts
# или
# %LOCALAPPDATA%\pypoetry\Cache

# Добавьте в PATH через System Properties → Environment Variables
```

### Linux/Mac

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Проверьте установку:
```bash
poetry --version
```

---

## 🗄️ Установка Redis

### Windows

**Вариант 1: Docker (рекомендуется)**
```powershell
docker run -d -p 6379:6379 --name redis redis
```

**Вариант 2: WSL2**
```bash
# В WSL2
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

**Вариант 3: Memurai (Windows-native Redis)**
- Скачайте: https://www.memurai.com/
- Установите и запустите

### Linux

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### Mac

```bash
brew install redis
brew services start redis
```

Проверьте работу Redis:
```bash
redis-cli ping
# Должно вернуть: PONG
```

---

## 🚀 Установка зависимостей

### С Poetry (рекомендуется)

```bash
cd apps/nexus-engine
poetry install
```

### Без Poetry (с pip)

```bash
cd apps/nexus-engine

# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install pydantic pydantic-settings "redis[hiredis]" aiohttp yfinance beautifulsoup4 lxml requests
```

---

## ▶️ Запуск Broadcaster

### С Poetry

```bash
cd apps/nexus-engine

# Базовый запуск
poetry run python broadcaster.py

# С настройками
$env:MARKET_SYMBOLS="BTCUSD,SPX,EURUSD,TSLA"
$env:MACRO_REGION="US"
poetry run python broadcaster.py
```

### Без Poetry

```bash
cd apps/nexus-engine

# Активируйте виртуальное окружение (если используете venv)
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# или
source venv/bin/activate  # Linux/Mac

# Запустите
python broadcaster.py
```

---

## ✅ Проверка работы

После запуска вы должны увидеть:

```
✓ Connected to Redis at redis://localhost:6379/0
✓ Starting broadcaster (interval: 200ms)
✓ Publishing to channel: terminal-v:data
Press Ctrl+C to stop...
```

Если видите ошибки - см. Troubleshooting ниже.

---

## 🐛 Troubleshooting

### "Python was not found"
**Решение:**
1. Установите Python: https://www.python.org/downloads/
2. При установке отметьте "Add Python to PATH"
3. Перезапустите терминал

### "poetry: command not found"
**Решение:**
```powershell
pip install poetry
# Или используйте pip напрямую (см. "Без Poetry" выше)
```

### "Redis connection failed"
**Решение:**
1. Убедитесь, что Redis запущен:
   ```bash
   redis-cli ping
   # Должно вернуть: PONG
   ```
2. Если Redis не установлен:
   - Windows: Используйте Docker или Memurai
   - Linux: `sudo apt install redis-server && sudo systemctl start redis`
   - Mac: `brew install redis && brew services start redis`

### "Module not found: yfinance"
**Решение:**
```bash
pip install yfinance beautifulsoup4 lxml requests
```

### "Failed to fetch data from [source]"
**Решение:**
- Это нормально - некоторые сайты могут блокировать запросы
- Код автоматически использует fallback на mock data
- Проверьте интернет-соединение
- Для production рассмотрите использование официальных API с ключами

---

## 📝 Быстрая проверка

1. ✅ Python установлен: `python --version`
2. ✅ Redis запущен: `redis-cli ping` → `PONG`
3. ✅ Зависимости установлены: `poetry install` или `pip install ...`
4. ✅ Broadcaster запускается: `poetry run python broadcaster.py`

---

## 🔗 Полезные ссылки

- [Python Downloads](https://www.python.org/downloads/)
- [Poetry Installation](https://python-poetry.org/docs/#installation)
- [Redis Downloads](https://redis.io/download)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
