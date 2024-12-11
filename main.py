import pandas as pd
from flask import Flask, url_for, jsonify, send_file, send_from_directory
import os
import plotly.express as px

app = Flask(__name__, static_folder='src/static')

# Datos JSON directamente en el backend
data = [
    {
        "title": "Beneficios de la Energía Solar",
        "description": "La energía solar reduce las emisiones de carbono y es sostenible.",
        "benefits": [
            "No contamina",
            "Es renovable",
            "Es económica",
            "Es autóctona",
            "Ayuda a crear empleo",
            "Tiene mantenimiento reducido",
            "Se puede utilizar en diferentes usos",
            "Recurso inagotable"
        ],
        "image": "static/images/Beneficios-energia-solar.jpg"
    },
    {
        "title": "Paneles Solares",
        "description": "Los paneles solares convierten la luz solar en electricidad.",
        "image": "/static/images/panel_solar.jpg"
    },
    {
        "title": "Futuro Sostenible",
        "description": "Un futuro limpio es posible con tecnologías renovables.",
        "image": "/static/images/Futuro_sostenible.jpeg"
    }
]

# Ruta principal
@app.route('/')
def index():
    return send_file('src/index.html')

# Ruta para archivos estáticos
@app.route('/static/<path:path>')
def static_files(path):
    return url_for('static', path)

# Ruta para devolver los datos JSON
@app.route('/data')
def get_data():
    return jsonify(data)

# Ruta para cargar datos desde el archivo CSV
@app.route("/cargarfuentedatos")
def cargarfuentedatos():
    with open("solarshareenergy.csv", "r") as archivo:   # Abrir el archivo y preparar variables
        mitabla = "<table id='t_datos' class='table table-hover'>"
        mitabla += "<thead>"
        mitabla += "    <tr>"
        mitabla += "        <th>País</th>"
        mitabla += "        <th>Código</th>"
        mitabla += "        <th>Año</th>"
        mitabla += "        <th>Ahorro</th>"
        mitabla += "    </tr>"
        mitabla += "</thead>"
        mitabla += "<tbody>"
        paises = set()  # Usaremos un conjunto para evitar duplicados
        for linea in archivo:  # Leer línea por línea el archivo
            elemento = linea.strip().split(",")  # Eliminar espacios y dividir por comas
            paises.add(elemento[0])  # Agregar país al conjunto
            mitabla += "<tr>"
            mitabla += "    <td>" + elemento[0] + "</td>"
            mitabla += "    <td>" + elemento[1] + "</td>"
            mitabla += "    <td>" + elemento[2] + "</td>"
            mitabla += "    <td>" + elemento[3] + "</td>"
            mitabla += "</tr>"
        mitabla += "</tbody></table>"

    # Crear el <select> para los países únicos
    select_paises = "<select id='sl_paises' class='form-control'>"
    for pais in sorted(paises):  # Ordenar los países alfabéticamente
        select_paises += "<option value='" + pais + "'>" + pais + "</option>"
    select_paises += "</select>"

    select_grafico = "<select id='sl_grafico' class='form-control'>"
    select_grafico += "<option value='Linea'>Linea</option>"
    select_grafico += "<option value='Torta'>Torta</option>"
    select_grafico += "<option value='Barras'>Barras</option>"
    select_grafico += "<option value='Area'>Area</option>"
    select_grafico += "</select>"

    todo = "<div class='row'>"
    todo += "<div class='col-md-7'>" + select_paises + "</div>"
    todo += "<div class='col-md-3'>" + select_grafico + "</div>"
    todo += "<div class='col-md-2'><button onclick='mostrarGrafico()' class='btn btn-success'>Graficar</button></div>"
    todo += "</div>"

    return todo + "<hr>" + mitabla

# Ruta para generar gráficos
@app.route('/graficar/<pais>/<grafico>')
def graficar(pais, grafico):
    df = pd.read_csv("shareelectricityrenewables.csv", header=None)     # Cargar el archivo en un DataFrame
    df.columns = ["País", "Código", "Año", "Ahorro"]  # Asegurar nombres de columnas

    # Filtrar los datos por el país proporcionado
    df_filtrado = df[df["País"] == pais]

    if df_filtrado.empty:
        return f"<h3>No hay datos disponibles para el país: {pais}</h3>"

    # Crear el gráfico según el tipo seleccionado
    if grafico == "Linea":
        fig = px.line(df_filtrado,
                      x="Año",
                      y="Ahorro",
                      title=f"Ahorro de energía en {pais} (Línea)",
                      markers=True)
    elif grafico == "Torta":
        # Para un gráfico de torta, usamos un único valor por categoría, ejemplo: total por año
        df_agg = df_filtrado.groupby("Año").sum().reset_index()
        fig = px.pie(df_agg,
                     names="Año",
                     values="Ahorro",
                     title=f"Ahorro de energía en {pais} (Torta)")
    elif grafico == "Barras":
        fig = px.bar(df_filtrado,
                     x="Año",
                     y="Ahorro",
                     title=f"Ahorro de energía en {pais} (Barras)",
                     text_auto=True)
    elif grafico == "Area":
        fig = px.area(df_filtrado,
                      x="Año",
                      y="Ahorro",
                      title=f"Ahorro de energía en {pais} (Área)")
    else:
        return f"<h3>Tipo de gráfico '{grafico}' no reconocido.</h3>"

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)
    print(graph_html)
    return graph_html

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)



