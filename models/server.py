from onto import Ontological
from svd import Collaborative
from flask import Flask, Response, make_response, jsonify
from flask_restful import Api, Resource, reqparse
import requests

import json

app = Flask(__name__)
api = Api(app)

userUpdateDatabaseAddress = 'http://172.24.41.67:8080/api/user/{}'

cb = Ontological()

class SVD(Resource):
    def get(self, uid):
        print('Retrieving SVD for user '+uid)
        collaborative_model = Collaborative(uid)
        ranking = collaborative_model.predict(uid)
        r = requests.put(userUpdateDatabaseAddress.format(uid), json = {'topsvd': ranking})
        if(r.ok):
            print(ranking + ' for SVD user ' + uid)
        else:
            print('Error for SVD user '+ uid)
        resp = Response(json.dumps(ranking), status=200, content_type='application/json')
        return resp

class Graph(Resource):
    def get(self, uid):
        print('Retrieving ONTO for user '+uid)
        ranking = cb.predict_for_user(uid)
        r = requests.put(userUpdateDatabaseAddress.format(uid), json = {'toponto': ranking})
        if(r.ok):
            print(ranking + ' for ONTO user ' + uid)
        else:
            print('Error for ONTO user '+ uid)
        resp = Response(json.dumps(ranking), status=200, content_type='application/json')
        return resp

api.add_resource(Graph, "/ontological/<int:uid>")
api.add_resource(SVD, "/collaborative/<int:uid>")
print('Models server on 0.0.0.0:8081')
app.run(host='0.0.0.0', port=8081, debug=False)
