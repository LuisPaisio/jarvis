import os
import sys
import subprocess
import openwakeword

ICON = "jarvis.ico"
ENTRY_POINT = os.path.join("src", "tray.py")
OUTPUT_NAME = "Jarvis"

sep = ";" if sys.platform == "win32" else ":"
oww_resources = os.path.join(os.path.dirname(openwakeword.__file__), "resources")

BUILD_ARGS = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    f"--icon={ICON}",
    "--collect-all", "nvidia.cublas",
    "--collect-all", "nvidia.cudnn",
    "--add-data", f"models/hey_jarvis_v0.1.onnx{sep}models/",
    "--add-data", f"{oww_resources}{sep}openwakeword/resources/",
    f"--name={OUTPUT_NAME}",
    "--add-data", f"jarvis.ico{sep}.",
    ENTRY_POINT,
]

if not os.path.exists(ICON):
    print(f"[WARN] Icono {ICON} no encontrado. Se usará el default de PyInstaller.")
    BUILD_ARGS.remove(f"--icon={ICON}")

subprocess.run(BUILD_ARGS, check=True)
print(f"\nBuild completo: dist/{OUTPUT_NAME}.exe")
