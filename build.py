import os
import sys
import subprocess
import importlib.util

ICON = "jarvis.ico"
ENTRY_POINT = os.path.join("src", "tray.py")
OUTPUT_NAME = "Jarvis"

sep = ";" if sys.platform == "win32" else ":"

spec_cublas = importlib.util.find_spec('nvidia.cublas')
spec_cudnn = importlib.util.find_spec('nvidia.cudnn')
cublas_lib = os.path.join(spec_cublas.submodule_search_locations[0], 'lib')
cudnn_lib = os.path.join(spec_cudnn.submodule_search_locations[0], 'lib')

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
