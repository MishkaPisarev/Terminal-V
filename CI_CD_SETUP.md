# 🚀 CI/CD Setup for Terminal-V

## Overview

This repository includes GitHub Actions workflows for:
- ✅ **CI** - Continuous Integration (testing, linting, building)
- ✅ **CD** - Continuous Deployment (GitHub Pages for frontend)

---

## 📋 CI Workflow (`.github/workflows/ci.yml`)

### Что делает:
1. **Frontend (Terminal Web)**
   - Устанавливает зависимости (pnpm)
   - Собирает UI Kit
   - Type checking
   - Linting
   - Build
   - Сохраняет артефакты

2. **Core API (FastAPI)**
   - Устанавливает Python 3.11
   - Устанавливает Poetry
   - Linting (ruff)
   - Type checking (mypy)
   - Тесты (pytest)

3. **Nexus Engine (Data Processing)**
   - Устанавливает Python 3.11
   - Устанавливает Poetry
   - Linting (ruff)
   - Type checking (mypy)
   - Тесты (pytest)

### Когда запускается:
- Push в `main` или `develop`
- Pull Request в `main` или `develop`

---

## 🚀 CD Workflow (`.github/workflows/deploy-frontend.yml`)

### Что делает:
1. Собирает Terminal Web frontend
2. Деплоит на GitHub Pages
3. Автоматически обновляет сайт при изменениях

### Когда запускается:
- Push в `main` ветку
- Только если изменены:
  - `apps/terminal-web/**`
  - `packages/ui-kit/**`
  - Сам workflow файл

---

## ⚙️ Настройка GitHub Pages

### Шаг 1: Включите GitHub Pages

1. Зайдите в: **Settings** → **Pages**
2. **Source**: выберите **GitHub Actions**
3. Сохраните

### Шаг 2: Настройте Custom Domain (опционально)

Если хотите использовать поддомен (например, `terminal.valkyrris.com`):

1. В **Settings** → **Pages** → **Custom domain**
2. Введите: `terminal.valkyrris.com`
3. Добавьте CNAME запись в GoDaddy (см. `GODADDY_SUBDOMAIN_SETUP.md`)
4. Включите **Enforce HTTPS**

---

## 🔍 Проверка Workflows

### Просмотр статуса:
1. Зайдите в репозиторий
2. Вкладка **Actions**
3. Выберите workflow run
4. Посмотрите результаты каждого job

### Логи:
- Кликните на job (например, "Terminal Web (Frontend)")
- Разверните шаги для детальных логов

---

## 🐛 Troubleshooting

### CI не запускается
- Проверьте, что файлы в `.github/workflows/` правильно названы (`.yml`)
- Убедитесь, что workflow файлы в репозитории
- Проверьте синтаксис YAML

### Build fails
- Проверьте логи в GitHub Actions
- Убедитесь, что все зависимости указаны
- Проверьте версии Node.js/Python

### Deployment не работает
- Проверьте, что GitHub Pages включен
- Убедитесь, что workflow имеет правильные permissions
- Проверьте, что build успешно завершился

---

## 📝 Добавление новых Workflows

### Пример: Deploy Backend

Если хотите деплоить Core API (например, на Railway/Render):

```yaml
name: Deploy Core API

on:
  push:
    branches: [ main ]
    paths:
      - 'apps/core-api/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # ... ваши шаги деплоя
```

---

## ✅ Checklist

- [x] CI workflow создан (`.github/workflows/ci.yml`)
- [x] CD workflow создан (`.github/workflows/deploy-frontend.yml`)
- [ ] GitHub Pages включен в Settings
- [ ] Первый CI run прошел успешно
- [ ] Frontend деплоится на GitHub Pages
- [ ] Custom domain настроен (если нужно)

---

## 🎯 Следующие шаги

1. **Сделайте commit и push** workflow файлов
2. **Проверьте Actions** tab - должны появиться runs
3. **Настройте GitHub Pages** в Settings
4. **Проверьте деплой** - сайт должен быть доступен

---

## 📚 Полезные ссылки

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [pnpm GitHub Actions](https://github.com/pnpm/action-setup)
- [Poetry GitHub Actions](https://github.com/snok/install-poetry)
