from flask import Flask, render_template, request  
import json
import os

app = Flask(__name__)  

JSON_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'js', 'peliculas.json')

@app.route('/buscador')
def buscador():
    return render_template('buscador.html')

@app.route('/resultados', methods=['POST'])
def buscar_peliculas():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            peliculas = json.load(f)
        
        busqueda = request.form['nombre'].lower()
        resultados = [p for p in peliculas if busqueda in p['titulo'].lower()]
        
        return render_template('buscador.html', 
                            resultados=resultados,
                            busqueda=busqueda)
    
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
