[English](README.md) | [Русский](README.ru.md)

# AWTRIX Ulanzi CLI

A CLI utility for controlling [Ulanzi TC001](https://www.ulanzi.com/products/ulanzi-pixel-smart-clock-2882) smart clocks running [AWTRIX 3](https://blueforcer.github.io/awtrix3) firmware via HTTP API.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Ulanzi TC001 with AWTRIX 3 firmware on the same local network

## Installation

```bash
git clone https://github.com/binido/awtrix_ulanzi_cli.git
cd awtrix_ulanzi_cli
uv sync
```

## First Run

On first launch the setup wizard will ask you to choose an interface language and enter the clock's IP address. The utility will verify the connection and save the configuration to `config.json`.

```bash
uv run awtrix
```

```
Select interface language / Выберите язык интерфейса:
  1. English
  2. Русский (Russian)
Enter 1 or 2: 1

Enter AWTRIX device IP address (e.g. 192.168.1.100): 192.168.1.37
Connecting to device at 192.168.1.37...
Successfully connected to AWTRIX device!
  Firmware version: 0.96
Configuration saved. Setup complete!
```

To reconfigure (change IP or language):

```bash
uv run awtrix init
```

## Interactive Shell

Run `awtrix` with no arguments or with the `shell` subcommand to open the interactive shell. Commands are entered without the `awtrix` prefix.

```bash
uv run awtrix
# or
uv run awtrix shell
```

```
Interactive shell started. Type 'help' for commands, 'exit' or Ctrl+D to quit.
Tip: Tab — autocomplete, ↑/↓ — history, Ctrl+C — cancel line.

awtrix (192.168.1.37) > brightness 200
awtrix (192.168.1.37) > notify "Hello!" --color 255 165 0
awtrix (192.168.1.37) > app next
awtrix (192.168.1.37) > exit
```

| Shortcut | Action |
|---|---|
| `Tab` | Autocomplete command |
| `↑` / `↓` | Command history |
| `Ctrl+C` | Cancel current line |
| `Ctrl+D` / `exit` / `quit` | Exit the shell |

## Commands

Commands can also be run directly, without entering the shell.

### `status` — Device status

```bash
uv run awtrix status
```

### `power` — Display power

```bash
uv run awtrix power on
uv run awtrix power off
```

### `reboot` — Reboot

```bash
uv run awtrix reboot
```

### `brightness` — Brightness

Value from `0` to `255`.

```bash
uv run awtrix brightness 128
```

### `settings` — Device settings

Setting keys correspond to the [AWTRIX 3 API docs](https://blueforcer.github.io/awtrix3/#/api). Values are auto-parsed as number, boolean (`true`/`false`), or JSON array.

```bash
# Show all settings
uv run awtrix settings get

# Show one setting
uv run awtrix settings get BRI

# Set brightness
uv run awtrix settings set BRI 200

# Enable/disable auto-brightness
uv run awtrix settings set ABRI true

# Set default text color (RGB array)
uv run awtrix settings set COL '[255,165,0]'

# Switch 12/24h time format (0 = 24h, 1 = 12h)
uv run awtrix settings set TMODE 1
```

### `notify` — Notification

```bash
# Simple notification
uv run awtrix notify "Hello!"

# With color and duration
uv run awtrix notify "Alert!" --color 255 0 0 --duration 10

# With background color and repeat
uv run awtrix notify "Info" --color 255 255 255 --bg-color 0 0 128 --repeat 3

# Rainbow text
uv run awtrix notify "Wow!" --rainbow

# With icon and sound
uv run awtrix notify "Done" --icon "check" --sound "beep"
```

| Flag | Description |
|---|---|
| `--color R G B` | Text color |
| `--bg-color R G B` | Background color |
| `--duration SEC` | Display duration in seconds (default: 5) |
| `--repeat N` | Repeat count (default: 1) |
| `--rainbow` | Rainbow text color effect |
| `--icon NAME` | Icon name from the device icon set |
| `--sound FILE` | Sound file to play (RTTTL or MP3 name) |

### `app` — App navigation

```bash
uv run awtrix app list           # list apps in rotation
uv run awtrix app next           # switch to next app
uv run awtrix app prev           # switch to previous app
uv run awtrix app switch clock   # switch to a specific app
```

### `indicator` — Indicator LEDs

The clock has three indicator LEDs (`1`, `2`, `3`). Pass RGB values to enable or `off` to disable.

```bash
# Set color
uv run awtrix indicator 1 255 0 0

# Turn off
uv run awtrix indicator 2 off

# Blink (ms interval)
uv run awtrix indicator 3 0 255 0 --blink 500

# Fade (ms duration)
uv run awtrix indicator 1 0 0 255 --fade 1000
```

## Localization

Locale files are in `awtrix/locales/`. To add a new language, create `awtrix/locales/<code>.json` based on `en.json` and set the language code in `config.json`.

```
awtrix/locales/
├── en.json   # English
└── ru.json   # Russian
```

## Project Structure

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
