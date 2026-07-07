import json
from pathlib import Path

from .config import ALUMNOS_FILE, ASISTENCIA_FILE, RUTINAS_FILE


def cargar_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(path: Path, datos):
    with path.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def cargar_alumnos():
    return cargar_json(ALUMNOS_FILE, [])


def guardar_alumnos(alumnos):
    guardar_json(ALUMNOS_FILE, alumnos)


def cargar_rutinas():
    return cargar_json(RUTINAS_FILE, [])


def guardar_rutinas(rutinas):
    guardar_json(RUTINAS_FILE, rutinas)


def cargar_asistencia():
    return cargar_json(ASISTENCIA_FILE, [])


def guardar_asistencia(asistencia):
    guardar_json(ASISTENCIA_FILE, asistencia)
