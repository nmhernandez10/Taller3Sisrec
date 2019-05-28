import datetime
import json
import time
from csv import reader

import numpy as np
import pandas as pd
import requests


class Ontological:

    graphJsonRoute = '../graph/graph.json'

    def __init__(self):

        self.graph = {}
        with open(self.graphJsonRoute) as json_file:
            self.graph = json.load(json_file)

    def predict(self, fromId):

        return self.graph[fromId]


if __name__ == "__main__":
    cb = Ontological()
    print(cb.predict("1"))
