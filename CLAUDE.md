# CLAUDE.md

## Что это за проект

CLI-утилита для управления умными часами **Ulanzi TC001** с прошивкой **AWTRIX 3**.
Цель — упростить настройку часов через удобный терминальный интерфейс, не заходя в веб-интерфейс устройства.

Репозиторий: https://github.com/binido/awtrix_ulanzi_cli
Документация AWTRIX 3 API: https://blueforcer.github.io/awtrix3/#/api

## Технологии

- **Python 3.10+**, пакетный менеджер **uv**
- **requests** — HTTP-клиент для общения с устройством
- **prompt_toolkit** — интерактивная REPL-оболочка
- Запуск: `uv run awtrix`

## Архитектура

```
awtrix/          # Core layer
  client.py      # AwtrixClient — все HTTP-вызовы к устройству
  config.py      # ConfigManager + Config dataclass → config.json
  i18n.py        # I18n — загрузка локалей, метод t()
  locales/
    en.json      # строки интерфейса
    ru.json

cli/             # CLI layer
  main.py        # точка входа, _build_parser(i18n), dispatch через args.func
  repl.py        # интерактивная оболочка (prompt_toolkit)
  parser.py      # LocalizedParser — argparse с примером в сообщении об ошибке
  init_flow.py   # мастер первого запуска (язык + IP)
  commands/
    power.py     # power on/off, reboot
    display.py   # brightness [VALUE|--auto], settings get/set
    notify.py    # notify TEXT [--color --duration --rainbow ...]
    apps.py      # app next/prev/list/switch, indicator
```

## Ключевые паттерны

**Добавление новой команды:**
1. Создать `cli/commands/mycommand.py` с `register(sub, i18n)` и хендлером `_handle(args, client, i18n) -> int`
2. В `register()` вызвать `sub.add_parser(...)`, установить `._example = i18n.t(...)` и `.set_defaults(func=_handle)`
3. Импортировать и зарегистрировать в `cli/main.py`: `cmd_mycommand.register(sub, i18n)`

**Добавление строки локализации:**
Добавить ключ в оба файла: `awtrix/locales/en.json` и `awtrix/locales/ru.json`.
Использовать в коде: `i18n.t("key")` или `i18n.t("key", param=value)`.

**args.func dispatch:**
Все команды регистрируют хендлер через `parser.set_defaults(func=handler)`.
`cli/main.py` создаёт один `AwtrixClient` и вызывает `args.func(args, client, i18n)`.

**LocalizedParser:**
`cli/parser.py` содержит фабрику `make_parser_class(i18n)`. Возвращает подкласс `ArgumentParser`,
чей `error()` дописывает строку `._example` на активном языке.
Вложенные `add_subparsers()` наследуют класс автоматически через `parser_class=type(self)`.

## Конфигурация

Хранится в `config.json` в корне проекта (в `.gitignore`).
Поля: `language` (ru/en), `device_ip`.
Если файла нет или поля отсутствуют — запускается `init_flow`.

## Что намеренно не реализовано

- **Пользовательские приложения (weather, курс валют)** — решено не добавлять в CLI.
  Проект фокусируется на настройке устройства, а не на создании виджетов.
  Для этого лучше использовать Home Assistant, Node-RED или AWTRIX-apps.
- **MQTT** — не нужен для текущих задач (управление настройками, яркостью, уведомлениями).
- **Async** — все запросы синхронные, достаточно для интерактивного CLI.

## Коммиты

Используем **Conventional Commits**: `feat`, `fix`, `docs`, `i18n`, `refactor`.
