# Aplicacion web Flask que predice el precio sugerido de venta (MSRP) de un automovil.
# Carga el pipeline entrenado y las opciones del formulario, y devuelve la prediccion.
import os
import json
import pandas as pd
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

# Carga una sola vez el pipeline entrenado y las opciones de los menus desplegables.
pipelineModelo = joblib.load("pipeline_msrp.joblib")
with open("opciones.json", "r", encoding="utf-8") as archivoOpciones:
    datosOpciones = json.load(archivoOpciones)
listaMarcas = datosOpciones["opciones"]["Make"]
listaCombustibles = datosOpciones["opciones"]["Engine Fuel Type"]
listaTamanos = datosOpciones["opciones"]["Vehicle Size"]
rangosNumericos = datosOpciones["rangos"]


@app.route("/", methods=["GET", "POST"])
def inicio():
    # Muestra el formulario y, cuando se envia, calcula y muestra la prediccion del precio.
    prediccionTexto = None
    mensajeError = None
    valoresPrevios = {}

    if request.method == "POST":
        try:
            # Lee cada campo del formulario y lo convierte al tipo adecuado.
            potenciaMotor = float(request.form["engine_hp"])
            anioModelo = int(request.form["year"])
            marcaSeleccionada = request.form["make"]
            tipoCombustible = request.form["fuel_type"]
            valorPopularidad = float(request.form["popularity"])
            tamanoVehiculo = request.form["vehicle_size"]
            valoresPrevios = request.form

            # Arma una fila con los nombres de columna EXACTOS que espera el pipeline.
            filaEntrada = pd.DataFrame([{
                "Engine HP": potenciaMotor,
                "Year": anioModelo,
                "Make": marcaSeleccionada,
                "Engine Fuel Type": tipoCombustible,
                "Popularity": valorPopularidad,
                "Vehicle Size": tamanoVehiculo,
            }])

            # Calcula la prediccion y la formatea con separador de miles.
            valorPredicho = float(pipelineModelo.predict(filaEntrada)[0])
            prediccionTexto = "{:,.2f}".format(valorPredicho)
        except Exception:
            mensajeError = "Verifica que todos los campos esten completos y sean validos."

    return render_template(
        "index.html",
        marcas=listaMarcas,
        combustibles=listaCombustibles,
        tamanos=listaTamanos,
        rangos=rangosNumericos,
        prediccion=prediccionTexto,
        error=mensajeError,
        valores=valoresPrevios,
    )


if __name__ == "__main__":
    # Ejecucion local; en Render se usa gunicorn con la variable de entorno PORT.
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
