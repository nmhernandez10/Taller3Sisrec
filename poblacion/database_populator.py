import json
import re
import requests
import io
import random
from datetime import datetime


class DatabasePopulator:
    genome_scores_file = '../../ml-latest/genome-scores.csv'
    genome_tags_file = '../../ml-latest/genome-tags.csv'
    links_file = '../../ml-latest/links.csv'
    movies_file = '../../ml-latest/movies.csv'
    movies_tags_file = '../../ml-latest/movies-attributes.json'
    ratings_file = '../../ml-latest/ratings.csv'
    nodes_file = '../../ml-latest/salida_nodos.csv'

    actors_file = '../../ml-latest/movies-actors.json'
    directors_file = '../../ml-latest/movies-directors.json'

    movie_indexes_file = '../../ml-latest/movies-indexes.csv'

    database_address = 'http://127.0.0.1:8080/api/{}'
    # database_address = 'http://172.24.101.30:8085/api/{}'

    genre_ids = {'Action': 1129,
                 'Adventure': 1130,
                 'Animation': 1131,
                 'Children': 1132,
                 'Comedy': 1133,
                 'Crime': 1134,
                 'Documentary': 1135,
                 'Drama': 1136,
                 'Fantasy': 1137,
                 'Film-Noir': 1138,
                 'Horror': 1139,
                 'Musical': 1140,
                 'Mystery': 1141,
                 'Romance': 1142,
                 'Sci-Fi': 1143,
                 'Thriller': 1144,
                 'War': 1145,
                 'Western': 1146,
                 'IMAX': 1147,
                 '(no genres listed)': 1148
                 }

    def load_tags(self):
        all_tags = {}
        with open(self.genome_tags_file, 'r', encoding='utf-8') as genome_tags:
            index = 1021
            genome_tags = genome_tags.readlines()
            header = 0
            for line in genome_tags[1020:]:
                if header:
                    # if index == 300:
                    #     break
                    tag = line.split(',')[1]
                    tag = tag[:-1]
                    # print(tag)
                    r = requests.post(self.database_address.format(
                        'tag'), json={'name': tag})

                    if r.status_code >= 300:
                        print(
                            "Error in {}. It's safer to start over, or from this tag.".format(index))
                        print(tag)
                        return
                    else:
                        all_tags[tag] = r.json()['id']

                    index += 1
                    if index % 100 == 0:
                        print('Total progress adding tags: {}%'.format(
                            index / len(genome_tags) * 100))
                header = 1

        for tag in self.genre_ids:
            r = requests.post(self.database_address.format(
                'tag'), json={'name': tag})

            if r.status_code >= 300:
                print("Error in {}".format(index))
                print(tag)
                return
            else:
                all_tags[tag] = r.json()['id']
            index += 1

    def load_movies(self):

        images = []
        images.append(
            'https://images.pexels.com/photos/2123337/pexels-photo-2123337.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2103949/pexels-photo-2103949.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1268551/pexels-photo-1268551.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/675951/pexels-photo-675951.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/395134/pexels-photo-395134.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1310777/pexels-photo-1310777.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/299348/pexels-photo-299348.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2059/restaurant-red-beans-coffee.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/62097/pexels-photo-62097.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/299347/pexels-photo-299347.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1566837/pexels-photo-1566837.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/958547/pexels-photo-958547.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1861785/pexels-photo-1861785.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1487511/pexels-photo-1487511.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/842142/pexels-photo-842142.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2425/food-restaurant-fruits-orange.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/629093/pexels-photo-629093.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/302901/pexels-photo-302901.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/6267/menu-restaurant-vintage-table.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/67468/pexels-photo-67468.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/260922/pexels-photo-260922.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/5317/food-salad-restaurant-person.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/724216/pexels-photo-724216.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/697058/pexels-photo-697058.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/670705/pexels-photo-670705.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1148086/pexels-photo-1148086.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1422384/pexels-photo-1422384.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/858508/pexels-photo-858508.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/47546/sushi-eat-japanese-asia-47546.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/277559/pexels-photo-277559.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/347141/pexels-photo-347141.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2079290/pexels-photo-2079290.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/717130/pexels-photo-717130.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/227675/pexels-photo-227675.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/259602/pexels-photo-259602.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/277590/pexels-photo-277590.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2079246/pexels-photo-2079246.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/976876/pexels-photo-976876.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1309897/pexels-photo-1309897.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1102913/pexels-photo-1102913.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/990824/pexels-photo-990824.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/325044/pexels-photo-325044.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/213399/pexels-photo-213399.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1516415/pexels-photo-1516415.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/225869/pexels-photo-225869.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/753267/pexels-photo-753267.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/161989/dolphins-sculpture-statue-architecture-161989.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1000654/pexels-photo-1000654.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1307929/pexels-photo-1307929.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1333737/pexels-photo-1333737.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/736782/pexels-photo-736782.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/726298/pexels-photo-726298.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2132227/pexels-photo-2132227.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/735855/pexels-photo-735855.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2121302/pexels-photo-2121302.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/161212/rio-de-janeiro-olympics-2016-niteroi-brazil-161212.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1959065/pexels-photo-1959065.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/111121/pexels-photo-111121.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1518500/pexels-photo-1518500.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1285625/pexels-photo-1285625.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/164041/pexels-photo-164041.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/984888/pexels-photo-984888.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1283219/pexels-photo-1283219.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/434311/pexels-photo-434311.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/21393/pexels-photo.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1600711/pexels-photo-1600711.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/424725/pexels-photo-424725.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/274249/pexels-photo-274249.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1531672/pexels-photo-1531672.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/327483/pexels-photo-327483.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/784928/pexels-photo-784928.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1009841/pexels-photo-1009841.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/542705/pexels-photo-542705.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1080471/pexels-photo-1080471.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2079439/pexels-photo-2079439.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/375885/pexels-photo-375885.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/941861/pexels-photo-941861.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/374885/pexels-photo-374885.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/305972/pexels-photo-305972.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/544962/pexels-photo-544962.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/442420/books-shelves-architecture-wood-442420.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1290141/pexels-photo-1290141.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1292464/pexels-photo-1292464.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/416510/pexels-photo-416510.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/2090921/pexels-photo-2090921.png?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/64208/pexels-photo-64208.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1435896/pexels-photo-1435896.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/546945/pexels-photo-546945.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/543733/pexels-photo-543733.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1200667/pexels-photo-1200667.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1070985/pexels-photo-1070985.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/808196/pexels-photo-808196.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/209564/pexels-photo-209564.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1662567/pexels-photo-1662567.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/40663/fireworks-rocket-new-year-s-day-new-year-s-eve-40663.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1229841/pexels-photo-1229841.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/327509/pexels-photo-327509.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1012725/pexels-photo-1012725.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/998238/pexels-photo-998238.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/804170/pexels-photo-804170.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/265705/pexels-photo-265705.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1871220/pexels-photo-1871220.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/404159/pexels-photo-404159.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1190829/pexels-photo-1190829.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/932577/pexels-photo-932577.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/264554/pexels-photo-264554.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1002740/pexels-photo-1002740.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/776938/pexels-photo-776938.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/165228/pexels-photo-165228.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1438445/pexels-photo-1438445.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/279260/pexels-photo-279260.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/164763/pexels-photo-164763.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/237718/pexels-photo-237718.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1258935/pexels-photo-1258935.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/1078973/pexels-photo-1078973.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append(
            'https://images.pexels.com/photos/318238/pexels-photo-318238.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')

        all_movies_tags = {}
        with open(self.movies_tags_file, 'r', encoding='utf-8') as movies_tags:
            movies_tags = movies_tags.readlines()
            all_movies_tags = json.loads(movies_tags[0])

        movies_actors = {}
        movies_directors = {}

        all_movies_indexes = {}

        # with io.open(self.nodes_file, 'r', encoding='latin-1') as nodes:
        #     header = 0
        #     index = 1
        #     for line in nodes:
        #         if header:
        #             node = line.split(',')
        #             actors = node[4:-1]
        #             director = node[2]
        #             movie_id = node[0]
        #             empty = 0
        #             for actor in actors:
        #                 if actor == '':
        #                     empty = 1
        #             if director == '':
        #                 empty = 1
        #             if not empty:
        #                 movies_actors[movie_id] = actors
        #                 movies_directors[movie_id] = director
        #                 if index == 57778:
        #                     with open(self.actors_file, 'w', encoding='latin-1') as actors:
        #                         actors.write(json.dumps(movies_actors))
        #                     with open(self.directors_file, 'w', encoding='latin-1') as directors:
        #                         directors.write(json.dumps(movies_directors))
        #         else:
        #             header = 1
        #         index += 1

        with io.open(self.actors_file, 'r', encoding='utf-8') as actors:
            actors = actors.readlines()
            movies_actors = json.loads(actors[0])
        with io.open(self.directors_file, 'r', encoding='utf-8') as directors:
            directors = directors.readlines()
            movies_directors = json.loads(directors[0])

        with io.open(self.movies_file, 'r') as movies:
            movies = movies.readlines()
            misfits = 0
            index = 0
            for line in movies[1:]:
                movie = line.split(',')
                movie_id = movie[0]
                if movie_id in movies_directors:
                    movie_title = movie[1].strip()
                    movie_year = -1
                    weird_titles = line.split('"')
                    if len(weird_titles) > 1:
                        movie_title = weird_titles[1].strip()
                    if len(weird_titles) > 3:
                        movie_title = ''
                        for title_piece in weird_titles[1:-1]:
                            movie_title += title_piece
                        movie_title = movie_title.strip()
                    year = re.search(r"\s\(\d{4}(\W\d{4})?\)", movie_title)
                    if year:
                        year = year.group(0)
                        year = year[2:-1]
                        movie_title = re.sub(
                            r"\s\(\d{4}(\W\d{4})?\)", "", movie_title)
                    else:
                        year = re.search(r"\s\d{4}(\W\d{4})?", movie_title)
                        if year:
                            year = year.group(0)
                            year = year[1:]
                            movie_title = re.sub(
                                r"\s\d{4}(\W\d{4})?", "", movie_title)
                        else:
                            year = re.search(
                                r"\(\d{4}(\W\d{4})?\)", movie_title)
                            if year:
                                year = year.group(0)
                                year = year[2:-1]
                                movie_title = re.sub(
                                    r"\(\d{4}(\W\d{4})?\)", "", movie_title)
                            else:

                                year = re.search(
                                    r"\s\(\d{4}(\W\s)?\)", movie_title)
                                if year:
                                    movie_title = re.sub(
                                        r"\s\(\d{4}(\W\s)?\)", "", movie_title)
                                    year = year.group(0)
                                    year = year[2:-3]
                                else:
                                    year = "-"
                    year = year.strip()
                    movie_title = movie_title.strip()

                    director = movies_directors[movie_id]
                    actors = ''
                    for actor in movies_actors[movie_id]:
                        actors += actor.strip()
                        actors += ','
                    actors = actors[:-1]

                    image = images[random.randint(0, len(images) - 1)]
                    # print(image)
                    # print(actors)
                    # print(director)
                    # print(year)
                    # print(movie_title)

                    r = requests.post(self.database_address.format('movie'),
                                      json={'name': movie_title,
                                            'photo': image,
                                            'year': year,
                                            'director': director,
                                            'actors': actors})
                    print(r)

                    if r.status_code >= 300:
                        print("Error in {}".format(movie_id))
                        print('name: {}'.format(movie_title))
                    else:
                        # all_movies_indexes[movie_id] = r.json()['id']
                        with io.open(self.movie_indexes_file, 'a', encoding='utf-8') as movie_indexes:
                            movie_indexes.write(
                                '{},{}\n'.format(movie_id, r.json()['id']))

                        # print({'name': movie_title,
                        #        'photo': image,
                        #        'year': year,
                        #        'director': director,
                        #        'actors': actors})

                        genres = all_movies_tags[movie_id]
                        for genre in genres:
                            # Add to MovieTags
                            rp = requests.post(self.database_address.format('movietag'),
                                               json={'TagId': genre,
                                                     'MovieId': r.json()['id']})

                            if rp.status_code >= 300:
                                print("Error in {}'s tag {}".format(
                                    movie_id, genre))

                            # print({'TagId': genre, 'MovieId': 'miId'})
                index += 1
                if index % 8000 == 0:
                    print('Reading movies file to post movies and moviestags: {:.2f}% done.'.format(
                        index/len(movies)*100))

    def load_users(self):
        images = []

        images.append(
            'https://www.peluqueriadeloeste.com/wp-content/uploads/2017/09/degradados-para-hombres-4.jpg')
        images.append(
            'https://www.somosmamas.com.ar/wp-content/uploads/2018/10/c28b520926e89d4ed2a9c9a16a65f181-768x1024.jpg')
        images.append('https://pbs.twimg.com/media/DtX77GRXcAELQ7u.jpg')
        images.append(
            'https://www.recreoviral.com/wp-content/uploads/2017/12/los-rostros-m%C3%A1s-atractivos-8.jpg')
        images.append(
            'https://freeyork.org/wp-content/uploads/2016/09/1pjUBUzNU_Q.jpg')
        images.append('https://pbs.twimg.com/media/CSAScbiXAAA6R7v.jpg')
        images.append(
            'https://upload.wikimedia.org/wikipedia/commons/d/d1/Carlos_Cuevas.png')
        images.append(
            'https://www.instyle.es/medio/2015/05/20/instyle_ursula_03_0300_788x1182.jpg')

        user_count = 283228
        for user in range(1, user_count + 1):
            names = user
            email = '{}@gmail.com'.format(user)
            password = user
            image = images[random.randint(0, len(images) - 1)]

            r = requests.post(self.database_address.format('user'),
                              json={'names': names,
                                    'email': email,
                                    'password': password,
                                    'image': image,
                                    'toponto': '',
                                    'topsvd': ''})
            print(r.json())

            if r.status_code >= 300:
                print("Error in {}".format(user))

            # print({'names': names,
            # 'email': email,
            # 'password': password,
            # 'image': image,
            # 'toponto': toponto,
            # 'topsvd': topsvd})

            if user % 10000 == 0:
                print('Creating users: {:.2f}% done.'.format(
                    user/user_count*100))

    def load_reviews(self):
        all_movie_indexes = {}
        with io.open(self.movie_indexes_file, 'r', encoding='utf-8') as movie_indexes:
            for line in movie_indexes:
                movie_index = line.split(',')
                movie_id = movie_index[0]
                db_id = movie_index[1][:-1]
                all_movie_indexes[movie_id] = db_id

        with io.open(self.ratings_file, 'r', encoding='utf-8') as ratings:
            ratings = ratings.readlines()
            index = 0
            for line in ratings[1:]:
                rating = line.split(',')
                movie_id = rating[1]
                if movie_id in all_movie_indexes:
                    user_id = rating[0]
                    rating_score = rating[2]
                    timestamp = rating[3]
                    date = datetime.fromtimestamp(int(timestamp))
                    movie_db_id = all_movie_indexes[movie_id]
                    r = requests.post(self.database_address.format('review'),
                                      json={'UserId': user_id, 
                                      'MovieId': movie_id, 
                                      'date': '{}'.format(date), 
                                      'stars': rating_score})

                    if r.status_code >= 300:
                        print("Error in uid: {}-mid: {}".format(user_id, movie_db_id))

                    # print({'UserId': user_id, 'MovieId': movie_id, 'date': timestamp, 'stars': rating_score})

                index += 1
                if index % 1000000 == 0:
                    print('Posting ratings: {:.2f}% done.'.format(
                        index/len(ratings)*100))


if __name__ == '__main__':
    databasePopulator = DatabasePopulator()
    # databasePopulator.load_tags()
    # databasePopulator.load_movies()
    # databasePopulator.load_users()
    databasePopulator.load_reviews()
