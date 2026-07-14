"""Punto de entrada principal para la aplicación GymManager.

Este archivo solo crea y ejecuta la app. La lógica de negocio está separada en
los módulos de la carpeta gymmanager_app.
"""

from gymmanager_app import app


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
