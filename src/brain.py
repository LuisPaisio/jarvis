import subprocess
import logging
import os
import re

from src import config, executor, responder

logger = logging.getLogger(__name__)

YT_VERBS = ["buscá", "busca", "buscame", "poné", "pone", "reproducí", "reproduce", "tocá", "toca", "pasá", "pasa"]
MEDIA_ACTIONS = {
    "subí el volumen": "subí el volumen",
    "bajá el volumen": "bajá el volumen",
    "silenciar": "silenciar",
    "mutear": "mutear",
    "desmutear": "desmutear",
    "activá el sonido": "desmutear",
    "activar sonido": "desmutear",
    "pausa": "pausa",
    "reanudar": "reanudar",
    "siguiente": "siguiente",
    "anterior": "anterior",
    "siguiente pista": "siguiente",
    "pista anterior": "anterior",
    "siguiente canción": "siguiente",
    "canción anterior": "anterior",
    "subí volumen": "subí el volumen",
    "bajá volumen": "bajá el volumen",
}


def classify(text: str) -> str:
    t = text.lower().strip()

    yt_result = _try_youtube_music(t)
    if yt_result:
        return yt_result

    if "discord" in t and any(v in t for v in ["mute", "mutear", "silencia", "desmute", "desmutear", "activá", "activar"]):
        return executor.discord_mute()

    for phrase, action in MEDIA_ACTIONS.items():
        if phrase in t:
            return executor.media_action(action)

    open_verbs = ["abrí", "abre", "ejecutá", "ejecuta", "iniciá", "inicia", "abr"]
    close_verbs = ["cerrá", "cierra", "cerr", "terminá", "termina", "matá", "mata"]

    for verb in open_verbs:
        if t.startswith(verb):
            app = t[len(verb):].strip().lstrip(" ")
            return executor.open_app(app)

    for verb in close_verbs:
        if t.startswith(verb):
            app = t[len(verb):].strip().lstrip(" ")
            return executor.close_app(app)

    rta = responder.answer(t)
    if rta:
        return rta

    return _opencode_query(t)


def _try_youtube_music(t: str) -> str | None:
    if "youtube music" not in t and "yt music" not in t:
        return None

    browser = None
    for alias in executor.BROWSER_ALIASES:
        pattern = rf"(?:con|en|usando)\s+{re.escape(alias)}$"
        m = re.search(pattern, t)
        if m:
            browser = alias
            t = t[:m.start()].strip()
            break

    for verb in YT_VERBS:
        if verb in t:
            idx = t.index(verb) + len(verb)
            query = t[idx:].strip()
            for prefix in ["youtube music", "yt music"]:
                if prefix in query:
                    query = query.replace(prefix, "").strip()
            query = query.lstrip(" ,-").strip()
            if query:
                return executor.open_youtube_music(query, browser)

    return None


def _opencode_query(prompt: str) -> str:
    opencode_path = config.OPENCODE_PATH
    if not opencode_path or not os.path.exists(opencode_path):
        import shutil
        opencode_path = shutil.which("opencode.exe") or shutil.which("opencode")
    if not opencode_path:
        logger.warning("OpenCode no encontrado en .env ni en PATH")
        return "No encontré OpenCode instalado"

    modelos = [config.OPENCODE_MODEL, "Nemotron 3 Super Free"]
    for modelo in modelos:
        try:
            result = subprocess.run(
                [opencode_path, "--cli", "--model", modelo, "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            logger.warning("OpenCode exit code %d con modelo %s", result.returncode, modelo)
        except subprocess.TimeoutExpired:
            logger.warning("Timeout con modelo %s", modelo)
        except Exception as e:
            logger.error("Error con modelo %s: %s", modelo, e)

    return "No pude obtener respuesta"
