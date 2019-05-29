import math

import requests
from scipy.special import ndtri


class Ranking:
    rankingUser = 283230

    user_update_database_address = 'http://127.0.0.1:8080/api/user/{}'
    # user_update_database_address = 'http://157.253.222.182:8080/api/user/{}'
    ratings_file = '../../ml-latest/ratings.csv'

    confidence = 0.95

    def __init__(self):
        print('Creating index for movie ids and database ids')
        self.movie_database_id = {}
        with open('../../ml-latest/movies-indexes.csv', 'r', encoding='utf-8') as movies_indexes:
            for line in movies_indexes:
                movie_index = line.split(',')
                movie_id = movie_index[0]
                db_id = movie_index[1][:-1]
                self.movie_database_id[movie_id] = db_id

        print('Creating n and total rating for every movie')
        self.movie_totals = {}
        with open(self.ratings_file, 'r', encoding='utf-8') as ratings:
            header = 0
            for line in ratings:
                if header:
                    rating = line.split(',')
                    user_id = rating[0]
                    movie_id = rating[1]
                    stars = float(rating[2])
                    if movie_id not in self.movie_totals:
                        self.movie_totals[movie_id] = (1, stars)
                    else:
                        old_n = self.movie_totals[movie_id][0]
                        old_t = self.movie_totals[movie_id][1]
                        new_n = old_n + 1
                        new_t = old_t + stars
                        self.movie_totals[movie_id] = (new_n, new_t)
                else:
                    header = 1
        
        print('Creating average for every movie')
        for movie in self.movie_totals:
            n = self.movie_totals[movie][0]
            t = self.movie_totals[movie][1]
            a = t / n
            self.movie_totals[movie] = (n, a)
    
        print('Creating pos for every movie')
        self.movie_pos = {}
        with open(self.ratings_file, 'r', encoding='utf-8') as ratings:
            header = 0
            for line in ratings:
                if header:
                    rating = line.split(',')
                    user_id = rating[0]
                    movie_id = rating[1]
                    stars = float(rating[2])
                    if movie_id not in self.movie_pos:
                        self.movie_pos[movie_id] = 0
                    average = self.movie_totals[movie_id][1]
                    if stars > average:
                        self.movie_pos[movie_id] += 1
                else:
                    header = 1

        print('Creating a single file with the data from every movie')
        self.movie_parameters = {}
        for movie in self.movie_totals:
            n = self.movie_totals[movie][0]
            p = self.movie_pos[movie]
            self.movie_parameters[movie] = (n, p)

    def ranking(self, top_n=12):
        items_ranking = {}
        print('Getting the complete ranking')
        index = 0
        for movie in self.movie_parameters:
            n = self.movie_parameters[movie][0]
            pos = self.movie_parameters[movie][1]
            items_ranking[movie] = self.ci_lower_bound(
                pos, n, self.confidence)

            index += 1
            if index % 1000 == 0:
                print('Building ranking, {:.2f}% done.'.format(index / 47555 * 100))
        ranking = sorted(items_ranking, key=items_ranking.get, reverse=True)

        return ['{}'.format(r) for r in ranking[:top_n]]

    def ci_lower_bound(self, pos, n, confidence):
        if n == 0:
            return 0
        z = ndtri(1-(1-confidence)/2)
        phat = 1.0*pos/n
        return (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

    def put_ranking(self):
        ranking = self.ranking()
        newTop = ''
        for top in ranking:
            newTop += ',{}'.format(top) if newTop else '{}'.format(top)
        print('Ranking: {}'.format(newTop))
        r = requests.put(
            self.user_update_database_address.format(self.rankingUser),
            json={'toponto': newTop})

        if r.status_code >= 300:
            print("Error updating ranking")

if __name__ == '__main__':
    ranking = Ranking()
    ranking.put_ranking()