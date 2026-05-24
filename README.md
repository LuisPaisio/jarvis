# Jarvis — Asistente de voz local para Windows 🎙️

Asistente activado por voz que escucha la palabra "Jarvis", procesa comandos y preguntas
**totalmente en local**. Sin nube, sin grabaciones externas, sin servidores.

## Stack

| Componente | Tecnología |
|---|---|
| Wake word | OpenWakeWord (offline) |
| STT | faster-whisper small (CUDA → CPU fallback) |
| TTS | edge-tts (es-MX-DaliaNeutral) |
| Tray icon | pystray + PIL |
| OpenCode bridge | subprocess → opencode.exe --cli |
| Ejecución comandos | PowerShell (abrir/cerrar apps) |
| YouTube Music | Edge/Chrome/Firefox en modo privado |
| VAD | webrtcvad (1.5s silencio threshold) |
| Build | PyInstaller → .exe portátil |

## Comandos de voz

| Intención | Ejemplo |
|---|---|
| Abrir app | "Abrí Steam", "Ejecutá Discord" |
| Cerrar app | "Cerrá Steam", "Matá Discord" |
| Información | "Qué hora es", "Qué día es hoy" |
| YouTube Music | "Buscá Never Gonna Give You Up en YouTube Music" |
| YouTube Music (navegador específico) | "Buscá Bohemian Rhapsody en YouTube Music con Chrome" |
| Tarea compleja | "Creame una función que..." → OpenCode |

## Requisitos (para buildear)

- Python 3.11+
- GPU NVIDIA con CUDA (opcional, fallback a CPU)
- OpenCode CLI en PATH (solo para tareas complejas)
- Windows 10/11 para ejecución final

## Quick start

```bash
git clone <repo>
cd jarvis
python -m venv venv-jarvis
source venv-jarvis/bin/activate   # Linux
# .\venv-jarvis\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tu OPENCODE_PATH
python src/tray.py
```

## Build .exe portable

```bash
pip install pyinstaller
python build.py
# → dist/Jarvis.exe
```

El build automático via GitHub Actions al pushear a `main`.
Descargar artifact → ejecutar en Windows.

## Estructura

```
jarvis/
├── src/
│   ├── main.py        # Loop principal
│   ├── wake.py        # OpenWakeWord
│   ├── recorder.py    # VAD + grabación
│   ├── stt.py         # Whisper STT
│   ├── brain.py       # Clasificador de intención
│   ├── executor.py    # PowerShell commands
│   ├── responder.py   # Preguntas informativas
│   ├── tts.py         # edge-tts
│   ├── tray.py        # Icono de bandeja
│   └── config.py      # .env loader
├── .github/workflows/ # CI/CD build
├── requirements.txt
└── build.py
```

## Seguridad

- Todo corre local — nunca se sube audio a ningún servidor
- OpenCode se comunica con sus providers vía HTTPS normal
- .env ignorado por git — secrets nunca se commitean
- Sin puertos expuestos, sin servidores

---

Desarrollado por [Luis Paisio](https://github.com/luispaisio) como parte de su portfolio.
