import os
import sys
import subprocess
import nvidia.cublas
import nvidia.cudnn

ICON = "jarvis.ico"
ENTRY_POINT = os.path.join("src", "tray.py")
OUTPUT_NAME = "Jarvis"

sep = ";" if sys.platform == "win32" else ":"

cublas_lib = os.path.join(os.path.dirname(nvidia.cublas.__file__), 'lib')
cudnn_lib = os.path.join(os.path.dirname(nvidia.cudnn.__file__), 'lib')

BUILD_ARGS = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    f"--icon={ICON}",
    "--collect-all", "nvidia.cublas",
    "--collect-all", "nvidia.cudnn",
    "--hidden-import", "keyboard",
    "--add-data", f"{os.path.join(cublas_lib, '*.dll')}{sep}nvidia{os.sep}cublas{os.sep}lib",
    "--add-data", f"{os.path.join(cudnn_lib, '*.dll')}{sep}nvidia{os.sep}cudnn{os.sep}lib",
    f"--name={OUTPUT_NAME}",
    "--add-data", f"jarvis.ico{sep}.",
    ENTRY_POINT,
]

if not os.path.exists(ICON):
    print(f"[WARN] Icono {ICON} no encontrado. Se usará el default de PyInstaller.")
    BUILD_ARGS.remove(f"--icon={ICON}")

subprocess.run(BUILD_ARGS, check=True)
print(f"\nBuild completo: dist/{OUTPUT_NAME}.exe")
