import datetime
import logging

logger = logging.getLogger(__name__)


def answer(question: str) -> str:
    q = question.lower().strip()

    if "hora" in q or "qué hora" in q:
        now = datetime.datetime.now()
        return f"Son las {now.hour} y {now.minute} minutos"

    if "día" in q or "fecha" in q or "qué día" in q:
        now = datetime.datetime.now()
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]
        dia_semana = dias[now.weekday()]
        return f"Hoy es {dia_semana} {now.day} de {meses[now.month - 1]} de {now.year}"

    return None
