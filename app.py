from flask import Flask, render_template, request, redirect, url_for, abort
import json
import os

app = Flask(__name__)

# Corregir ruta del JSON (sin 'static')
JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'js', 'peliculas.json')

@app.route('/')
def home():
    return redirect(url_for('buscador'))

@app.route('/buscador')
def buscador():
    return render_template('buscador.html')

@app.route('/resultados', methods=['POST'])
def resultados():
    try:
        if not os.path.exists(JSON_PATH):
            return "Error: Archivo JSON no encontrado", 500
            
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            peliculas = json.load(f)
            
        busqueda = request.form.get('nombre', '').lower()
        
        if busqueda:
            resultados = [p for p in peliculas if p['titulo'].lower().startswith(busqueda)]
        else:
            resultados = peliculas
        
        return render_template('resultados.html',
                            resultados=resultados,
                            busqueda=busqueda)
                            
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/pelicula/<id>')
def detalle_pelicula(id):
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            peliculas = json.load(f)
            
        pelicula = next((p for p in peliculas if str(p.get('id')) == str(id)), None)
        
        if pelicula is None:
            abort(404)
            
        return render_template('detalle.html', pelicula=pelicula)
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
