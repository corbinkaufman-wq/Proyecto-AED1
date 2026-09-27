import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
runtime = ROOT / "runtime"
if runtime.exists():
    sys.path.insert(0, str(runtime))

exe = ROOT / ("fenwick.exe" if os.name == "nt" else "fenwick")
zig_spec = importlib.util.find_spec("ziglang")
if zig_spec and zig_spec.origin:
    zig = Path(zig_spec.origin).parent / ("zig.exe" if os.name == "nt" else "zig")
    compiler = [str(zig), "c++"]
elif shutil.which("g++"):
    compiler = ["g++"]
elif shutil.which("clang++"):
    compiler = ["clang++"]
else:
    raise SystemExit("Instala las dependencias: python -m pip install -r requirements.txt")

with (ROOT / "compilacion.log").open("w", encoding="utf-8") as log:
    result = subprocess.run(
        compiler + ["-std=c++17", "fenwick.cpp", "-o", str(exe)],
        stdout=log, stderr=log,
    )
if result.returncode:
    raise SystemExit("No se pudo compilar. Revisa compilacion.log.")

trace = subprocess.check_output([str(exe)], text=True)
data = json.loads(trace)
assert data["query_result"] == 24
assert data["range_result"] == 19
assert data["updated_result"] == 28
(ROOT / "traza.json").write_text(trace, encoding="utf-8")
if "--solo-datos" in sys.argv:
    print("C++: pruebas y traza verificadas.")
    sys.exit(0)

preview = "--preview" in sys.argv
quality = "-ql" if preview else "-qh"
bootstrap = "import sys,runpy; sys.path.insert(0,sys.argv.pop(1)); runpy.run_module('manim',run_name='__main__')"
subprocess.run(
    [sys.executable, "-c", bootstrap, str(runtime), quality,
     "--disable_caching", "--progress_bar", "none", "-v", "WARNING",
     "video.py", "FenwickVideo"],
    check=True,
)
resolution = "480p15" if preview else "1080p60"
source = ROOT / "media" / "videos" / "video" / resolution / "FenwickVideo.mp4"
destination = ROOT / ("Fenwick_preview.mp4" if preview else "Fenwick_Tree.mp4")
shutil.copy2(source, destination)
print(f"Video listo: {destination}")
