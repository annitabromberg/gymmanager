"""Inicialización de la aplicación Flask para GymManager.

Este módulo crea la instancia principal de Flask, configura la carpeta de
plantillas y archivos estáticos, y registra el blueprint con todas las rutas.
"""

from flask import Flask

from .config import STATIC_DIR, TEMPLATES_DIR
from .routes import main


def create_app():
    """Crea y configura la instancia principal de la aplicación."""
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )
    app.secret_key = "gymmanager"
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.register_blueprint(main)
    return app


app = create_app()
