from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR

ALUMNOS_FILE = DATA_DIR / "alumnos.json"
RUTINAS_FILE = DATA_DIR / "rutinas.json"
ASISTENCIA_FILE = DATA_DIR / "asistencia.json"

USUARIO = "admin"
CONTRASENA = "1234"
