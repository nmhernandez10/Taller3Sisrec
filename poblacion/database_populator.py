import json
import re
import requests


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
        all_movies_tags = {}
        with open(self.movies_tags_file, 'r', encoding='utf-8') as movies_tags:
            movies_tags = movies_tags.readlines()
            all_movies_tags = json.loads(movies_tags[0])
        
        movies_actors = {}
        movies_directors = {}
        with open(self.actors_file, 'r', encoding='utf-8') as actors:
            actors = actors.readlines()
            movies_actors = json.loads(actors[0])
        with open(self.directors_file, 'r', encoding='utf-8') as directors:
            directors = directors.readlines()
            movies_directors = json.loads(directors[0])

        # with open(self.nodes_file, 'r', encoding='ansi', errors='ignore') as nodes:
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
        #                 if index == 58099:
        #                     with open(self.actors_file, 'w', encoding='utf-8') as actors:
        #                         actors.write(json.dumps(movies_actors))
        #                     with open(self.directors_file, 'w', encoding='utf-8') as directors:
        #                         directors.write(json.dumps(movies_directors))
        #         else:
        #             header = 1
        #         index += 1

        with open(self.movies_file, 'r') as movies:
            movies = movies.readlines()
            misfits = 0
            for line in movies[1:]:
                movie = line.split(',')
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
                        movie_title = re.sub(r"\s\d{4}(\W\d{4})?", "", movie_title)
                    else:
                        year = re.search(r"\(\d{4}(\W\d{4})?\)", movie_title)
                        if year:
                            year = year.group(0)
                            year = year[2:-1]
                            movie_title = re.sub(r"\(\d{4}(\W\d{4})?\)", "", movie_title)
                        else:

                            year = re.search(r"\s\(\d{4}(\W\s)?\)", movie_title)
                            if year:
                                movie_title = re.sub(r"\s\(\d{4}(\W\s)?\)", "", movie_title)
                                year = year.group(0)
                                year = year[2:-3]
                            else:
                                year = "-"
                year = year.strip()
                movie_title = movie_title.strip()
                movie_id = movie[0]
                
                # Add to Movies

                genres = all_movies_tags[movie_id]
                for genre in genres:
                    # Add to MovieTags
                    pass
            print(misfits)

    def load_users(self):
        pass

    def load_reviews(self):
        pass


if __name__ == '__main__':
    databasePopulator = DatabasePopulator()
    # databasePopulator.load_tags()
    databasePopulator.load_movies()
