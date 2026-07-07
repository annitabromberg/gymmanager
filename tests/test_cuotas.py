import json
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))

app_module = importlib.import_module("gymmanager_app")


def test_cuotas_renderiza_su_contenido():
    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["usuario"] = "admin"

    response = client.get("/cuotas")

    assert response.status_code == 200
    assert b"Gesti\xc3\xb3n de Cuotas" in response.data
    assert b"Nueva Cuota" in response.data


def test_agregar_cuota_guarda_en_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with open(tmp_path / "alumnos.json", "w", encoding="utf-8") as f:
        json.dump([
            {
                "id": 1,
                "nombre": "Ana",
                "edad": "20",
                "dni": "123",
                "telefono": "111",
                "email": "ana@test.com",
                "altura": "160",
                "peso": "55",
                "objetivo": "muscular",
                "plan": "Básico",
                "estado": "Activo",
            }
        ], f)

    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["usuario"] = "admin"

    response = client.post(
        "/agregar_cuota",
        data={
            "alumno": "Ana",
            "plan": "Premium",
            "monto": "25000",
            "vencimiento": "2026-08-10",
            "estado": "Pendiente",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with open(tmp_path / "cuotas.json", "r", encoding="utf-8") as f:
        saved = json.load(f)

    assert len(saved) == 1
    assert saved[0]["alumno"] == "Ana"
    assert saved[0]["plan"] == "Premium"
    assert saved[0]["monto"] == "25000"
    assert saved[0]["estado"] == "Pendiente"
