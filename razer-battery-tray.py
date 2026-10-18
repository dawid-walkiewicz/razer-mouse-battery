#!/usr/bin/env python3
import sys
import time
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import QTimer, Qt
from openrazer.client import DeviceManager

INTERVAL_MS = 60_000  # refresh every minute
LOW_LEVEL = 15  # warn at or below this percentage

low_warned = False
last_level = None  # last real reading, shown while the mouse sleeps
last_read_at = None  # time.monotonic() of that reading
tooltip = ("", None)  # (text, reading time to show the age of, or None)


def get_mouse():
    try:
        for d in DeviceManager().devices:
            if d.type == "mouse" and d.has("battery"):
                return d
    except Exception:
        pass
    return None


def make_icon(text, color):
    pm = QPixmap(64, 64)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setPen(QColor(color))
    f = QFont()
    f.setBold(True)
    f.setPixelSize(36 if len(text) < 3 else 28)
    p.setFont(f)
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, text)
    p.end()
    return QIcon(pm)


def set_tooltip(text, read_at=None):
    global tooltip
    tooltip = (text, read_at)
    refresh_tooltip()


def refresh_tooltip():
    text, read_at = tooltip
    if read_at is not None:
        age = round(time.monotonic() - read_at)
        text += f" · updated {age}s ago" if age < 120 else f" · updated {age // 60}m ago"
    tray.setToolTip(text)


def show_unknown(text):
    tray.setIcon(make_icon("?", "#888888"))
    set_tooltip(text)


def update():
    global low_warned, last_level, last_read_at
    m = get_mouse()
    if m is None:
        show_unknown("Razer mouse unavailable")
        return
    # each read is a separate D-Bus call; an uncaught exception in a Qt slot aborts the app
    try:
        name = m.name
        lvl = m.battery_level
        charging = m.is_charging
    except Exception:
        show_unknown("Razer mouse unavailable")
        return
    # a sleeping or switched-off wireless mouse reports 0% while the dongle stays connected
    if lvl == 0 and not charging:
        if last_level is None:
            show_unknown(f"{name}: battery level unknown (mouse asleep or off?)")
        else:
            tray.setIcon(make_icon(str(last_level), "#888888"))
            set_tooltip(f"{name}: {last_level}% (asleep, last reading)", last_read_at)
        return
    last_level = lvl
    last_read_at = time.monotonic()
    if charging:
        color = "#3daee9"
    elif lvl <= LOW_LEVEL:
        color = "#da4453"
    elif lvl <= 35:
        color = "#f67400"
    else:
        color = "#27ae60"
    tray.setIcon(make_icon(str(lvl), color))
    set_tooltip(f"{name}: {lvl}%" + (" (charging)" if charging else ""), last_read_at)

    # notify once per discharge, not on every refresh
    if charging or lvl > LOW_LEVEL:
        low_warned = False
    elif not low_warned:
        tray.showMessage(
            "Razer mouse battery low",
            f"{name}: {lvl}% left",
            QSystemTrayIcon.MessageIcon.Warning,
        )
        low_warned = True


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

tray = QSystemTrayIcon()
menu = QMenu()
menu.addAction("Quit", app.quit)
tray.setContextMenu(menu)

# show() needs an icon, and the first update() may already send a notification
show_unknown("Razer mouse unavailable")
tray.show()
update()

timer = QTimer()
timer.timeout.connect(update)
timer.start(INTERVAL_MS)

# a tray tooltip has no hover event, so keep the age current by rewriting it every second
tooltip_timer = QTimer()
tooltip_timer.timeout.connect(refresh_tooltip)
tooltip_timer.start(1000)

sys.exit(app.exec())
