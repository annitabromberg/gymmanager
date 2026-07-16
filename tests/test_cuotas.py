import json
import re
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


def test_formulario_cuota_no_muestra_opcion_vencida():
    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["usuario"] = "admin"

    response = client.get("/agregar_cuota")

    assert response.status_code == 200
    assert b"Vencida" not in response.data


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
            "fecha_pago": "2026-07-01",
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
    assert saved[0]["monto"] == 50000
    assert saved[0]["fecha_pago"] == "2026-07-01"
    assert saved[0]["vencimiento"] == "2026-07-31"
    assert saved[0]["estado"] == "Pendiente"


def test_inicio_muestra_cantidad_de_cuotas_pendientes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with open(tmp_path / "cuotas.json", "w", encoding="utf-8") as f:
        json.dump([
            {
                "id": 1,
                "alumno": "Ana",
                "plan": "Básico",
                "monto": 35000,
                "fecha_pago": "2026-07-01",
                "vencimiento": "2026-07-31",
                "estado": "Pendiente",
            },
            {
                "id": 2,
                "alumno": "Luis",
                "plan": "Premium",
                "monto": 50000,
                "fecha_pago": "2026-07-05",
                "vencimiento": "2026-08-04",
                "estado": "Pagada",
            },
        ], f)

    with open(tmp_path / "alumnos.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "rutinas.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "asistencia.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["usuario"] = "admin"

    response = client.get("/inicio")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert re.search(r"<h2>Cuotas pendientes</h2>\s*<h1>1</h1>", html)


def test_editar_cuota_preserva_fecha_de_pago_y_vencimiento(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with open(tmp_path / "cuotas.json", "w", encoding="utf-8") as f:
        json.dump([
            {
                "id": 1,
                "alumno": "Ana",
                "plan": "Básico",
                "monto": 35000,
                "fecha_pago": "2026-07-01",
                "vencimiento": "2026-07-31",
                "estado": "Pagada",
            }
        ], f)

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
        "/editar_cuota/1",
        data={
            "alumno": "Ana",
            "plan": "Premium",
            "fecha_pago": "2026-07-15",
            "estado": "Pagada",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with open(tmp_path / "cuotas.json", "r", encoding="utf-8") as f:
        saved = json.load(f)

    assert saved[0]["fecha_pago"] == "2026-07-15"
    assert saved[0]["vencimiento"] == "2026-08-14"
    assert saved[0]["monto"] == 50000
    assert saved[0]["estado"] == "Pagada"
