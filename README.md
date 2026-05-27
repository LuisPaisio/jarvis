# Jarvis — Asistente de voz local para Windows 🎙️

Asistente activado por voz "Jarvis", procesa comandos y preguntas
**totalmente en local**. Sin nube, sin grabaciones externas, sin servidores.

## Stack

| Componente | Tecnología |
|---|---|
| Activación | VAD (voz con "Jarvis") / Push-to-talk (tecla) |
| STT | faster-whisper small (CUDA → CPU fallback) |
| TTS | edge-tts (es-MX-DaliaNeural) |
| Tray icon | pystray + PIL |
| OpenCode CLI bridge | subprocess → opencode.exe --cli |
| Ejecución comandos | PowerShell (abrir/cerrar apps) |
| YouTube Music | Edge/Chrome/Firefox en modo privado |
| VAD | webrtcvad (1.5s silencio threshold) |
| Build | PyInstaller → .exe portátil |

## Comandos de voz

| Intención | Ejemplo |
|---|---|
| Abrir app | "Abrí Steam", "Ejecutá Discord" |
| Cerrar app | "Cerrá Steam", "Matá Discord" |
| Volumen | "Subí el volumen", "Bajá el volumen", "Silenciar" |
| Reproducción | "Pausa", "Reanudar", "Siguiente pista", "Anterior" |
| Discord mute | "Mutear Discord", "Desmutear Discord" |
| Información | "Qué hora es", "Qué día es hoy" |
| YouTube Music | "Buscá Never Gonna Give You Up en YouTube Music" |
| YouTube Music (navegador específico) | "Buscá Bohemian Rhapsody en YouTube Music con Chrome" |
| Tarea compleja | "Creame una función que..." → OpenCode (DeepSeek V4 Flash Free, fallback Nemotron 3 Super Free) |

## Requisitos (para buildear)

- Python 3.11+
- GPU NVIDIA con CUDA (opcional, fallback a CPU)
- OpenCode CLI instalado (en .env o PATH, solo para tareas complejas)
- Windows 10/11 para ejecución final

## Quick start

```bash
git clone <repo>
cd jarvis
python -m venv venv-jarvis
source venv-jarvis/bin/activate   # Linux
# .\venv-jarvis\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env             # Linux
copy .env.example .env           # Windows
# Editar .env con tu OPENCODE_PATH
python src/tray.py
```

## Modos de activación

| Modo | Cómo se usa | Ideal para |
|------|-------------|------------|
| `vad` | Decís "Jarvis ¿qué hora es?" en la frase | Manos libres, escritorio |
| `ptt` | Apretás Ctrl+Alt+Z → hablás → soltás → procesa | Gaming (no escucha Discord, 0% GPU) |

Elegí el modo en `.env` con `WAKE_MODE=ptt` o `WAKE_MODE=vad`.

### Push-to-talk (PTT)
Apretás la tecla configurada, hablás, soltás, y Jarvis procesa lo que dijiste sin necesidad de decir "Jarvis". No consume GPU ni CPU en idle. Ideal para gaming: no interfiere con Discord, no falsos positivos.

## Configuración (.env)

OPENCODE_PATH=C:\ruta\a\opencode.exe   # Obligatorio para tareas OpenCode
LOG_LEVEL=WARNING                       # DEBUG | INFO | WARNING | ERROR | OFF
WAKE_MODE=vad                           # "vad" → voz, "ptt" → tecla
PTT_HOTKEY=ctrl+alt+z                   # Solo en modo ptt

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
│   ├── main.py        # Loop principal (VAD / PTT)
│   ├── recorder.py    # VAD + grabación
│   ├── stt.py         # Whisper STT
│   ├── brain.py       # Clasificador de intención
│   ├── executor.py    # PowerShell commands
│   ├── responder.py   # Preguntas informativas
│   ├── tts.py         # edge-tts
│   ├── tray.py        # Icono de bandeja
│   └── config.py      # .env loader
├── .github/workflows/ # CI/CD build
├── .env.example
├── .env             # Config local (ignorado por git)
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
