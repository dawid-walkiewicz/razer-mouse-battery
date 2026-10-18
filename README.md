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

Hover the icon for the mouse name and exact level. Right-click to **Quit**. The level refreshes every minute.

When the battery drops to 15% or less, you get a desktop notification once, until the mouse is charged again.

## Requirements

- [OpenRazer](https://openrazer.github.io/)
- PyQt6

## Usage

```sh
./razer-battery-tray.py
```

To start it on login, add the script to your desktop's autostart programs.

## License

[MIT](LICENSE)
