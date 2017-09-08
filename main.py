# Flask Libs
from flask import Flask
from flask import request
from flask import Response, send_from_directory, render_template, request
from flask_cors import CORS, cross_origin
# System libs
import json
import numpy as np

# Mainlib
from score_regressor import get_best

app = Flask(__name__)
CORS(app)

@app.route("/get_prediction", methods = ["GET", "POST", "PUT"])
def get_predicition():
    # Para evitar problemas con Chrome
    #resp.headers['Access-Control-Allow-Origin'] = '*'
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

        prediction_model = get_best(np.array(data["days"]), np.array(data["scores"]))
        # Variables de Retorno
        if prediction_model is not None:
            result = {"probability":1 - prediction_model.posterior_cdf(data["query_score"], np.array([data["query_day"], ])),"r_score":prediction_model.score()}
            status = 200
        else:
            result ={"r_score":prediction_model.score()}
            status = 422
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
