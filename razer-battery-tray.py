#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import QTimer, Qt
from openrazer.client import DeviceManager

INTERVAL_MS = 60_000  # refresh every minute
LOW_LEVEL = 15  # warn at or below this percentage

low_warned = False
last_level = None  # last real reading, shown while the mouse sleeps


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


def show_unknown(tooltip):
    tray.setIcon(make_icon("?", "#888888"))
    tray.setToolTip(tooltip)


def update():
    global low_warned, last_level
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
            tray.setToolTip(f"{name}: {last_level}% (asleep, last reading)")
        return
    last_level = lvl
    if charging:
        color = "#3daee9"
    elif lvl <= LOW_LEVEL:
        color = "#da4453"
    elif lvl <= 35:
        color = "#f67400"
    else:
        color = "#27ae60"
    tray.setIcon(make_icon(str(lvl), color))
    tray.setToolTip(f"{name}: {lvl}%" + (" (charging)" if charging else ""))

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

sys.exit(app.exec())
