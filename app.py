import os
from flask import Flask, render_template, request, abort, redirect, url_for
import json

app = Flask(__name__)
# Hacer que 'os' esté disponible en todas las plantillas
app.jinja_env.globals['os'] = os
# Obtener la ruta absoluta al directorio actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'peliculas.json')

# Cargar el JSON
with open(JSON_PATH, encoding="utf-8") as f:
    datos = json.load(f)

def preparar_datos():
    peliculas = []
    for pelicula in datos["peliculas"]:
        try:
            pelicula_completa = {
                "id": pelicula["titulo"].lower().replace(" ", "-"),
                "titulo": pelicula.get("titulo", "Sin título"),
                "anio": pelicula.get("anio", "Año desconocido"),
                "genero": pelicula.get("genero", []),
                "director": {
                    "nombre": pelicula.get("director", {}).get("nombre", "Director desconocido"),
                    "nacionalidad": pelicula.get("director", {}).get("nacionalidad", "Nacionalidad desconocida")
                },
                "duracion": pelicula.get("duracion", 0),
                "actores": pelicula.get("actores", []),
                "sinopsis": pelicula.get("sinopsis", "Sin sinopsis disponible"),
                "calificacion": pelicula.get("calificacion", 0.0),
                "presupuesto": pelicula.get("presupuesto", 0),
                "ingresos": pelicula.get("ingresos", 0),
                "premios": {
                    "Oscar": pelicula.get("premios", {}).get("Oscar", 0),
                    "Nominaciones": pelicula.get("premios", {}).get("Nominaciones", 0)
                }
            }
            peliculas.append(pelicula_completa)
        except Exception as e:
            print(f"Error procesando película: {str(e)}")
            continue
    return peliculas
# Preparamos los datos al iniciar
todas_las_peliculas = preparar_datos()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    return redirect(url_for("buscador"))

@app.route("/peliculas", methods=["GET", "POST"])
def buscador():
    # Obtener todos los géneros únicos para el dropdown
    generos = sorted({genero for pelicula in todas_las_peliculas for genero in pelicula["genero"]})
    
    # Valores por defecto
    resultados = []
    busqueda = ""
    genero_seleccionado = ""
    
    if request.method == "POST":
        busqueda = request.form.get("nombre", "").lower()
        genero_seleccionado = request.form.get("genero", "")
        
        # Filtrar películas
        resultados = todas_las_peliculas
        if busqueda:
            resultados = [p for p in resultados if busqueda in p["titulo"].lower()]
        if genero_seleccionado:
            resultados = [p for p in resultados if genero_seleccionado in p["genero"]]
    
    return render_template("buscador.html", 
                         peliculas=resultados, 
                         busqueda=busqueda,
                         generos=generos,
                         genero_seleccionado=genero_seleccionado)

@app.route("/pelicula/<id>")
def detalle(id):
    pelicula = next((p for p in todas_las_peliculas if p["id"] == id), None)
    if pelicula is None:
        abort(404)
    return render_template("detalle.html", pelicula=pelicula)



if __name__ == "__main__":
    app.run(debug=True)
