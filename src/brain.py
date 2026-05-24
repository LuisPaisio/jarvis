import subprocess
import logging
import os

from src import config, executor, responder

logger = logging.getLogger(__name__)


def classify(text: str) -> str:
    t = text.lower().strip()

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
