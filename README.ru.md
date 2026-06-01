[English](README.md) | [Русский](README.ru.md)

# AWTRIX Ulanzi CLI

CLI-утилита для управления умными часами [Ulanzi TC001](https://www.ulanzi.com/products/ulanzi-pixel-smart-clock-2882) с прошивкой [AWTRIX 3](https://blueforcer.github.io/awtrix3) через HTTP API.

## Требования

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Часы Ulanzi TC001 с прошивкой AWTRIX 3, подключённые к той же локальной сети

## Установка

```bash
git clone https://github.com/binido/awtrix_ulanzi_cli.git
cd awtrix_ulanzi_cli
uv sync
```

## Первый запуск

При первом запуске мастер настройки предложит выбрать язык интерфейса и ввести IP-адрес часов. Утилита автоматически проверит связь с устройством и сохранит конфигурацию в `config.json`.

```bash
uv run awtrix
```

```
Select interface language / Выберите язык интерфейса:
  1. English
  2. Русский (Russian)
Введите 1 или 2: 2

Введите IP-адрес устройства AWTRIX (например, 192.168.1.100): 192.168.1.37
Подключение к устройству 192.168.1.37...
Успешное подключение к устройству AWTRIX!
  Версия прошивки: 0.96
Конфигурация сохранена. Первоначальная настройка завершена!
```

Для повторной настройки (сменить IP или язык):

```bash
uv run awtrix init
```

## Интерактивная оболочка

Запустите `awtrix` без аргументов или с командой `shell` — откроется интерактивная оболочка. Команды вводятся без префикса `awtrix`.

```bash
uv run awtrix
# или
uv run awtrix shell
```

```
Интерактивная оболочка запущена. Введите 'help' для справки, 'exit' или Ctrl+D для выхода.
Подсказка: Tab — автодополнение, ↑/↓ — история, Ctrl+C — отмена строки.

awtrix (192.168.1.37) > brightness 200
awtrix (192.168.1.37) > notify "Привет!" --color 255 165 0
awtrix (192.168.1.37) > app next
awtrix (192.168.1.37) > exit
```

| Горячая клавиша | Действие |
|---|---|
| `Tab` | Автодополнение команды |
| `↑` / `↓` | История команд |
| `Ctrl+C` | Отменить текущую строку |
| `Ctrl+D` / `exit` / `quit` | Выйти из оболочки |

## Команды

Команды можно запускать и напрямую, без входа в оболочку.

### `status` — Статус устройства

```bash
uv run awtrix status
```

### `power` — Питание дисплея

```bash
uv run awtrix power on
uv run awtrix power off
```

### `reboot` — Перезагрузка

```bash
uv run awtrix reboot
```

### `brightness` — Яркость

```bash
# Установить фиксированное значение (0-255)
uv run awtrix brightness 128

# Включить автояркость
uv run awtrix brightness --auto

# Выключить автояркость
uv run awtrix brightness --auto off
```

### `settings` — Настройки устройства

Ключи настроек соответствуют [документации AWTRIX 3 API](https://blueforcer.github.io/awtrix3/#/api). Значения автоматически определяются как число, булево значение (`true`/`false`) или JSON-массив.

```bash
# Показать все настройки
uv run awtrix settings get

# Показать одну настройку
uv run awtrix settings get BRI

# Установить яркость
uv run awtrix settings set BRI 200

# Включить/выключить автояркость
uv run awtrix settings set ABRI true

# Установить цвет текста по умолчанию (RGB-массив)
uv run awtrix settings set COL '[255,165,0]'

# Переключить формат времени (0 = 24ч, 1 = 12ч)
uv run awtrix settings set TMODE 1
```

### `notify` — Уведомление

```bash
# Простое уведомление
uv run awtrix notify "Привет!"

# С цветом и длительностью
uv run awtrix notify "Тревога!" --color 255 0 0 --duration 10

# С фоном и повтором
uv run awtrix notify "Инфо" --color 255 255 255 --bg-color 0 0 128 --repeat 3

# Радужный текст
uv run awtrix notify "Ура!" --rainbow

# С иконкой и звуком
uv run awtrix notify "Готово" --icon "check" --sound "beep"
```

| Флаг | Описание |
|---|---|
| `--color R G B` | Цвет текста |
| `--bg-color R G B` | Цвет фона |
| `--duration SEC` | Длительность показа в секундах (по умолч. 5) |
| `--repeat N` | Количество повторений (по умолч. 1) |
| `--rainbow` | Радужный эффект |
| `--icon NAME` | Имя иконки из набора устройства |
| `--sound FILE` | Звуковой файл (RTTTL или MP3) |

### `app` — Навигация по приложениям

```bash
uv run awtrix app list           # список приложений в ротации
uv run awtrix app next           # следующее приложение
uv run awtrix app prev           # предыдущее приложение
uv run awtrix app switch clock   # перейти к конкретному приложению
```

### `indicator` — Индикаторные светодиоды

Часы имеют три индикатора (`1`, `2`, `3`). Передайте RGB-значения для включения или `off` для выключения.

```bash
# Установить цвет
uv run awtrix indicator 1 255 0 0

# Выключить
uv run awtrix indicator 2 off

# С миганием (интервал в мс)
uv run awtrix indicator 3 0 255 0 --blink 500

# С затуханием (длительность в мс)
uv run awtrix indicator 1 0 0 255 --fade 1000
```

## Локализация

Файлы локализации находятся в `awtrix/locales/`. Для добавления нового языка создайте файл `awtrix/locales/<код>.json` по образцу `en.json` и укажите код языка в `config.json`.

```
awtrix/locales/
├── en.json   # English
└── ru.json   # Русский
```

## Структура проекта

```
awtrix_ulanzi_cli/
├── awtrix/
│   ├── client.py       # HTTP API клиент
│   ├── config.py       # Управление конфигурацией (config.json)
│   ├── i18n.py         # Движок локализации
│   └── locales/
│       ├── en.json
│       └── ru.json
├── cli/
│   ├── commands/
│   │   ├── apps.py     # app, indicator
│   │   ├── display.py  # brightness, settings
│   │   ├── notify.py   # notify
│   │   └── power.py    # power, reboot
│   ├── init_flow.py    # Мастер настройки
│   ├── main.py         # Точка входа
│   ├── parser.py       # Локализованный ArgumentParser
│   └── repl.py         # Интерактивная оболочка
├── main.py
└── pyproject.toml
```
