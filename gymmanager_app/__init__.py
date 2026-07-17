"""Inicialización de la aplicación Flask para GymManager.

Este módulo crea la instancia principal de Flask, configura la carpeta de
plantillas y archivos estáticos, y registra el blueprint con todas las rutas.
"""

from flask import Flask

from .config import STATIC_DIR, TEMPLATES_DIR
from .routes import main


def create_app():
    """Crea y configura la instancia principal de la aplicación (app)."""
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )
    app.secret_key = "gymmanager"
    """Sin secret_key, las sesiones no funcionan."""
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    """Recargar plantillas automáticamente, para no reiniciar el servidor cada que cambia html"""
    app.jinja_env.auto_reload = True
    """lo mismo pero para jinja"""
    app.register_blueprint(main)
    """conecta todas las rutas con la aplicación."""
    return app


app = create_app()
