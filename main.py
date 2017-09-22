# Flask Libs
from flask import Flask
from flask import request
from flask import Response, send_from_directory, render_template, request
from flask_cors import CORS, cross_origin
# System libs
import json
import numpy as np
import sys
import itertools

# Mainlib
from score_regressor import get_best
from newton import Newton
from newton.knn import *

app = Flask(__name__)
CORS(app)
setattr(sys.modules['__main__'],'gower_distance',gower_distance)

sisrec = Newton(np.array([i for i in range(1, 12)]), 'newton/forest/serialized', 'newton/knn/serialized', 'newton/data', 3, 3)



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
            result = {"probability":1 - prediction_model.posterior_cdf(data["query_score"], np.array([data["query_day"], ])),"r_score":prediction_model.score(), "prediction":int(prediction_model.posterior_mean(np.array([data["query_day"], ])))}
            status = 200
        else:
            result ={"r_score":prediction_model.score()}
            status = 422
        #db.conn.close()

    elif request.method == "PUT":
        result = 'PUT request is not allowed'

    resp = Response(json.dumps(result), status=status, mimetype='application/json')
    return resp

@app.route("/get_recommendations",methods=["POST"])
def get_recommendations():
    data = request.get_json(force=True)
    area = data['area_id']
    #scores deberia ser array de arrays
    scores = np.array(data['scores'])
    recs = sisrec.get_recs(area,scores)
    result = build_dict(recs)
    # print(recs)
    # print(result)
    return Response(json.dumps(result), status=200, mimetype='application/json')

@app.route("/get_nn",methods=["POST"])
def get_nn():
    data = request.get_json(force=True)
    careers = np.array(data['carreers'])
    k = data['k']
    nns = sisrec.balltree.query(careers,k)
    result = {'result':{i:[int(x) for x in nns[i]] for i in range(len(careers))}}
    return Response(json.dumps(result), status=200, mimetype='application/json')

# @app.route("/get_classification",methods=["POST"])
# def get_classification():
#
#     return ""


def build_dict(res):
    result = {"result": {}}
    for i in range(res.shape[0]):
        print(res[i])
        result["result"][i] = [int(x) for x in itertools.chain.from_iterable(res[i])]
    return result


@app.errorhandler(404)
def page_not_found(e):
    return "ups! error:404"


if __name__ == "__main__":

    app.run(host="0.0.0.0")
