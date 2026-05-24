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
