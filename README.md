# razer-mouse-battery

A tiny system tray icon that shows the battery level of a Razer mouse on Linux.

The icon shows the battery percentage, colored by state:

| Color  | Meaning                                         |
| ------ | ----------------------------------------------- |
| blue   | charging                                        |
| red    | 15% or less                                     |
| orange | 35% or less                                     |
| green  | above 35%                                       |
| grey   | mouse asleep; shows the last reading            |
| grey ? | mouse not found, or daemon not running          |

Hover the icon for the mouse name, exact level, and how long ago it was read (seconds, then minutes after 2 minutes). Right-click to **Quit**. The level refreshes every minute.

While the mouse sleeps, the dongle reports 0%, so the icon keeps showing the last real reading in grey instead.

When the battery drops to 15% or less, you get a desktop notification once, until the mouse is charged again.

## Requirements

- [OpenRazer](https://openrazer.github.io/)
- PyQt6

## Usage

```sh
./razer-battery-tray.py
```

To start it on login, link it into your `PATH` and add it to your desktop's autostart programs.

```sh
ln -s "$PWD/razer-battery-tray.py" ~/.local/bin/
```

To restart a running instance after changing the script:

```sh
pkill -f razer-battery-tray.py; setsid -f razer-battery-tray.py >/dev/null 2>&1
```

## License

[MIT](LICENSE)
