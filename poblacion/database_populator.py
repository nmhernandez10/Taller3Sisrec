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
            index = 1
            genome_tags = genome_tags.readlines()
            header = 0
            for line in genome_tags[1:]:
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
        images.append('https://images.pexels.com/photos/162354/harris-hawk-hawk-harris-bird-162354.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/507410/pexels-photo-507410.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1005012/pexels-photo-1005012.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/143580/pexels-photo-143580.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/690800/pexels-photo-690800.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1309902/pexels-photo-1309902.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/53442/birkenau-auschwitz-concentration-camp-53442.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/417202/pexels-photo-417202.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/346796/pexels-photo-346796.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1111597/pexels-photo-1111597.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/236243/pexels-photo-236243.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/4827/nature-forest-trees-fog.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/917494/pexels-photo-917494.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/459225/pexels-photo-459225.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1125776/pexels-photo-1125776.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/326055/pexels-photo-326055.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/814499/pexels-photo-814499.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/247431/pexels-photo-247431.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2274018/pexels-photo-2274018.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1320602/pexels-photo-1320602.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/54320/rose-roses-flowers-red-54320.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/378371/pexels-photo-378371.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1213447/pexels-photo-1213447.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/266958/pexels-photo-266958.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/89773/wolf-wolves-snow-wolf-landscape-89773.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/397857/pexels-photo-397857.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/162389/lost-places-old-decay-ruin-162389.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/316681/pexels-photo-316681.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1270184/pexels-photo-1270184.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/673862/pexels-photo-673862.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/289367/pexels-photo-289367.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/40748/ghosts-gespenter-spooky-horror-40748.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/259591/pexels-photo-259591.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/461763/pexels-photo-461763.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/534590/pexels-photo-534590.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/992731/pexels-photo-992731.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/638701/pexels-photo-638701.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1552173/pexels-photo-1552173.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1441460/pexels-photo-1441460.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/262333/pexels-photo-262333.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/264791/pexels-photo-264791.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1440476/pexels-photo-1440476.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/402028/pexels-photo-402028.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1134166/pexels-photo-1134166.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/46253/mt-fuji-sea-of-clouds-sunrise-46253.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1829980/pexels-photo-1829980.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/301614/pexels-photo-301614.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1822605/pexels-photo-1822605.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2187605/pexels-photo-2187605.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/290604/pexels-photo-290604.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/380707/pexels-photo-380707.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2070047/pexels-photo-2070047.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1455964/pexels-photo-1455964.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1487952/pexels-photo-1487952.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/724216/pexels-photo-724216.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/776538/pexels-photo-776538.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1149831/pexels-photo-1149831.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/120049/pexels-photo-120049.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/337909/pexels-photo-337909.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/34514/spot-runs-start-la.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/33703/relay-race-competition-stadium-sport.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1594932/pexels-photo-1594932.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2190188/pexels-photo-2190188.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/551593/pexels-photo-551593.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1564896/pexels-photo-1564896.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/341378/pexels-photo-341378.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1564828/pexels-photo-1564828.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/267885/pexels-photo-267885.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/7096/people-woman-coffee-meeting.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1106468/pexels-photo-1106468.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/532860/pexels-photo-532860.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/316080/pexels-photo-316080.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/404313/pexels-photo-404313.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1055068/pexels-photo-1055068.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/68389/pexels-photo-68389.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1059078/pexels-photo-1059078.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/460659/pexels-photo-460659.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2199486/pexels-photo-2199486.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2181111/pexels-photo-2181111.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2246648/pexels-photo-2246648.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/92129/pexels-photo-92129.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/685674/pexels-photo-685674.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/220201/pexels-photo-220201.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/216692/pexels-photo-216692.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2156/sky-earth-space-working.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/335908/pexels-photo-335908.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/752614/pexels-photo-752614.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2018360/pexels-photo-2018360.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/62307/air-bubbles-diving-underwater-blow-62307.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/932638/pexels-photo-932638.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2170473/pexels-photo-2170473.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/580871/pexels-photo-580871.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1631768/pexels-photo-1631768.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1395306/pexels-photo-1395306.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1619981/pexels-photo-1619981.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/247115/pexels-photo-247115.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/949590/pexels-photo-949590.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/206274/pexels-photo-206274.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/415307/pexels-photo-415307.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1327446/pexels-photo-1327446.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2294362/pexels-photo-2294362.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2015287/pexels-photo-2015287.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/36487/above-adventure-aerial-air.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1328891/pexels-photo-1328891.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/825876/pexels-photo-825876.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1331978/pexels-photo-1331978.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1626481/pexels-photo-1626481.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/6966/abstract-music-rock-bw.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/167092/pexels-photo-167092.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1389429/pexels-photo-1389429.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/63703/pexels-photo-63703.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/164821/pexels-photo-164821.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/265672/pexels-photo-265672.png?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1005324/literature-book-open-pages-1005324.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/135033/pexels-photo-135033.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/326097/pexels-photo-326097.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/145911/pexels-photo-145911.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1599452/pexels-photo-1599452.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1000529/pexels-photo-1000529.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1680214/pexels-photo-1680214.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2317904/pexels-photo-2317904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/37859/sailing-ship-vessel-boat-sea-37859.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/875858/pexels-photo-875858.png?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1323550/pexels-photo-1323550.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/6272/wood-free-wooden-home.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/2101187/pexels-photo-2101187.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/843226/pexels-photo-843226.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/884788/pexels-photo-884788.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1266808/pexels-photo-1266808.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/37349/rose-beautiful-beauty-bloom.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1406866/pexels-photo-1406866.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1335971/pexels-photo-1335971.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/65894/peacock-pen-alluring-yet-lure-65894.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/887764/pexels-photo-887764.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/887764/pexels-photo-887764.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        images.append('https://images.pexels.com/photos/1212045/pexels-photo-1212045.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')

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
            for line in movies[1:100]:
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
        for user in range(1, 100):#user_count + 1):
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
                        print("Error in uid: {} - mid: {}".format(user_id, movie_db_id))

                    # print({'UserId': user_id, 'MovieId': movie_id, 'date': timestamp, 'stars': rating_score})

                index += 1
                if index % 1000000 == 0:
                    print('Posting ratings: {:.2f}% done.'.format(
                        index/len(ratings)*100))


if __name__ == '__main__':
    databasePopulator = DatabasePopulator()
    databasePopulator.load_tags()
    databasePopulator.load_movies()
    databasePopulator.load_users()
    databasePopulator.load_reviews()
