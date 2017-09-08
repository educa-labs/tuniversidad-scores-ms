# Flask Libs
from flask import Flask
from flask import request
from flask import Response, send_from_directory, render_template, request
from flask_cors import CORS, cross_origin
# System libs
import json
import datetime
# Mainlib
from score_regressor import get_best

app = Flask(__name__)
CORS(app)

@app.route("/get_prediction", methods = ["GET", "POST", "PUT"])
def get_predicition():
    # Para evitar problemas con Chrome
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # Data viene en formato json -> {}
    # {uid}

    if request.method == "GET":
        result = 'GET request is not allowed'

    elif request.method == "POST":
        # Diccionario de data que viene en el request
        data = request.get_json(force=True)
        #token = request.headers["authorization"]
        # Verificar autenticacion
        # Instancia de base de datos
        #db = DB()

        prediction = get_best(data["dates"], data["scores"])
        # Variables de Retorno
        result = prediction
        status = 200

        #db.conn.close()

    elif request.method == "PUT":
        result = 'PUT request is not allowed'

    resp = Response(json.dumps(result), status=status, mimetype='application/json')
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return "Nice try motherfucker"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
