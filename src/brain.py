import subprocess
import logging
import os
import re

from src import config, executor, responder

logger = logging.getLogger(__name__)

YT_VERBS = ["buscá", "busca", "buscame", "poné", "pone", "reproducí", "reproduce", "tocá", "toca", "pasá", "pasa"]


def classify(text: str) -> str:
    t = text.lower().strip()

    yt_result = _try_youtube_music(t)
    if yt_result:
        return yt_result

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
        logger.warning("OpenCode no encontrado en %s", opencode_path)
        return "No encontré OpenCode instalado"

    try:
        result = subprocess.run(
            [opencode_path, "--cli", "--prompt", prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout.strip()
        if not output:
            output = "No obtuve respuesta de OpenCode"
        return output
    except subprocess.TimeoutExpired:
        logger.error("OpenCode timeout")
        return "OpenCode tardó demasiado en responder"
    except Exception as e:
        logger.error("Error ejecutando OpenCode: %s", e)
        return "Tuve un error al ejecutar OpenCode"
