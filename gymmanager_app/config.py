"""Configuración central de la aplicación GymManager.

Aquí se definen las rutas a los archivos JSON, las credenciales del sistema y
las constantes generales usadas por el resto de módulos.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


def data_dir():
    """Devuelve la carpeta base desde donde se leen los archivos de datos."""
    return Path.cwd()


def alumnos_file():
    """Ruta del archivo donde se almacenan los alumnos."""
    return data_dir() / "alumnos.json"


def rutinas_file():
    """Ruta del archivo donde se almacenan las rutinas."""
    return data_dir() / "rutinas.json"


def asistencia_file():
    """Ruta del archivo donde se almacenan los registros de asistencia."""
    return data_dir() / "asistencia.json"


def cuotas_file():
    """Ruta del archivo donde se almacenan las cuotas."""
    return data_dir() / "cuotas.json"


USUARIO = "admin"
CONTRASENA = "1234"
