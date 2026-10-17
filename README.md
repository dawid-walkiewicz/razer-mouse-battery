# razer-mouse-battery

A tiny system tray icon that shows the battery level of a Razer mouse on Linux.

The icon shows the battery percentage, colored by state:

| Color  | Meaning                                         |
| ------ | ----------------------------------------------- |
| blue   | charging                                        |
| red    | 15% or less                                     |
| orange | 35% or less                                     |
| green  | above 35%                                       |
| grey ? | mouse not found, asleep, or daemon not running  |

Hover the icon for the mouse name and exact level. Right-click to **Quit**. The level refreshes every minute.

## Requirements

- [OpenRazer](https://openrazer.github.io/)
- PyQt6

## Usage

```sh
./razer-battery-tray.py
```

To start it on login, add the script to your desktop's autostart programs.
