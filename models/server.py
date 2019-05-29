from .onto import Ontological
from .svd import Collaborative
from flask import Flask, Response, make_response, jsonify
from flask_restful import Api, Resource, reqparse

import json

app = Flask(__name__)
api = Api(app)

class SVD(Resource):
    def get(self, uid):
        collaborative_model = Collaborative(uid)
        resp = Response(json.dumps(collaborative_model.predict(uid)), status=200, content_type='application/json')
        return resp

class Graph(Resource):
    def get(self, uid):
        resp = Response(json.dumps([1,2,3,4,5,6,7,8]), status=200, content_type='application/json')
        return resp

api.add_resource(SVD, "/ontological/<int:uid>")
api.add_resource(Graph, "/collaborative/<int:uid>")
app.run(host='0.0.0.0', port=8081, debug=False)