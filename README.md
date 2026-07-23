# Demon Cry Bot 🔍

Telegram-бот — UI-обёртка для [Demon Cry](https://github.com/Mooncore-inc/demon-cry), автономного OSINT-агента на LLM. Отправь текст в чат — бот перенаправит его агенту и вернёт результат с отчётом об использованных инструментах.

### Как это работает

1. Пользователь пишет сообщение в Telegram
2. Бот отправляет POST-запрос на Demon Cry API (`/api/investigate`)
3. Агент проводит расследование: строит гипотезы, ищет в открытых источниках, парсит сайты
4. Бот возвращает результат с футером: список инструментов и количество токенов

### Установка

#### Локально

Клонируем репозиторий:
```bash
git clone https://github.com/Mooncore-inc/demon-cry-bot.git && cd demon-cry-bot
```

Создаём виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate
```

Устанавливаем зависимости:
```bash
pip install -r requirements.txt
```

Копируем шаблон конфига:
```bash
cp example_config.json config.json
```

Заполняем `config.json`:
```json
{
    "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "api_url": "http://localhost:8000",
    "max_tokens": 10000
}
```

| Поле | Описание |
|------|----------|
| `bot_token` | Токен Telegram-бота (от [@BotFather](https://t.me/BotFather)) |
| `api_url` | URL Demon Cry API (без `/api/investigate`) |
| `max_tokens` | Максимум токенов на одно расследование |

Запуск:
```bash
python -m bot
```

#### Docker

```bash
docker compose up -d
```

Конфиг автоматически пробрасывается через volume. Для просмотра логов:
```bash
docker compose logs -f
```

### Использование

Просто напиши любое сообщение в чат с ботом. Бот автоматически отправит его на расследование.

**Пример:**
```
кто такой fazzyt
```

**Ответ:**
```
Судя по открытым источникам, fazzyt — это псевдоним разработчика...

——————————
🛠 `web_search ×4` · `parse_website ×3`
📊 `7931` tokens
```

### Зависимости

Бот требует работающий Demon Cry API. Если ты используешь Docker — подключи бота к той же сети, что и Demon Cry, и укажи `api_url` как имя контейнера (например, `http://demon-cry:8000`).
