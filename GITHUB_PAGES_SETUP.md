# GitHub Pages Setup for Terminal-V

## 🚀 Настройка GitHub Pages для terminal.valkyrris.com

### Шаг 1: Включите GitHub Pages в Settings

1. Зайдите в репозиторий: https://github.com/MishkaPisarev/Terminal-V
2. **Settings** → **Pages** (в левом меню)
3. **Source**: выберите **GitHub Actions** (не Branch!)
4. Сохраните

---

### Шаг 2: Проверьте, что Deploy Workflow запустился

1. Зайдите в **Actions** tab
2. Найдите workflow **"Deploy Terminal Web"**
3. Проверьте, что он:
   - ✅ Запустился (после последнего push)
   - ✅ Прошел успешно (зеленая галочка)
   - ✅ Деплоился на GitHub Pages

Если workflow не запустился:
- Сделайте небольшой commit в `apps/terminal-web/` или `packages/ui-kit/`
- Или запустите workflow вручную: Actions → Deploy Terminal Web → Run workflow

---

### Шаг 3: Настройте Custom Domain

1. В **Settings** → **Pages** → **Custom domain**
2. Введите: `terminal.valkyrris.com`
3. Нажмите **Save**
4. GitHub проверит DNS (может занять несколько минут)
5. Когда появится зеленая галочка ✓, включите **Enforce HTTPS**

---

### Шаг 4: Настройте DNS в GoDaddy

1. Зайдите в GoDaddy → **My Products** → **Domains** → `valkyrris.com` → **DNS**
2. Добавьте CNAME запись:
   ```
   Type: CNAME
   Name: terminal
   Value: mishkapisarev.github.io
   TTL: 600
   ```
3. Сохраните

---

### Шаг 5: Проверьте DNS

```powershell
nslookup terminal.valkyrris.com
```

Должно показать:
```
Name:    mishkapisarev.github.io
Address: [IP адрес GitHub]
```

Или проверьте онлайн:
- https://dnschecker.org/#CNAME/terminal.valkyrris.com

---

## 🐛 Troubleshooting

### "404 - There isn't a GitHub Pages site here"

**Причины:**
1. GitHub Pages не включен в Settings
2. Deploy workflow не запустился или упал
3. Custom domain не настроен

**Решение:**
1. Проверьте Settings → Pages → Source = **GitHub Actions**
2. Проверьте Actions tab - должен быть успешный deploy
3. Если workflow не запускается, сделайте commit в `apps/terminal-web/`

---

### Workflow не запускается

**Проверьте:**
- Workflow файл существует: `.github/workflows/deploy-frontend.yml`
- Workflow настроен на `push` в `main` ветку
- Изменения в `apps/terminal-web/**` или `packages/ui-kit/**`

**Решение:**
- Сделайте небольшой commit (например, добавьте комментарий в код)
- Или запустите workflow вручную: Actions → Deploy Terminal Web → Run workflow

---

### DNS не работает

**Проверьте:**
- CNAME запись добавлена в GoDaddy
- Name: только `terminal` (не `terminal.valkyrris.com`)
- Value: точно `mishkapisarev.github.io`
- Подождите 10-30 минут для распространения DNS

---

## ✅ Checklist

- [ ] GitHub Pages включен (Settings → Pages → Source: GitHub Actions)
- [ ] Deploy workflow запустился и прошел успешно
- [ ] Custom domain настроен: `terminal.valkyrris.com`
- [ ] DNS CNAME запись добавлена в GoDaddy
- [ ] DNS проверен через nslookup или dnschecker.org
- [ ] Подождали 10-30 минут после настройки DNS
- [ ] Enforce HTTPS включен в GitHub Pages

---

## 🎯 После настройки

Сайт будет доступен на:
- `https://terminal.valkyrris.com` (custom domain)
- `https://MishkaPisarev.github.io/Terminal-V/` (GitHub Pages URL)

---

## 📝 Примечания

- GitHub Pages использует GitHub Actions для деплоя
- Сайт обновляется автоматически при каждом push в `main`
- Custom domain требует правильной настройки DNS
- HTTPS включается автоматически после настройки custom domain
