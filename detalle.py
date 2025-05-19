{% extends "base.html" %}

{% block content %}
<div class="container my-5">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <div class="card bg-dark text-white">
                <div class="row no-gutters">
                    <!-- Sección de imagen simplificada -->
                    <div class="col-md-4">
                        <div class="card-img-container">
                            <img src="{{ url_for('static', filename='assets/img/peliculas/' + pelicula.imagen + '.jpg') }}" 
                                 class="card-img"
                                 alt="{{ pelicula.titulo }}"
                                 onerror="this.style.display='none'; document.getElementById('default-poster').style.display='block'">
                            <div id="default-poster" class="default-poster" style="display: none;">
                                <i class="fas fa-film fa-5x"></i>
                                <p>Imagen no disponible</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Sección de detalles -->
                    <div class="col-md-8">
                        <div class="card-body">
                            <h1 class="card-title">{{ pelicula.titulo }} <small class="text-muted">({{ pelicula.anio }})</small></h1>
                            
                            <div class="mb-3">
                                {% for genero in pelicula.genero %}
                                <span class="badge bg-danger me-1">{{ genero }}</span>
                                {% endfor %}
                            </div>
                            
                            <p class="card-text"><strong>Director:</strong> {{ pelicula.director.nombre }} ({{ pelicula.director.nacionalidad }})</p>
                            <p class="card-text"><strong>Duración:</strong> {{ pelicula.duracion }} minutos</p>
                            <p class="card-text"><strong>Calificación:</strong> 
                                {% if pelicula.calificacion %}
                                {{ pelicula.calificacion }}/10
                                {% else %}
                                No disponible
                                {% endif %}
                            </p>
                            
                            <h4 class="mt-4">Sinopsis</h4>
                            <p class="card-text">{{ pelicula.sinopsis }}</p>
                            
                            <h4 class="mt-4">Reparto Principal</h4>
                            <ul class="list-unstyled">
                                {% for actor in pelicula.actores %}
                                <li><strong>{{ actor.nombre }}</strong> como {{ actor.personaje }}</li>
                                {% endfor %}
                            </ul>
                            
                            <h4 class="mt-4">Datos de Producción</h4>
                            <p><strong>Presupuesto:</strong> ${{ "{:,}".format(pelicula.presupuesto) }}</p>
                            <p><strong>Ingresos:</strong> ${{ "{:,}".format(pelicula.ingresos) }}</p>
                            
                            <h4 class="mt-4">Premios</h4>
                            <p><strong>Oscars ganados:</strong> {{ pelicula.premios.Oscar }}</p>
                            <p><strong>Nominaciones:</strong> {{ pelicula.premios.Nominaciones }}</p>
                        </div>
                    </div>
                </div>
                <div class="card-footer bg-transparent">
                    <a href="{{ url_for('buscador') }}" class="btn btn-outline-light">
                        <i class="fas fa-arrow-left"></i> Volver al buscador
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
