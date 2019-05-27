import json

import requests


class DatabasePopulator:
    genome_scores_file = '../../ml-latest/genome-scores.csv'
    genome_tags_file = '../../ml-latest/genome-tags.csv'
    links_file = '../../ml-latest/links.csv'
    movies_file = '../../ml-latest/movies.csv'
    ratings_file = '../../ml-latest/ratings.csv'
    tag_ids_file = '../../ml-latest/tags_ids_file.json'
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
            index = 0
            genome_tags = genome_tags.readlines()
            header = 0
            for line in genome_tags:
                if header:
                    tag = line.split(',')[1]
                    r = requests.post(self.database_address.format(
                        'tag'), json={'name': tag})

                    if r.status_code >= 300:
                        print("Error in {}".format(index))
                    else:
                        all_tags[tag] = r.json()['id']

                    index += 1
                    if index % 100 == 0:
                        print('Total progress adding tags: {}%'.format(
                            index / len(genome_tags) * 100))
                header = 1

        with open(self.tag_ids_file, 'w', encoding = 'utf-8') as tag_ids:
            tag_ids.write(json.dumps(all_tags))

    def load_movies(self):
        pass

    def load_users(self):
        pass

    def load_reviews(self):
        pass


if __name__ == '__main__':
    databasePopulator = DatabasePopulator()
    databasePopulator.load_tags()
