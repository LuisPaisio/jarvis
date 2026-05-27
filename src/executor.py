import subprocess
import logging
import urllib.parse
import os

from src import config

logger = logging.getLogger(__name__)

COMMANDS = {
    "steam": r"start steam://",
    "discord": "start discord",
    "battlefield 6": "start steam://rungameid/2807960",
    "dayz": "start steam://rungameid/221100",
    "arc raiders": "start steam://rungameid/1808500",
    "peak": "start steam://rungameid/3527290",
    "squad": "start steam://rungameid/393380",
}

PROCESS_NAMES = {
    "steam": "steam.exe",
    "discord": "discord.exe",
    "battlefield 6": "bf6.exe",
    "dayz": "DayZ",
    "arc raiders": "ArcRaiders",
    "peak": "PEAK",
    "squad": "Squad",
}

BROWSER_FLAGS = {
    "edge": "start msedge --inprivate",
    "chrome": "start chrome --incognito",
    "firefox": "start firefox --private-window",
}

BROWSER_ALIASES = {
    "edge": "edge",
    "microsoft edge": "edge",
    "msedge": "edge",
    "chrome": "chrome",
    "google chrome": "chrome",
    "google": "chrome",
    "firefox": "firefox",
    "mozilla": "firefox",
    "mozilla firefox": "firefox",
}

TRANSPORT_KEYS = {
    "pausa": "[char]179",
    "reanudar": "[char]179",
    "siguiente": "[char]176",
    "anterior": "[char]177",
}

BROWSER_PROCESSES = {"msedge.exe", "chrome.exe", "firefox.exe", "msedge", "chrome", "firefox"}


def open_app(name: str) -> str:
    name_lower = name.lower().strip()
    for key, uri in COMMANDS.items():
        if key in name_lower:
            cmd = f"Start-Process '{uri}'"
            subprocess.Popen(["powershell", "-Command", cmd], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info("Abriendo %s", key)
            return f"Abriendo {key}"
    return f"No sé cómo abrir {name}"


def close_app(name: str) -> str:
    name_lower = name.lower().strip()
    for key, proc in PROCESS_NAMES.items():
        if key in name_lower:
            cmd = f"Stop-Process -Name '{proc.replace('.exe', '')}' -Force"
            subprocess.Popen(["powershell", "-Command", cmd], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info("Cerrando %s", key)
            return f"Cerrando {key}"
    return f"No encontré {name} ejecutándose"


def open_youtube_music(query: str, browser: str = None) -> str:
    browser = browser or config.DEFAULT_BROWSER
    browser = browser.lower().strip()
    for alias, name in BROWSER_ALIASES.items():
        if alias in browser:
            browser = name
            break
    flag = BROWSER_FLAGS.get(browser)
    if not flag:
        flag = BROWSER_FLAGS["edge"]
        browser = "edge"
    encoded = urllib.parse.quote(query)
    url = f"https://music.youtube.com/search?q={encoded}"
    cmd = f"{flag} '{url}'"
    subprocess.Popen(["powershell", "-Command", cmd], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    logger.info("Buscando '%s' en YouTube Music con %s", query, browser)
    return f"Buscando {query} en YouTube Music"


def _browser_volume() -> object | None:
    try:
        from pycaw.pycaw import AudioUtilities
        sessions = AudioUtilities.GetAllSessions()
        for s in sessions:
            if s.Process and s.Process.name.lower() in BROWSER_PROCESSES:
                return s.SimpleAudioVolume
    except Exception as e:
        logger.error("pycaw error: %s", e)
    return None


def media_action(action: str) -> str:
    if action in TRANSPORT_KEYS:
        key = TRANSPORT_KEYS[action]
        cmd = f"(New-Object -ComObject WScript.Shell).SendKeys({key})"
        subprocess.Popen(["powershell", "-Command", cmd], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info("Media transport: %s", action)
        return f"Comando {action} ejecutado"

    vol = _browser_volume()
    if not vol:
        return "No detecté YouTube Music reproduciendo"

    if action in ("silenciar", "mutear"):
        vol.SetMute(True, None)
        logger.info("YT Music muteado")
        return "YouTube Music silenciado"

    if action == "desmutear":
        vol.SetMute(False, None)
        logger.info("YT Music desmuteado")
        return "YouTube Music con sonido activado"

    current = vol.GetMasterVolume()
    delta = 0.1 if "subí" in action else -0.1
    new_vol = max(0.0, min(1.0, current + delta))
    vol.SetMasterVolume(new_vol, None)
    logger.info("YT Music volumen: %d%%", int(new_vol * 100))
    return f"Volumen de YouTube Music al {int(new_vol * 100)}%"


def discord_mute() -> str:
    if os.name != "nt":
        return "Discord mute solo disponible en Windows"
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.FindWindowW("Chrome_WidgetWin_1", None)
        if not hwnd:
            hwnd = user32.FindWindowW(None, "Discord")
        if not hwnd:
            hwnd = user32.FindWindowW(None, "Discord")
            if not hwnd:
                return "No encontré la ventana de Discord"
        WM_KEYDOWN = 0x0100
        WM_KEYUP = 0x0101
        VK_CONTROL = 0x11
        VK_SHIFT = 0x10
        VK_M = 0x4D
        user32.PostMessageW(hwnd, WM_KEYDOWN, VK_CONTROL, 0)
        user32.PostMessageW(hwnd, WM_KEYDOWN, VK_SHIFT, 0)
        user32.PostMessageW(hwnd, WM_KEYDOWN, VK_M, 0)
        user32.PostMessageW(hwnd, WM_KEYUP, VK_M, 0)
        user32.PostMessageW(hwnd, WM_KEYUP, VK_SHIFT, 0)
        user32.PostMessageW(hwnd, WM_KEYUP, VK_CONTROL, 0)
        logger.info("Discord mute toggled via PostMessage")
        return "Alternando mute de Discord"
    except Exception as e:
        logger.error("Error en discord_mute: %s", e)
        return "Error al mutear Discord"
