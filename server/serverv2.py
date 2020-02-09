from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse
from waitress import serve
import json

app = Flask(__name__)
api = Api(app)

data = {
"id" : 0,
"sequence" : []
}
class Neuro(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type = int,  required = True)

        args = parser.parse_args()
        resp = make_response(json.dumps(data["sequence"][args["id"]]), 200)
        resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
        return resp
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("sequence", required = True)

        args = parser.parse_args()
        data["sequence"].append(args["sequence"])
        data["id"]+=1
        resp = make_response(json.dumps(data["id"]-1), 200)
        resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
        return resp
    def options(self):
        resp = make_response(json.dumps(''), 200)
        resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
        return resp

api.add_resource(Neuro, "/neuro")
serve(app, port = 8000)
