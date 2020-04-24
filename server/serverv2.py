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
from base64 import b64encode
from aligner import align_sequence

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
        try:
            id = None
            global counter
            with counter.get_lock():
                id = counter.value
                counter.value += 1
            parser = reqparse.RequestParser()
            parser.add_argument("sequence", required = True)
            parser.add_argument("sens", required = True)
            parser.add_argument("num_matches", required = True)

            args = parser.parse_args()
            seq = args["sequence"]
            sens = float(args["sens"])
            num_matches = int(args["num_matches"])
            # data["sequence"].append(seq)
            logging.info("Seq " + seq + " with id " + str(id) + " from ip " +request.remote_addr)
            parse(seq, id)
            process(id, seq)
            p = Process(target=predict(id))
            p.start()
            # print("started")
            p.join()
            # print("joined")
            # predict(id)
            dot_bracket_string = to_string(id)
            print(dot_bracket_string)
            aligned_dot = align_sequence(seq, dot_bracket_string, sens, num_matches)
            file1 = open("./pics/"+str(id)+"_pred.png", "rb")
            img1 = file1.read()
            file2 = open("./pics/"+str(id)+"_binarized.png", "rb")
            img2 = file2.read()
            # resp = make_response(json.dumps(id), 200)
            resp = make_response(json.dumps({"id": id, "seq" : aligned_dot, "raw_dot" : dot_bracket_string, "img1" : b64encode(img1).decode('utf-8'),\
             "img2" : b64encode(img2).decode('utf-8')}), 200)
            # id+=1
            resp.headers.extend({'Access-Control-Allow-Headers' : '*','Access-Control-Allow-Credentials': 'true','Access-Control-Allow-Origin' : '*'})
            return resp
        except Exception as e:
            print(e)
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
