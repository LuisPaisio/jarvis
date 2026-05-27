import datetime
import re


def answer(question: str) -> str:
    q = re.sub(r'[^\w\s]', '', question.lower().strip())

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

    if q in ("hola", "buenos días", "buenas", "buenas tardes", "buenas noches", "qué tal"):
        return "Hola, ¿en qué puedo ayudarte?"
    if q in ("adiós", "chau", "hasta luego", "nos vemos", "me voy"):
        return "Hasta luego, que tengas un buen día"
    if q in ("gracias", "muchas gracias", "te agradezco"):
        return "De nada, cuando quieras"
    if q in ("cómo estás", "como estas", "qué tal estás", "como andas"):
        return "Estoy listo para ayudarte"

    return None
