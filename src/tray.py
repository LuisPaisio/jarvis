import os
import sys
import threading
import pystray
from PIL import Image

from src.main import main


def _get_icon():
    icon_path = os.path.join(os.path.dirname(__file__), "..", "jarvis.ico")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    img = Image.new("RGBA", (64, 64), (0, 120, 255, 255))
    return img


def _is_autostart_enabled() -> bool:
    if os.name != "nt":
        return False
    import winreg
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ,
        )
        winreg.QueryValueEx(key, "JarvisAssistant")
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def _toggle_autostart():
    if os.name != "nt":
        return
    import winreg
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE | winreg.KEY_READ,
    )
    if _is_autostart_enabled():
        winreg.DeleteValue(key, "JarvisAssistant")
    else:
        exe_path = sys.executable
        winreg.SetValueEx(key, "JarvisAssistant", 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)


def run_tray():
    icon = pystray.Icon(
        "Jarvis",
        _get_icon(),
        "Jarvis Assistant",
        menu=pystray.Menu(
            pystray.MenuItem("Iniciar con Windows", _toggle_autostart,
                             checked=lambda: _is_autostart_enabled()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Salir", lambda: icon.stop()),
        ),
    )

    jarvis_thread = threading.Thread(target=main, daemon=True)
    jarvis_thread.start()

    icon.run()


if __name__ == "__main__":
    run_tray()
