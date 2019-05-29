import datetime
import json
import time
from csv import reader

import numpy as np
import pandas as pd
import requests


class Ontological:

    graph_json_route = '../graph/graph.json'
    # get_movie_ids = 'http://172.24.101.30:8080/api/movie/formodel/foronto/{}'
    # get_movie_ids = 'http://157.253.222.182:8080/api/movie/formodel/foronto/{}'
    get_movie_ids = 'http://127.0.0.1:8080/api/movie/formodel/foronto/{}'
    # get_user_info = 'http://157.253.222.182:8080/api/user/{}'
    get_user_info = 'http://127.0.0.1:8080/api/user/{}'

    complete_ranking_file = '../../ml-latest/ranking.json'
    movie_indexes_file = '../../ml-latest/movies-indexes.csv'
    movies_tags_values_file = '../../ml-latest/movies-attributes-values.json'
    all_tags_file = '../../ml-latest/all-tags.csv'

    def __init__(self):
        self.all_tags = ['{}'.format(i) for i in range(1,1148)]
        # self.all_tags = []
        # with open(self.all_tags_file, 'r', encoding='utf-8') as all_tags:
        #     for line in all_tags:
        #         tag = all_tags.split(',')
        #         self.all_tags.append(tag[0])

        self.movie_values = {}
        with open(self.movies_tags_values_file, 'r', encoding='utf-8') as movies_tags_values:
            self.movie_values = json.load(movies_tags_values)

        self.movie_database_id = {}
        self.movielens_ids = {}
        with open(self.movie_indexes_file, 'r', encoding='utf-8') as movies_indexes:
            for line in movies_indexes:
                movie_index = line.split(',')
                movie_id = movie_index[0]
                db_id = movie_index[1][:-1]
                self.movie_database_id[movie_id] = db_id
                self.movielens_ids[db_id] = movie_id

        self.graph = {}
        with open(self.graph_json_route, 'r', encoding='utf-8') as json_file:
            self.graph = json.load(json_file)
        
        self.ranking = {}
        with open(self.complete_ranking_file, 'r', encoding='utf-8') as complete_ranking:
            self.ranking=json.load(complete_ranking)

    def get_relations(self, from_id):
        from_id = self.movielens_ids['{}'.format(from_id)]
        if from_id in self.graph:
            movie_list = []
            for movie in self.graph[from_id]:
                if movie in self.movie_database_id:
                    movie_list.append(self.movie_database_id[movie])
            return movie_list
        else:
            return ''
    
    def get_user_viewed(self, user_info):
        reviews = user_info['Reviews']
        movie_list = []
        for review in reviews:
            movie_list.append(review['Movie']['id'])
        return movie_list

    def get_user_tags(self, user_info):
        user_tags = {'positive': [], 'negative': []}
        for tag in user_info['UserTags']:
            if tag['like']:
                user_tags['positive'].append(tag['id'])
            else:
                user_tags['negative'].append(tag['id'])
        return user_tags

    def predict_for_user(self, user_id):
        r = requests.get(self.get_movie_ids.format(user_id))        
        movie_list = r.json()
        movie_relations = []
        for movie in movie_list:
            movie_relations = [*movie_relations, *self.get_relations(movie)]

        r = requests.get(self.get_user_info.format(user_id))
        user_info = r.json()
        movies_viewed = self.get_user_viewed(user_info)

        user_tags = self.get_user_tags(user_info)
        return self.predict(raw_user_tags=user_tags, movies_reviewed=movies_viewed, movie_list=movie_relations)

    def predict(self, raw_user_tags=[], movies_reviewed=[], movie_list=[]):
        movie_list = np.array(movie_list)
        userTags = []
        tagRandomizer = 0
        for tag in self.all_tags:
            if not raw_user_tags:
                userTags.append(0)
            else:
                if tag in raw_user_tags['positive']:
                    userTags.append(1)
                elif tag in raw_user_tags['negative']:
                    userTags.append(-1)
                else:
                    userTags.append(0)

        userTags = np.array(userTags, dtype=int)
        userPredictions = np.array([])

        for movie in movie_list:
            if movie in self.movie_values:
                movie_tags = []
                for tag in self.all_tags:
                    if tag in self.movie_values[movie]:
                        movie_tags.append(self.movie_values[movie][tag])
                    else:
                        movie_tags.append(0)
            movie_tags = np.array(movie_tags, dtype=float)
            predict = np.dot(movie_tags, userTags)
            userPredictions = np.append(userPredictions, predict)
            userPredictions = userPredictions / np.max(userPredictions) * 5
            alreadySeen = len(movies_reviewed)
        if len(userPredictions) >= 8 + alreadySeen:
            topnindexes = np.argpartition(userPredictions, -(8 + alreadySeen))[-(8 + alreadySeen):][::-1]
            topn = movie_list[topnindexes]

            for movie in movies_reviewed:
                if movie in topn:
                    index = np.argwhere(topn == movie)
                    topn = np.delete(topn, index)
                    
            return ['{}'.format(top) for top in topn[:8]]
        elif len(userPredictions) >= 8:
            topnindexes = np.argpartition(userPredictions, -8)[-8:][::-1]
            topn = movie_list[topnindexes]
            return ['{}'.format(top) for top in topn[:8]]
        else:
            topnindexes = np.argpartition(userPredictions, -len(userPredictions))[-len(userPredictions):][::-1]
            topn = movie_list[topnindexes]
            return ['{}'.format(top) for top in topn[:len(userPredictions)]]


if __name__ == "__main__":
    cb = Ontological()
    # print(cb.predict("1"))
    cb.predict_for_user(1)