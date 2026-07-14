"""Acceso a datos y manejo de archivos JSON para GymManager.

Este módulo se encarga de leer y escribir los archivos JSON que almacenan la
información del sistema: alumnos, rutinas, asistencia y cuotas.
"""

import json
from pathlib import Path

from .config import alumnos_file, asistencia_file, cuotas_file, rutinas_file


def cargar_json(path: Path, default):
    """Carga un JSON desde disco o devuelve un valor por defecto si no existe."""
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(path: Path, datos):
    """Guarda un objeto Python en formato JSON en disco."""
    with path.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def cargar_alumnos():
    """Devuelve la lista de alumnos almacenada en el archivo JSON."""
    return cargar_json(alumnos_file(), [])


def guardar_alumnos(alumnos):
    """Guarda la lista de alumnos en el archivo JSON."""
    guardar_json(alumnos_file(), alumnos)


def cargar_rutinas():
    """Devuelve la lista de rutinas almacenada en el archivo JSON."""
    return cargar_json(rutinas_file(), [])


def guardar_rutinas(rutinas):
    """Guarda la lista de rutinas en el archivo JSON."""
    guardar_json(rutinas_file(), rutinas)


def cargar_asistencia():
    """Devuelve la lista de asistencias almacenada en el archivo JSON."""
    return cargar_json(asistencia_file(), [])


def guardar_asistencia(asistencia):
    """Guarda la lista de asistencias en el archivo JSON."""
    guardar_json(asistencia_file(), asistencia)


def cargar_cuotas():
    """Devuelve la lista de cuotas almacenada en el archivo JSON."""
    return cargar_json(cuotas_file(), [])


def guardar_cuotas(cuotas):
    """Guarda la lista de cuotas en el archivo JSON."""
    guardar_json(cuotas_file(), cuotas)
