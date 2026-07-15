# Guion de la presentación: GymManager

## 1. Introducción

Buenas tardes. Hoy vamos a explicar una aplicación web llamada GymManager. Esta app está pensada para ayudar a gestionar un gimnasio. La presentación la realizan Anna Bromberg, María Josefina Velázquez Paz y Ángela Romero, para la asignatura Fundamentos de Informática.

## 2. ¿Qué hace la app?

La aplicación permite:
- registrar alumnos
- guardar rutinas
- controlar asistencia
- organizar cuotas

## 3. ¿Con qué se construyó?

Se usaron varias herramientas:
- Python
- Flask
- HTML
- CSS
- JSON

## 4. ¿Cómo se organiza el proyecto?

La app está organizada en varias carpetas para separar responsabilidades:

- app.py: archivo principal que inicia la aplicación y levanta el servidor.
- gymmanager_app/__init__.py: crea la instancia de Flask.
- gymmanager_app/routes.py: define las rutas del sitio, como login, alumnos, rutinas y asistencia.
- gymmanager_app/data.py: contiene la lógica para leer y guardar información en archivos JSON.
- gymmanager_app/config.py: guarda la configuración general de la aplicación.
- templates/: almacena las páginas HTML que se muestran al usuario.
- static/: guarda CSS, archivos multimedia y recursos visuales.

Esta división hace que el código sea más ordenado y fácil de mantener, porque cada parte se encarga de una tarea específica.

## 5. Flujo simple

1. El usuario entra al sistema.
2. Se abre la pantalla de login.
3. Si las credenciales son correctas, entra al dashboard.
4. Allí puede administrar alumnos, rutinas y asistencia.

## 6. Explicación para principiantes

Piensen en la app como una computadora que organiza la información del gimnasio.
No es magia: todo se basa en archivos, formularios y rutas.

## 7. Conclusión

GymManager muestra cómo una idea sencilla puede volverse una aplicación real usando tecnologías básicas. Es un excelente proyecto para aprender web development desde cero.
