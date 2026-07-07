import json
from pathlib import Path

from .config import alumnos_file, asistencia_file, cuotas_file, rutinas_file


def cargar_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(path: Path, datos):
    with path.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def cargar_alumnos():
    return cargar_json(alumnos_file(), [])


def guardar_alumnos(alumnos):
    guardar_json(alumnos_file(), alumnos)


def cargar_rutinas():
    return cargar_json(rutinas_file(), [])


def guardar_rutinas(rutinas):
    guardar_json(rutinas_file(), rutinas)


def cargar_asistencia():
    return cargar_json(asistencia_file(), [])


def guardar_asistencia(asistencia):
    guardar_json(asistencia_file(), asistencia)


def cargar_cuotas():
    return cargar_json(cuotas_file(), [])


def guardar_cuotas(cuotas):
    guardar_json(cuotas_file(), cuotas)
