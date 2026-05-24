import subprocess
import logging

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
