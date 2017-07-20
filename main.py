from flask import Flask
from flask import request
from flask import Response, send_from_directory, render_template, request
# from db import DB
import json

app = Flask(__name__)


@app.route("/get_prediction", methods = ["GET", "POST", "PUT"])
def get_predicition():
    # Para evitar problemas con Chrome
    resp.headers['Access-Control-Allow-Origin'] = '*'

    # Diccionario de data que viene en el request
    data = request.get_json(force=True)

    if request.method == "GET":
        result = 'post'

    elif request.method == "POST":
        result = 'post'

    elif request.method == "PUT":
        result = 'put'
    

    # result debe venir como diccionario de python (objeto json)
    resp = Response(json.dumps(result), status=200, mimetype='application/json')
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return "Nice try motherfucker"

if __name__ == "__main__":
    app.run(host="0.0.0.0")