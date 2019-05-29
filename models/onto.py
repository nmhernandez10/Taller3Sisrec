import datetime
import json
import time
from csv import reader

import numpy as np
import pandas as pd
import requests


class Ontological:

    graphJsonRoute = '../graph/graph.json'
    # get_movie_ids = 'http://172.24.101.30:8080/api/movie/formodel/foronto/{}'
    get_movie_ids = 'http://157.253.222.182:8080/api/movie/formodel/foronto/{}'

    def __init__(self):

        self.graph = {}
        with open(self.graphJsonRoute) as json_file:
            self.graph = json.load(json_file)

    def predict(self, from_id):
        return self.graph[from_id]

    def predict_for_user(self, user_id):
        r = requests.get(self.get_movie_ids.format(user_id))        
        movie_list = r.json()
        for movie in movie_list:
            movie_relations = self.predict(movie)
        


if __name__ == "__main__":
    cb = Ontological()
    # print(cb.predict("1"))
    cb.predict_for_user(1)