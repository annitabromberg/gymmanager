from flask import Blueprint, redirect, render_template, request, session

from .config import CONTRASENA, USUARIO
from .data import (
    cargar_alumnos,
    cargar_asistencia,
    cargar_cuotas,
    cargar_rutinas,
    guardar_alumnos,
    guardar_asistencia,
    guardar_cuotas,
    guardar_rutinas,
)

main = Blueprint("main", __name__)


def requiere_login():
    if "usuario" not in session:
        return redirect("/")
    return None


@main.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["password"]

        if usuario == USUARIO and contrasena == CONTRASENA:
            session["usuario"] = usuario
            return redirect("/inicio")

        return render_template("login.html", error="Usuario o contraseña incorrectos.")

    return render_template("login.html")


@main.route("/inicio")
def inicio():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    alumnos = cargar_alumnos()
    rutinas = cargar_rutinas()
    asistencias = cargar_asistencia()
    cuotas = cargar_cuotas()

    return render_template(
        "inicio.html",
        cantidad=len(alumnos),
        cantidad_rutinas=len(rutinas),
        cantidad_asistencia=len(asistencias),
        cantidad_cuotas=sum(1 for cuota in cuotas if cuota.get("estado") == "Pendiente"),
        ultimos_alumnos=alumnos[-5:][::-1],
        ultimas_asistencias=asistencias[-5:][::-1],
    )


@main.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@main.route("/alumnos")
def alumnos():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    lista = cargar_alumnos()
    buscar = request.args.get("buscar", "")

    if buscar:
        lista = [alumno for alumno in lista if buscar.lower() in alumno["nombre"].lower()]

    return render_template("alumnos.html", alumnos=lista, buscar=buscar)


@main.route("/agregar", methods=["GET", "POST"])
def agregar():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    alumnos = cargar_alumnos()

    if request.method == "POST":
        if alumnos:
            nuevo_id = max(a["id"] for a in alumnos) + 1
        else:
            nuevo_id = 1

        nuevo = {
            "id": nuevo_id,
            "nombre": request.form["nombre"],
            "edad": request.form["edad"],
            "dni": request.form["dni"],
            "telefono": request.form["telefono"],
            "email": request.form["email"],
            "altura": request.form["altura"],
            "peso": request.form["peso"],
            "objetivo": request.form["objetivo"],
            "plan": request.form["plan"],
            "estado": request.form["estado"],
        }
        alumnos.append(nuevo)
        guardar_alumnos(alumnos)
        return redirect("/alumnos")

    return render_template("formulario_alumno.html", titulo="Agregar Alumno", alumno=None)


@main.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    alumnos = cargar_alumnos()
    alumno = next((a for a in alumnos if a["id"] == id), None)

    if alumno is None:
        return redirect("/alumnos")

    if request.method == "POST":
        alumno["nombre"] = request.form.get("nombre", "")
        alumno["edad"] = request.form.get("edad", "")
        alumno["dni"] = request.form.get("dni", "")
        alumno["telefono"] = request.form.get("telefono", "")
        alumno["email"] = request.form.get("email", "")
        alumno["altura"] = request.form.get("altura", "")
        alumno["peso"] = request.form.get("peso", "")
        alumno["objetivo"] = request.form.get("objetivo", "")
        alumno["plan"] = request.form.get("plan", "")
        alumno["estado"] = request.form.get("estado", "")

        guardar_alumnos(alumnos)
        return redirect("/alumnos")

    return render_template("formulario_alumno.html", titulo="Editar Alumno", alumno=alumno)


@main.route("/eliminar/<int:id>")
def eliminar(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    alumnos = cargar_alumnos()
    alumnos = [a for a in alumnos if a["id"] != id]
    guardar_alumnos(alumnos)
    return redirect("/alumnos")


@main.route("/cuotas")
def cuotas():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    lista = cargar_cuotas()
    buscar = request.args.get("buscar", "")

    if buscar:
        lista = [cuota for cuota in lista if buscar.lower() in cuota["alumno"].lower()]

    return render_template("cuotas.html", cuotas=lista, buscar=buscar)


@main.route("/agregar_cuota", methods=["GET", "POST"])
def agregar_cuota():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    cuotas = cargar_cuotas()
    alumnos = cargar_alumnos()

    if request.method == "POST":
        if cuotas:
            nuevo_id = max(c["id"] for c in cuotas) + 1
        else:
            nuevo_id = 1

        nueva = {
            "id": nuevo_id,
            "alumno": request.form["alumno"],
            "plan": request.form["plan"],
            "monto": request.form["monto"],
            "vencimiento": request.form["vencimiento"],
            "estado": request.form["estado"],
        }

        cuotas.append(nueva)
        guardar_cuotas(cuotas)
        return redirect("/cuotas")

    return render_template("formulario_cuota.html", alumnos=alumnos)


@main.route("/editar_cuota/<int:id>", methods=["GET", "POST"])
def editar_cuota(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    cuotas = cargar_cuotas()
    cuota = next((c for c in cuotas if c["id"] == id), None)

    if cuota is None:
        return redirect("/cuotas")

    if request.method == "POST":
        cuota["alumno"] = request.form.get("alumno", "")
        cuota["plan"] = request.form.get("plan", "")
        cuota["monto"] = request.form.get("monto", "")
        cuota["vencimiento"] = request.form.get("vencimiento", "")
        cuota["estado"] = request.form.get("estado", "")
        guardar_cuotas(cuotas)
        return redirect("/cuotas")

    return render_template("formulario_cuota.html", alumnos=cargar_alumnos(), cuota=cuota)


@main.route("/eliminar_cuota/<int:id>")
def eliminar_cuota(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    cuotas = cargar_cuotas()
    cuotas = [c for c in cuotas if c["id"] != id]
    guardar_cuotas(cuotas)
    return redirect("/cuotas")


@main.route("/rutinas")
def rutinas():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    lista = cargar_rutinas()
    buscar = request.args.get("buscar", "")

    if buscar:
        buscar = buscar.lower()
        lista = [
            r
            for r in lista
            if buscar in r["alumno"].lower()
            or buscar in r["lunes"].lower()
            or buscar in r["martes"].lower()
            or buscar in r["miercoles"].lower()
            or buscar in r["jueves"].lower()
            or buscar in r["viernes"].lower()
        ]

    return render_template("rutinas.html", rutinas=lista, buscar=buscar)


@main.route("/agregar_rutina", methods=["GET", "POST"])
def agregar_rutina():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    rutinas = cargar_rutinas()

    if request.method == "POST":
        if rutinas:
            nuevo_id = max(r["id"] for r in rutinas) + 1
        else:
            nuevo_id = 1

        nueva = {
            "id": nuevo_id,
            "alumno": request.form["alumno"],
            "lunes": request.form["lunes"],
            "martes": request.form["martes"],
            "miercoles": request.form["miercoles"],
            "jueves": request.form["jueves"],
            "viernes": request.form["viernes"],
        }
        rutinas.append(nueva)
        guardar_rutinas(rutinas)
        return redirect("/rutinas")

    return render_template("formulario_rutina.html", titulo="Agregar Rutina", rutina=None, alumnos=cargar_alumnos())


@main.route("/editar_rutina/<int:id>", methods=["GET", "POST"])
def editar_rutina(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    rutinas = cargar_rutinas()
    rutina = next((r for r in rutinas if r["id"] == id), None)

    if rutina is None:
        return redirect("/rutinas")

    if request.method == "POST":
        rutina["alumno"] = request.form.get("alumno", "")
        rutina["lunes"] = request.form.get("lunes", "")
        rutina["martes"] = request.form.get("martes", "")
        rutina["miercoles"] = request.form.get("miercoles", "")
        rutina["jueves"] = request.form.get("jueves", "")
        rutina["viernes"] = request.form.get("viernes", "")
        guardar_rutinas(rutinas)
        return redirect("/rutinas")

    return render_template("formulario_rutina.html", titulo="Editar Rutina", rutina=rutina, alumnos=cargar_alumnos())


@main.route("/eliminar_rutina/<int:id>")
def eliminar_rutina(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    rutinas = cargar_rutinas()
    rutinas = [r for r in rutinas if r["id"] != id]
    guardar_rutinas(rutinas)
    return redirect("/rutinas")


@main.route("/asistencia")
def asistencia():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    lista = cargar_asistencia()
    buscar = request.args.get("buscar", "")

    if buscar:
        lista = [a for a in lista if buscar.lower() in a["nombre"].lower()]

    return render_template("asistencia.html", asistencia=lista, buscar=buscar)


@main.route("/agregar_asistencia", methods=["GET", "POST"])
def agregar_asistencia():
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    asistencia = cargar_asistencia()

    if request.method == "POST":
        if asistencia:
            nuevo_id = max(a["id"] for a in asistencia) + 1
        else:
            nuevo_id = 1

        nuevo = {
            "id": nuevo_id,
            "nombre": request.form["nombre"],
            "fecha": request.form["fecha"],
            "hora": request.form["hora"],
            "estado": request.form["estado"],
        }
        asistencia.append(nuevo)
        guardar_asistencia(asistencia)
        return redirect("/asistencia")

    return render_template("formulario_asistencia.html", titulo="Registrar asistencia", registro=None, alumnos=cargar_alumnos())


@main.route("/editar_asistencia/<int:id>", methods=["GET", "POST"])
def editar_asistencia(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    asistencia = cargar_asistencia()
    registro = next((a for a in asistencia if a["id"] == id), None)

    if registro is None:
        return redirect("/asistencia")

    if request.method == "POST":
        registro["nombre"] = request.form.get("nombre", "")
        registro["fecha"] = request.form.get("fecha", "")
        registro["hora"] = request.form.get("hora", "")
        registro["estado"] = request.form.get("estado", "")
        guardar_asistencia(asistencia)
        return redirect("/asistencia")

    return render_template("formulario_asistencia.html", titulo="Editar asistencia", registro=registro, alumnos=cargar_alumnos())


@main.route("/eliminar_asistencia/<int:id>")
def eliminar_asistencia(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    asistencia = cargar_asistencia()
    asistencia = [a for a in asistencia if a["id"] != id]
    guardar_asistencia(asistencia)
    return redirect("/asistencia")


@main.route("/perfil_alumno/<int:id>")
def perfil_alumno(id):
    redirect_result = requiere_login()
    if redirect_result is not None:
        return redirect_result

    alumnos = cargar_alumnos()
    rutinas = cargar_rutinas()
    asistencias = cargar_asistencia()
    alumno = next((a for a in alumnos if a["id"] == id), None)

    if alumno is None:
        return redirect("/alumnos")

    imc = None
    estado_imc = "Sin datos"

    try:
        peso = float(alumno["peso"])
        altura = float(alumno["altura"])

        if altura > 3:
            altura = altura / 100

        if altura > 0:
            imc = round(peso / (altura ** 2), 2)

            if imc < 18.5:
                estado_imc = "Bajo peso"
            elif imc < 25:
                estado_imc = "Peso normal"
            elif imc < 30:
                estado_imc = "Sobrepeso"
            else:
                estado_imc = "Obesidad"
    except Exception:
        pass

    rutina = next((r for r in rutinas if r["alumno"] == alumno["nombre"]), None)
    asistencias_alumno = [a for a in asistencias if a["nombre"] == alumno["nombre"]]

    return render_template(
        "perfil_alumno.html",
        alumno=alumno,
        rutina=rutina,
        asistencias=asistencias_alumno,
        imc=imc,
        estado_imc=estado_imc,
    )
