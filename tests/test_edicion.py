import json
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT))

app_module = importlib.import_module("gymmanager_app")


def test_asistencia_se_muestra_de_mas_nueva_a_mas_vieja(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with open(tmp_path / "asistencia.json", "w", encoding="utf-8") as f:
        json.dump([
            {
                "id": 1,
                "nombre": "Ana",
                "fecha": "2026-07-01",
                "hora": "09:00",
                "estado": "Presente",
            },
            {
                "id": 2,
                "nombre": "Ana",
                "fecha": "2026-07-10",
                "hora": "11:00",
                "estado": "Presente",
            },
        ], f)

    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["usuario"] = "admin"

    response = client.get("/asistencia")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert html.index("2026-07-10") < html.index("2026-07-01")


def test_editar_alumno_guarda_todos_los_campos(tmp_path, monkeypatch):
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
        "/editar/1",
        data={
            "nombre": "Ana Modificada",
            "edad": "21",
            "dni": "999",
            "telefono": "222",
            "email": "ana2@test.com",
            "altura": "165",
            "peso": "56",
            "objetivo": "resistencia",
            "plan": "Premium",
            "estado": "Inactivo",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with open(tmp_path / "alumnos.json", "r", encoding="utf-8") as f:
        saved = json.load(f)

    alumno = saved[0]
    assert alumno["nombre"] == "Ana Modificada"
    assert alumno["edad"] == "21"
    assert alumno["dni"] == "999"
    assert alumno["telefono"] == "222"
    assert alumno["email"] == "ana2@test.com"
    assert alumno["altura"] == "165"
    assert alumno["peso"] == "56"
    assert alumno["objetivo"] == "resistencia"
    assert alumno["plan"] == "Premium"
    assert alumno["estado"] == "Inactivo"


def test_editar_rutina_guarda_todos_los_campos(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open(tmp_path / "rutinas.json", "w", encoding="utf-8") as f:
        json.dump([
            {
                "id": 1,
                "alumno": "Ana",
                "lunes": "A",
                "martes": "B",
                "miercoles": "C",
                "jueves": "D",
                "viernes": "E",
            }
        ], f)

    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["usuario"] = "admin"

    response = client.post(
        "/editar_rutina/1",
        data={
            "alumno": "Ana",
            "lunes": "L1",
            "martes": "L2",
            "miercoles": "L3",
            "jueves": "L4",
            "viernes": "L5",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with open(tmp_path / "rutinas.json", "r", encoding="utf-8") as f:
        saved = json.load(f)

    rutina = saved[0]
    assert rutina["lunes"] == "L1"
    assert rutina["martes"] == "L2"
    assert rutina["miercoles"] == "L3"
    assert rutina["jueves"] == "L4"
    assert rutina["viernes"] == "L5"


def test_editar_asistencia_guarda_todos_los_campos(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open(tmp_path / "asistencia.json", "w", encoding="utf-8") as f:
        json.dump([
            {
                "id": 1,
                "nombre": "Ana",
                "fecha": "2026-01-01",
                "hora": "10:00",
                "estado": "Presente",
            }
        ], f)

    client = app_module.app.test_client()
    with client.session_transaction() as sess:
        sess["usuario"] = "admin"

    response = client.post(
        "/editar_asistencia/1",
        data={
            "nombre": "Ana",
            "fecha": "2026-01-02",
            "hora": "11:00",
            "estado": "Ausente",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with open(tmp_path / "asistencia.json", "r", encoding="utf-8") as f:
        saved = json.load(f)

    registro = saved[0]
    assert registro["fecha"] == "2026-01-02"
    assert registro["hora"] == "11:00"
    assert registro["estado"] == "Ausente"
