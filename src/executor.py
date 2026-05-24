import subprocess
import logging
import urllib.parse

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

MEDIA_KEYS = {
    "subí el volumen": "[char]175",
    "bajá el volumen": "[char]174",
    "silenciar": "[char]173",
    "mutear": "[char]173",
    "pausa": "[char]179",
    "reanudar": "[char]179",
    "siguiente": "[char]176",
    "anterior": "[char]177",
}


def open_app(name: str) -> str:
    name_lower = name.lower().strip()
    for key, uri in COMMANDS.items():
        if key in name_lower:
            cmd = f"Start-Process '{uri}'"
            subprocess.Popen(["powershell", "-Command", cmd], shell=True)
            logger.info("Abriendo %s", key)
            return f"Abriendo {key}"
    return f"No sé cómo abrir {name}"


def close_app(name: str) -> str:
    name_lower = name.lower().strip()
    for key, proc in PROCESS_NAMES.items():
        if key in name_lower:
            cmd = f"Stop-Process -Name '{proc.replace('.exe', '')}' -Force"
            subprocess.Popen(["powershell", "-Command", cmd], shell=True)
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
    subprocess.Popen(["powershell", "-Command", cmd], shell=True)
    logger.info("Buscando '%s' en YouTube Music con %s", query, browser)
    return f"Buscando {query} en YouTube Music"


def media_action(action: str) -> str:
    key = MEDIA_KEYS.get(action)
    if not key:
        return None
    cmd = f"(New-Object -ComObject WScript.Shell).SendKeys({key})"
    subprocess.Popen(["powershell", "-Command", cmd], shell=True)
    logger.info("Media action: %s", action)
    return f"Comando {action} ejecutado"


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
