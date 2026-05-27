import os
import sys
import subprocess

ICON = "jarvis.ico"
ENTRY_POINT = os.path.join("src", "tray.py")
OUTPUT_NAME = "Jarvis"

sep = ";" if sys.platform == "win32" else ":"

BUILD_ARGS = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    f"--icon={ICON}",
    "--collect-all", "nvidia.cublas",
    "--collect-all", "nvidia.cudnn",
    "--collect-all", "pvporcupine",
    f"--name={OUTPUT_NAME}",
    "--add-data", f"jarvis.ico{sep}.",
    ENTRY_POINT,
]

if not os.path.exists(ICON):
    print(f"[WARN] Icono {ICON} no encontrado. Se usará el default de PyInstaller.")
    BUILD_ARGS.remove(f"--icon={ICON}")

subprocess.run(BUILD_ARGS, check=True)
print(f"\nBuild completo: dist/{OUTPUT_NAME}.exe")
