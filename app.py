from flask import Flask, render_template, request, abort, redirect, url_for
import json
import os

app = Flask(__name__)

# Configura la ruta del archivo JSON
app.config['JSON_FILE'] = os.path.join(app.root_path, 'static', 'assets', 'js', 'peliculas.json')

# Preprocesar datos para facilitar búsquedas
def preparar_datos():
    try:
        with open(app.config['JSON_FILE'], 'r', encoding='utf-8') as file:
            datos = json.load(file)
            
            # Verificamos si es un diccionario con clave 'peliculas'
            if isinstance(datos, dict) and 'peliculas' in datos:
                peliculas = datos['peliculas']
            else:
                peliculas = datos if isinstance(datos, list) else []
            
            # Creamos objetos película normalizados
            peliculas_procesadas = []
            for idx, pelicula in enumerate(peliculas):
                try:
                    pelicula_procesada = {
                        "id": str(idx),
                        "titulo": pelicula.get("titulo", "Sin título"),
                        "nombre": pelicula.get("titulo", "Sin título"),  # Para compatibilidad
                        "anio": pelicula.get("anio", "Desconocido"),
                        "genero": ", ".join(pelicula["genero"]) if isinstance(pelicula.get("genero"), list) else pelicula.get("genero", "Desconocido"),
                        "director": pelicula["director"]["nombre"] if isinstance(pelicula.get("director"), dict) else pelicula.get("director", "Desconocido"),
                        "duracion": pelicula.get("duracion", "Desconocido"),
                        "sinopsis": pelicula.get("sinopsis", "Sin sinopsis disponible"),
                        "calificacion": pelicula.get("calificacion", "N/A"),
                        "actores": ", ".join([a["nombre"] for a in pelicula["actores"]]) if isinstance(pelicula.get("actores"), list) else "Desconocido",
                        "pais": pelicula.get("pais", "Desconocido"),
                        "premios": f"{pelicula['premios']['Oscar']} Oscars" if isinstance(pelicula.get("premios"), dict) and 'Oscar' in pelicula['premios'] else "Sin premios Oscar"
                    }
                    peliculas_procesadas.append(pelicula_procesada)
                except (KeyError, AttributeError) as e:
                    print(f"Error procesando película {idx}: {str(e)}")
                    continue
            
            return peliculas_procesadas
    
    except FileNotFoundError:
        abort(500, description="Archivo de películas no encontrado")
    except json.JSONDecodeError:
        abort(500, description="Error al leer el archivo JSON")
    except Exception as e:
        abort(500, description=f"Error inesperado: {str(e)}")

# Cargamos los datos al iniciar
todas_las_peliculas = preparar_datos()

@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/inicio')
def inicio():
    return render_template('base.html')

@app.route('/buscador', methods=['GET', 'POST'])
def buscador():
    # Obtener todos los géneros únicos para el dropdown
    generos = sorted({g for p in todas_las_peliculas for g in p["genero"].split(", ")})
    
    # Obtener todos los años únicos
    años = sorted({p["anio"] for p in todas_las_peliculas if p["anio"] != "Desconocido"}, reverse=True)
    
    # Valores por defecto
    resultados = []
    busqueda = ""
    genero_seleccionado = ""
    año_seleccionado = ""
    
    if request.method == 'POST':
        busqueda = request.form.get('nombre', '').lower().strip()
        genero_seleccionado = request.form.get('genero', '')
        año_seleccionado = request.form.get('anio', '')
        
        # Filtrar películas
        resultados = todas_las_peliculas
        
        if busqueda:
            resultados = [p for p in resultados if busqueda in p["titulo"].lower()]
        
        if genero_seleccionado:
            resultados = [p for p in resultados if genero_seleccionado in p["genero"]]
        
        if año_seleccionado:
            resultados = [p for p in resultados if str(p["anio"]) == año_seleccionado]
    
    return render_template('buscador.html',
                         peliculas=resultados,
                         busqueda=busqueda,
                         generos=generos,
                         años=años,
                         genero_seleccionado=genero_seleccionado,
                         año_seleccionado=año_seleccionado)

@app.route('/detalle/<id>')
def detalle(id):
    try:
        pelicula = next((p for p in todas_las_peliculas if p["id"] == id), None)
        if pelicula is None:
            abort(404)
            
        return render_template('detalle.html', pelicula=pelicula)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
