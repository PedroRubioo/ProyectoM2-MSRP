# Despliegue en Render - Predictor de precio (MSRP)

Aplicacion web en Flask que predice el precio sugerido de venta (MSRP) de un automovil
a partir de seis caracteristicas: Engine HP, Year, Make, Engine Fuel Type, Popularity y Vehicle Size.

## Archivos
- app.py                  -> aplicacion Flask
- templates/index.html    -> formulario web
- pipeline_msrp.joblib    -> pipeline entrenado (preprocesamiento + RandomForest)
- opciones.json           -> valores de los menus desplegables y rangos
- requirements.txt        -> dependencias con versiones fijas
- URL_Render.txt          -> URL publica de la aplicacion

## Probar en local
1. python -m venv venv
2. Activar el entorno (Windows: venv\Scripts\activate)
3. pip install -r requirements.txt
4. python app.py
5. Abrir http://localhost:5000

## Publicar en Render
1. Subir esta carpeta a un repositorio de GitHub.
2. En render.com: New + -> Web Service -> conectar el repositorio.
3. Configuracion:
   - Environment: Python 3
   - Build Command:  pip install -r requirements.txt
   - Start Command:  gunicorn app:app --bind 0.0.0.0:$PORT
4. Crear el servicio y esperar el despliegue.
5. Copiar la URL publica y colocarla en URL_Render.txt, en la libreta y en el PDF.
