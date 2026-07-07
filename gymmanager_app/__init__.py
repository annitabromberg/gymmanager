from flask import Flask

from .config import STATIC_DIR, TEMPLATES_DIR
from .routes import main


def create_app():
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )
    app.secret_key = "gymmanager"
    app.register_blueprint(main)
    return app


app = create_app()
