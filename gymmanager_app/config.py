from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


def data_dir():
    return Path.cwd()


def alumnos_file():
    return data_dir() / "alumnos.json"


def rutinas_file():
    return data_dir() / "rutinas.json"


def asistencia_file():
    return data_dir() / "asistencia.json"


def cuotas_file():
    return data_dir() / "cuotas.json"


USUARIO = "admin"
CONTRASENA = "1234"
