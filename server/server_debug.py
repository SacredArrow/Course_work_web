from flask import Flask, make_response, request
from flask_restful import Api, Resource, reqparse
from waitress import serve
from multiprocessing import Value, Process
import json
import logging
from my_parser import parse
from network import predict
from postprocessor import process
from serializer import to_string
import tracemalloc
tracemalloc.start()
s1=None
s2=None

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.INFO)

# data = {
# "id" : 0,
# "sequence" : []
# }
counter = Value('i', 0)

class Neuro(Resource):
    # def get(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("id", type = int,  required = True)
    #
    #     args = parser.parse_args()
    #     resp = make_response(json.dumps(to_string(args["id"])), 200)
    #     resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
    #
    #     return resp
    def post(self):
        global s1, s2
        id = None
        global counter
        with counter.get_lock():
            id = counter.value
            counter.value += 1
        parser = reqparse.RequestParser()
        parser.add_argument("sequence", required = True)
        parser.add_argument("trace", required = True)

        args = parser.parse_args()
        seq = args["sequence"]
        trace = args["trace"]
        # data["sequence"].append(seq)
        logging.info("Seq " + seq + " with id " + str(id) + " from ip " +request.remote_addr)
        parse(seq, id)
        process(id, seq)
        p = Process(target=predict(id))
        p.start()
        print("started")
        p.join()
        print("joined")
        # predict(id)

        if trace == 's2':
            s2=tracemalloc.take_snapshot()
            for i in s2.compare_to(s1,'lineno')[:10]:
                print(i)
        elif trace == 's1':
            s1=tracemalloc.take_snapshot()

        # resp = make_response(json.dumps(id), 200)
        resp = make_response(json.dumps({"id": id, "seq" : to_string(id)}), 200)
        # id+=1
        resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
        return resp
        resp = make_response(json.dumps({"id": id, "seq" : "Error"}), 200)
        resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
        return resp

    def options(self):
        resp = make_response(json.dumps(''), 200)
        resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
        return resp

api.add_resource(Neuro, "/neuro")

if __name__ == "__main__":
    serve(app, port = 8000)
