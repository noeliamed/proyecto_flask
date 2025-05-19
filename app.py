from flask import Flask, render_template, request, abort, redirect, url_for
import json
import os

app = Flask(__name__)

# Configuración definitiva de rutas
def get_json_path():
    # Intenta varias ubicaciones posibles
    possible_paths = [
        os.path.join(app.root_path, 'peliculas.json'),  # Primero busca en raíz
        os.path.join(app.root_path, 'static', 'assets', 'js', 'peliculas.json'),
        os.path.join(app.root_path, 'static', 'peliculas.json')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Si no existe en ninguna ruta, usa la raíz por defecto
    return os.path.join(app.root_path, 'peliculas.json')

# Ruta definitiva del JSON
JSON_PATH = get_json_path()
print(f"Intentando cargar el archivo JSON desde: {JSON_PATH}")

def cargar_peliculas():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Procesamiento flexible de la estructura
            if isinstance(data, dict):
                return data.get('peliculas', [])
            elif isinstance(data, list):
                return data
            else:
                raise ValueError("Formato de archivo no válido")
                
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado en {JSON_PATH}")
        print("Creando archivo JSON vacío...")
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []
    except json.JSONDecodeError:
        print("ERROR: Archivo JSON corrupto o mal formado")
        return []
    except Exception as e:
        print(f"ERROR inesperado: {str(e)}")
        return []

# Carga inicial de datos
todas_las_peliculas = cargar_peliculas()
print(f"Se cargaron {len(todas_las_peliculas)} películas")

# ... [el resto de tu código permanece igual] ...

if __name__ == '__main__':
    app.run(debug=True)
