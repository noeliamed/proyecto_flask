from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Ruta al JSON
JSON_PATH = os.path.join(app.root_path, 'assets', 'js', 'peliculas.json')

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/buscador')
def buscador():
    return render_template('buscador.html')

@app.route('/listaxxxs', methods=['POST'])
def buscar():
    # Obtener término de búsqueda
    busqueda = request.form.get('nombre', '').lower()
    
    # Leer archivo JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        peliculas = json.load(f)
    
    # Filtrar resultados
    resultados = [p for p in peliculas if 
                 busqueda in p['titulo'].lower() or 
                 busqueda in p['director'].lower()]
    
    return render_template('buscador.html', 
                         resultados=resultados,
                         busqueda=busqueda)

if __name__ == '__main__':
    app.run(debug=True)
