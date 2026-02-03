# Настройка бэкенда для Production

## 📋 Обзор

Для работы Terminal-V в production нужно:
1. Развернуть FastAPI бэкенд (Core API)
2. Настроить переменную окружения `VITE_API_URL` в GitHub
3. Обновить workflow для использования этой переменной

---

## 🚀 Шаг 1: Развертывание бэкенда

### Вариант A: Heroku / Railway / Render (рекомендуется)

1. **Создайте аккаунт** на одном из сервисов:
   - [Heroku](https://heroku.com) (платный после 2022)
   - [Railway](https://railway.app) (бесплатный tier)
   - [Render](https://render.com) (бесплатный tier)

2. **Подключите репозиторий Terminal-V**

3. **Настройте деплой:**
   - Root Directory: `apps/core-api`
   - Build Command: `poetry install && poetry run uvicorn core_api.main:app --host 0.0.0.0 --port $PORT`
   - Start Command: `poetry run uvicorn core_api.main:app --host 0.0.0.0 --port $PORT`

4. **Добавьте переменные окружения:**
   - `REDIS_URL` (если используете внешний Redis)
   - Любые другие секреты для API

5. **Получите URL бэкенда:**
   - Heroku: `https://your-app.herokuapp.com`
   - Railway: `https://your-app.railway.app`
   - Render: `https://your-app.onrender.com`

### Вариант B: VPS / Cloud Server

1. **Создайте VPS** (DigitalOcean, AWS EC2, etc.)

2. **Установите зависимости:**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip
   pip install poetry
   ```

3. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/MishkaPisarev/Terminal-V.git
   cd Terminal-V/apps/core-api
   poetry install
   ```

4. **Запустите с systemd или PM2:**
   ```bash
   poetry run uvicorn core_api.main:app --host 0.0.0.0 --port 8000
   ```

5. **Настройте Nginx reverse proxy** (опционально):
   ```nginx
   server {
       listen 80;
       server_name api.terminal.valkyrris.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

---

## 🔐 Шаг 2: Добавление секрета в GitHub

1. **Откройте репозиторий Terminal-V:**
   - https://github.com/MishkaPisarev/Terminal-V

2. **Перейдите в Settings:**
   - Settings → Secrets and variables → Actions

3. **Нажмите "New repository secret"**

4. **Добавьте секрет:**
   - **Name:** `VITE_API_URL`
   - **Value:** URL вашего бэкенда (например: `https://your-app.railway.app`)
   - **Важно:** Используйте `https://`, не `http://`

5. **Нажмите "Add secret"**

---

## ⚙️ Шаг 3: Обновление Workflow

Workflow уже обновлён для использования `VITE_API_URL`. Проверьте файл:
`.github/workflows/deploy-frontend.yml`

Он должен содержать:
```yaml
- name: Build Terminal Web
  env:
    VITE_API_URL: ${{ secrets.VITE_API_URL }}
  run: pnpm --filter terminal-web build
```

---

## ✅ Шаг 4: Проверка

1. **После добавления секрета:**
   - Workflow запустится автоматически при следующем push
   - Или запустите вручную: Actions → "Deploy Terminal Web" → "Run workflow"

2. **Проверьте деплой:**
   - Откройте `terminal.valkyrris.com`
   - Откройте консоль браузера (F12)
   - Должно быть: "✓ Connected to Nexus stream" (если бэкенд работает)
   - Или: "⚠️ Backend API not configured" (если секрет не добавлен)

3. **Проверьте WebSocket:**
   - В Network tab → WS
   - Должно быть подключение к вашему бэкенду

---

## 🐛 Troubleshooting

### Проблема: "Backend API not configured"
**Решение:**
- Проверьте, что секрет `VITE_API_URL` добавлен в GitHub
- Проверьте, что workflow использует этот секрет
- Перезапустите workflow

### Проблема: WebSocket connection failed
**Решение:**
- Проверьте, что бэкенд запущен и доступен
- Проверьте CORS настройки в FastAPI
- Проверьте, что URL использует `https://` (не `http://`)
- Проверьте, что WebSocket endpoint работает: `wss://your-api.com/ws/nexus-stream`

### Проблема: CORS ошибки
**Решение:**
Добавьте в `apps/core-api/core_api/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://terminal.valkyrris.com", "https://valkyrris.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Текущий статус

- ✅ Frontend готов к использованию переменной `VITE_API_URL`
- ✅ Workflow обновлён для использования секрета
- ⏳ Нужно: Развернуть бэкенд и добавить секрет в GitHub

---

## 🔗 Полезные ссылки

- [Railway Deployment Guide](https://docs.railway.app)
- [Render Deployment Guide](https://render.com/docs)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
