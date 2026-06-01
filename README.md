# AWTRIX Ulanzi CLI

CLI-утилита для управления умными часами [Ulanzi TC001](https://www.ulanzi.com/products/ulanzi-pixel-smart-clock-2882) с прошивкой [AWTRIX 3](https://blueforcer.github.io/awtrix3) через HTTP API.

A CLI utility for controlling [Ulanzi TC001](https://www.ulanzi.com/products/ulanzi-pixel-smart-clock-2882) smart clocks running [AWTRIX 3](https://blueforcer.github.io/awtrix3) firmware via HTTP API.

---

## Содержание / Table of Contents

- [Требования / Requirements](#требования--requirements)
- [Установка / Installation](#установка--installation)
- [Первый запуск / First Run](#первый-запуск--first-run)
- [Интерактивная оболочка / Interactive Shell](#интерактивная-оболочка--interactive-shell)
- [Команды / Commands](#команды--commands)
- [Локализация / Localization](#локализация--localization)

---

## Требования / Requirements

**RU:** Python 3.10 или новее, [uv](https://docs.astral.sh/uv/getting-started/installation/), часы Ulanzi TC001 с прошивкой AWTRIX 3, подключённые к той же локальной сети.

**EN:** Python 3.10+, [uv](https://docs.astral.sh/uv/getting-started/installation/), Ulanzi TC001 clock running AWTRIX 3 firmware on the same local network.

---

## Установка / Installation

```bash
git clone https://github.com/ArtyomPimenov/awtrix_ulanzi_cli.git
cd awtrix_ulanzi_cli
uv sync
```

---

## Первый запуск / First Run

**RU:** При первом запуске мастер настройки предложит выбрать язык интерфейса и ввести IP-адрес часов. Утилита автоматически проверит связь с устройством и сохранит конфигурацию в `config.json`.

**EN:** On first launch the setup wizard will ask you to choose an interface language and enter the clock's IP address. The utility will verify the connection and save the configuration to `config.json`.

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

**RU:** Для повторной настройки (сменить IP или язык):

**EN:** To reconfigure (change IP or language):

```bash
uv run awtrix init
```

---

## Интерактивная оболочка / Interactive Shell

**RU:** Запустите `awtrix` без аргументов или с командой `shell` — откроется интерактивная оболочка. Команды вводятся без префикса `awtrix`.

**EN:** Run `awtrix` with no arguments or with the `shell` subcommand to open the interactive shell. Commands are entered without the `awtrix` prefix.

```bash
uv run awtrix
# или / or
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

| Горячая клавиша / Shortcut | Действие / Action |
|---|---|
| `Tab` | Автодополнение команды / Autocomplete command |
| `↑` / `↓` | История команд / Command history |
| `Ctrl+C` | Отменить текущую строку / Cancel current line |
| `Ctrl+D` / `exit` / `quit` | Выйти из оболочки / Exit the shell |

---

## Команды / Commands

**RU:** Команды можно запускать и напрямую, без входа в оболочку.

**EN:** Commands can also be run directly, without entering the shell.

### `status` — Статус устройства / Device status

```bash
uv run awtrix status
```

### `power` — Питание дисплея / Display power

```bash
uv run awtrix power on
uv run awtrix power off
```

### `reboot` — Перезагрузка / Reboot

```bash
uv run awtrix reboot
```

### `brightness` — Яркость / Brightness

**RU:** Значение от `0` до `255`.

**EN:** Value from `0` to `255`.

```bash
uv run awtrix brightness 128
```

### `settings` — Настройки устройства / Device settings

**RU:** Ключи настроек соответствуют [документации AWTRIX 3 API](https://blueforcer.github.io/awtrix3/#/api). Значения автоматически определяются как число, булево значение (`true`/`false`) или JSON-массив.

**EN:** Setting keys correspond to the [AWTRIX 3 API docs](https://blueforcer.github.io/awtrix3/#/api). Values are auto-parsed as number, boolean (`true`/`false`), or JSON array.

```bash
# Показать все настройки / Show all settings
uv run awtrix settings get

# Показать одну настройку / Show one setting
uv run awtrix settings get BRI

# Установить яркость / Set brightness
uv run awtrix settings set BRI 200

# Включить/выключить автояркость / Enable/disable auto-brightness
uv run awtrix settings set ABRI true

# Установить цвет текста (RGB) / Set default text color (RGB)
uv run awtrix settings set COL '[255,165,0]'

# Переключить 12/24-часовой формат / Switch 12/24h time format
uv run awtrix settings set TMODE 1
```

### `notify` — Уведомление / Notification

```bash
# Простое уведомление / Simple notification
uv run awtrix notify "Hello!"

# С цветом и длительностью / With color and duration
uv run awtrix notify "Alert!" --color 255 0 0 --duration 10

# С фоном и повтором / With background and repeat
uv run awtrix notify "Info" --color 255 255 255 --bg-color 0 0 128 --repeat 3

# Радужный текст / Rainbow text
uv run awtrix notify "Wow!" --rainbow

# С иконкой и звуком / With icon and sound
uv run awtrix notify "Done" --icon "check" --sound "beep"
```

| Флаг / Flag | Описание / Description |
|---|---|
| `--color R G B` | Цвет текста / Text color |
| `--bg-color R G B` | Цвет фона / Background color |
| `--duration SEC` | Длительность в секундах (по умолч. 5) / Duration in seconds (default 5) |
| `--repeat N` | Количество повторений (по умолч. 1) / Repeat count (default 1) |
| `--rainbow` | Радужный эффект / Rainbow effect |
| `--icon NAME` | Имя иконки / Icon name |
| `--sound FILE` | Звуковой файл / Sound file (RTTTL or MP3) |

### `app` — Навигация по приложениям / App navigation

```bash
uv run awtrix app list           # список приложений / list apps
uv run awtrix app next           # следующее / next
uv run awtrix app prev           # предыдущее / previous
uv run awtrix app switch clock   # перейти к / switch to
```

### `indicator` — Индикаторные светодиоды / Indicator LEDs

**RU:** Часы имеют три индикатора (`1`, `2`, `3`). Передайте RGB-значения для включения или `off` для выключения.

**EN:** The clock has three indicators (`1`, `2`, `3`). Pass RGB values to enable or `off` to disable.

```bash
# Установить цвет / Set color
uv run awtrix indicator 1 255 0 0

# Выключить / Turn off
uv run awtrix indicator 2 off

# С миганием / With blink (ms interval)
uv run awtrix indicator 3 0 255 0 --blink 500

# С затуханием / With fade (ms duration)
uv run awtrix indicator 1 0 0 255 --fade 1000
```

---

## Локализация / Localization

**RU:** Файлы локализации находятся в `awtrix/locales/`. Для добавления нового языка создайте файл `awtrix/locales/<код>.json` по образцу `en.json` и укажите код языка в `config.json`.

**EN:** Locale files are located in `awtrix/locales/`. To add a new language, create `awtrix/locales/<code>.json` based on `en.json` and set the language code in `config.json`.

```
awtrix/locales/
├── en.json   # English
└── ru.json   # Русский
```

---

## Структура проекта / Project Structure

```
awtrix_ulanzi_cli/
├── awtrix/
│   ├── client.py       # HTTP API client
│   ├── config.py       # Config manager (config.json)
│   ├── i18n.py         # Localization engine
│   └── locales/
│       ├── en.json
│       └── ru.json
├── cli/
│   ├── commands/
│   │   ├── apps.py     # app, indicator
│   │   ├── display.py  # brightness, settings
│   │   ├── notify.py   # notify
│   │   └── power.py    # power, reboot
│   ├── init_flow.py    # Setup wizard
│   ├── main.py         # Entry point
│   ├── parser.py       # Localized ArgumentParser
│   └── repl.py         # Interactive shell
├── main.py
└── pyproject.toml
```
