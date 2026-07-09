from flask import Flask, render_template, request, redirect, session
import json
import os
import socket

app = Flask(__name__)
app.secret_key = "gymmanager"

# ===============================
# USUARIO DEL SISTEMA
# ===============================

USUARIO = "admin"
CONTRASENA = "1234"

# ===============================
# FUNCIONES JSON
# ===============================

def cargar_alumnos():

    if not os.path.exists("alumnos.json"):
        return []

    with open("alumnos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_alumnos(alumnos):

    with open("alumnos.json", "w", encoding="utf-8") as archivo:
        json.dump(alumnos, archivo, indent=4, ensure_ascii=False)

# ===============================
# CUOTAS
# ===============================

def cargar_cuotas():
    try:
        with open("cuotas.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except:
        return []


def guardar_cuotas(cuotas):
    with open("cuotas.json", "w", encoding="utf-8") as archivo:
        json.dump(cuotas, archivo, indent=4, ensure_ascii=False)

# ===============================
# LISTA DE CUOTAS
# ===============================

@app.route("/cuotas")
def cuotas():

    if "usuario" not in session:
        return redirect("/")

    lista = cargar_cuotas()

    buscar = request.args.get("buscar", "")

    if buscar:
        lista = [
            cuota for cuota in lista
            if buscar.lower() in cuota["alumno"].lower()
        ]

    return render_template(
        "cuotas.html",
        cuotas=lista,
        buscar=buscar
    )
    
# ===============================
# AGREGAR CUOTA
# ===============================

@app.route("/agregar_cuota", methods=["GET", "POST"])
def agregar_cuota():

    if "usuario" not in session:
        return redirect("/")

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
            "estado": request.form["estado"]
        }

        cuotas.append(nueva)
        guardar_cuotas(cuotas)

        return redirect("/cuotas")

    return render_template(
        "formulario_cuota.html",
        alumnos=alumnos
    )


@app.route("/editar_cuota/<int:id>", methods=["GET", "POST"])
def editar_cuota(id):

    if "usuario" not in session:
        return redirect("/")

    cuotas = cargar_cuotas()

    cuota = None

    for c in cuotas:
        if c["id"] == id:
            cuota = c
            break

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

    return render_template(
        "formulario_cuota.html",
        alumnos=cargar_alumnos(),
        cuota=cuota
    )


@app.route("/eliminar_cuota/<int:id>")
def eliminar_cuota(id):

    if "usuario" not in session:
        return redirect("/")

    cuotas = cargar_cuotas()
    cuotas = [c for c in cuotas if c["id"] != id]
    guardar_cuotas(cuotas)
    return redirect("/cuotas")

# ===============================
# LOGIN
# ===============================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        contrasena = request.form["password"]

        if usuario == USUARIO and contrasena == CONTRASENA:

            session["usuario"] = usuario

            return redirect("/inicio")

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos."
        )

    return render_template("login.html")

# ===============================
# INICIO
# ===============================

@app.route("/inicio")
def inicio():

    if "usuario" not in session:
        return redirect("/")

    alumnos = cargar_alumnos()
    rutinas = cargar_rutinas()
    asistencias = cargar_asistencia()

    # Últimos 5 alumnos agregados
    ultimos_alumnos = alumnos[-5:]

    # Últimas 5 asistencias
    ultimas_asistencias = asistencias[-5:]

    return render_template(
        "inicio.html",
        cantidad=len(alumnos),
        cantidad_rutinas=len(rutinas),
        cantidad_asistencia=len(asistencias),
        cantidad_cuotas=0,
        ultimos_alumnos=ultimos_alumnos[::-1],
        ultimas_asistencias=ultimas_asistencias[::-1]
    )
# ===============================
# CERRAR SESIÓN
# ===============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ===============================
# LISTA DE ALUMNOS
# ===============================

@app.route("/alumnos")
def alumnos():

    if "usuario" not in session:
        return redirect("/")

    lista = cargar_alumnos()

    buscar = request.args.get("buscar", "")

    if buscar:

        lista = [

            alumno for alumno in lista

            if buscar.lower() in alumno["nombre"].lower()

        ]

    return render_template(

        "alumnos.html",

        alumnos=lista,

        buscar=buscar

    )

# ===============================
# AGREGAR ALUMNO
# ===============================

@app.route("/agregar", methods=["GET", "POST"])
def agregar():

    if "usuario" not in session:
        return redirect("/")

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

         "estado": request.form["estado"]

      }

        alumnos.append(nuevo)

        guardar_alumnos(alumnos)

        return redirect("/alumnos")
    return render_template(
        "formulario_alumno.html",
        titulo="Agregar Alumno",
        alumno=None
    )
    
# ===============================
# RUTINAS JSON
# ===============================

def cargar_rutinas():

    if not os.path.exists("rutinas.json"):
        return []

    with open("rutinas.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_rutinas(rutinas):

    with open("rutinas.json", "w", encoding="utf-8") as archivo:
        json.dump(rutinas, archivo, indent=4, ensure_ascii=False)

# ===============================
# EDITAR ALUMNO
# ===============================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if "usuario" not in session:
        return redirect("/")

    alumnos = cargar_alumnos()

    alumno = None

    for a in alumnos:

        if a["id"] == id:
            alumno = a
            break

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

    return render_template(

        "formulario_alumno.html",

        titulo="Editar Alumno",

        alumno=alumno

    )

# ===============================
# ELIMINAR ALUMNO
# ===============================

@app.route("/eliminar/<int:id>")
def eliminar(id):

    if "usuario" not in session:
        return redirect("/")

    alumnos = cargar_alumnos()

    alumnos = [a for a in alumnos if a["id"] != id]

    guardar_alumnos(alumnos)

    return redirect("/alumnos")


# ===============================
# RUTINAS
# ===============================

@app.route("/rutinas")
def rutinas():

    if "usuario" not in session:
        return redirect("/")

    lista = cargar_rutinas()

    buscar = request.args.get("buscar","")

    if buscar:

        buscar = buscar.lower()

        lista = [
         r for r in lista
         if buscar in r["alumno"].lower()
            or buscar in r["lunes"].lower()
         or buscar in r["martes"].lower()
            or buscar in r["miercoles"].lower()
            or buscar in r["jueves"].lower()
         or buscar in r["viernes"].lower()
      ]

    return render_template(

        "rutinas.html",

        rutinas=lista,

        buscar=buscar

    )

# AGREGAR RUTINAS

@app.route("/agregar_rutina", methods=["GET", "POST"])
def agregar_rutina():

    if "usuario" not in session:
        return redirect("/")

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

           "viernes": request.form["viernes"]

        }

        rutinas.append(nueva)

        guardar_rutinas(rutinas)

        return redirect("/rutinas")

    return render_template(

        "formulario_rutina.html",

     titulo="Agregar Rutina",

     rutina=None,

     alumnos=cargar_alumnos()

    )

# EDITAR RUTINAS

@app.route("/editar_rutina/<int:id>", methods=["GET", "POST"])
def editar_rutina(id):

    if "usuario" not in session:
        return redirect("/")

    rutinas = cargar_rutinas()

    rutina = None

    for r in rutinas:

        if r["id"] == id:
            rutina = r
            break

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

    return render_template(

     "formulario_rutina.html",

      titulo="Editar Rutina",

     rutina=rutina,

      alumnos=cargar_alumnos()

    )
    
#ELIMINAR RUTINAS

@app.route("/eliminar_rutina/<int:id>")
def eliminar_rutina(id):

    if "usuario" not in session:
        return redirect("/")

    rutinas = cargar_rutinas()

    rutinas = [r for r in rutinas if r["id"] != id]

    guardar_rutinas(rutinas)

    return redirect("/rutinas")

# ===============================
# ASISTENCIA
# ===============================

@app.route("/asistencia")
def asistencia():

    if "usuario" not in session:
        return redirect("/")

    lista = cargar_asistencia()

    buscar = request.args.get("buscar","")

    if buscar:

        lista = [

            a for a in lista

            if buscar.lower() in a["nombre"].lower()

        ]

    return render_template(

        "asistencia.html",

        asistencia=lista,

        buscar=buscar

    )

# ===============================
# ASISTENCIA JSON
# ===============================

def cargar_asistencia():

    if not os.path.exists("asistencia.json"):
        return []

    with open("asistencia.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_asistencia(asistencia):

    with open("asistencia.json", "w", encoding="utf-8") as archivo:
        json.dump(asistencia, archivo, indent=4, ensure_ascii=False)

# AGREGAR

@app.route("/agregar_asistencia", methods=["GET","POST"])
def agregar_asistencia():

    if "usuario" not in session:
        return redirect("/")

    asistencia = cargar_asistencia()

    if request.method == "POST":

        if asistencia:
            nuevo_id = max(a["id"] for a in asistencia)+1
        else:
            nuevo_id = 1

        nuevo = {

            "id":nuevo_id,

            "nombre":request.form["nombre"],

            "fecha":request.form["fecha"],

            "hora":request.form["hora"],

            "estado":request.form["estado"]

        }

        asistencia.append(nuevo)

        guardar_asistencia(asistencia)

        return redirect("/asistencia")

    return render_template(

    "formulario_asistencia.html",

    titulo="Registrar asistencia",

    registro=None,

    alumnos=cargar_alumnos()

)
    
#EDITAR
@app.route("/editar_asistencia/<int:id>", methods=["GET","POST"])
def editar_asistencia(id):

    if "usuario" not in session:
        return redirect("/")

    asistencia = cargar_asistencia()

    registro = None

    for a in asistencia:

        if a["id"] == id:

            registro = a

            break

    if registro is None:
        return redirect("/asistencia")

    if request.method == "POST":

        registro["nombre"] = request.form.get("nombre", "")
        registro["fecha"] = request.form.get("fecha", "")
        registro["hora"] = request.form.get("hora", "")
        registro["estado"] = request.form.get("estado", "")

        guardar_asistencia(asistencia)

        return redirect("/asistencia")

    return render_template(

    "formulario_asistencia.html",

    titulo="Editar asistencia",

    registro=registro,

    alumnos=cargar_alumnos()

)
    
#ELIMINAR

@app.route("/eliminar_asistencia/<int:id>")
def eliminar_asistencia(id):

    if "usuario" not in session:
        return redirect("/")

    asistencia = cargar_asistencia()

    asistencia = [

        a for a in asistencia

        if a["id"] != id

    ]

    guardar_asistencia(asistencia)

    return redirect("/asistencia")

@app.route("/perfil_alumno/<int:id>")
def perfil_alumno(id):

    if "usuario" not in session:
        return redirect("/")

    alumnos = cargar_alumnos()

    rutinas = cargar_rutinas()

    asistencias = cargar_asistencia()

    alumno = next((a for a in alumnos if a["id"] == id), None)
        # ======================
    # CALCULAR IMC
    # ======================

    imc = None
    estado_imc = "Sin datos"

    try:
        peso = float(alumno["peso"])
        altura = float(alumno["altura"])

        # Si la altura está en centímetros, la pasamos a metros
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

    except:
        pass

    if alumno is None:
        return redirect("/alumnos")

    rutina = next(

        (r for r in rutinas if r["alumno"] == alumno["nombre"]),

        None

    )

    asistencias_alumno = [

        a for a in asistencias

        if a["nombre"] == alumno["nombre"]

    ]

    return render_template(
        "perfil_alumno.html",
      alumno=alumno,
     rutina=rutina,
     asistencias=asistencias_alumno,
     imc=imc,
     estado_imc=estado_imc
    )
# ===============================
# EJECUTAR
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    
