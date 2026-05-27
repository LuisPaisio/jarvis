import logging
import re

from src import executor, responder

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

    return "No entendí tu consulta"


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


    
