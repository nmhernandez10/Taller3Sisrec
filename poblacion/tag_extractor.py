import json


class TagExtractor:
    genome_scores_file = '../../ml-latest/genome-scores.csv'
    genome_tags_file = '../../ml-latest/genome-tags.csv'
    movies_tags_file = '../../ml-latest/movies-attributes.json'
    movies_tags_values_file = '../../ml-latest/movies-attributes-values.json'
    movies_file = '../../ml-latest/movies.csv'
    all_tags_file = '../../ml-latest/all-tags.csv'

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

    def define_tags(self):
        all_movies_tags = {}
        all_movies_tags_values = {}
        with open(self.movies_tags_file, 'w', encoding='utf-8') as movie_tags:
            movie_tags.write('')

        average_tags = 0
        number_of_movies = 0
        with open(self.genome_scores_file, 'r', encoding='utf-8') as genome_scores:
            index = 0
            header = 0
            last_movie_id = -1
            genome_scores = genome_scores.readlines()
            print(len(genome_scores))
            for line in genome_scores[1:]:
                # if index == 100:
                #     break
                # if header:
                genome_score = line.split(',')
                movie_id = genome_score[0]
                tag_id = genome_score[1]
                score = genome_score[2][:-1]
                if last_movie_id != movie_id:
                    if last_movie_id != -1:
                        average_tags += len(all_movies_tags[last_movie_id])
                        number_of_movies += 1
                    last_movie_id = movie_id
                    
                try:
                    if float(score) >= 0.65:
                        all_movies_tags[movie_id].append(tag_id)
                        all_movies_tags_values[movie_id][tag_id] = float(score)
                except:
                    all_movies_tags[movie_id] = []
                    all_movies_tags_values[movie_id] = {}
                    if float(score) >= 0.65:
                        all_movies_tags[movie_id].append(tag_id)
                        all_movies_tags_values[movie_id][tag_id] = float(score)
                try:
                    all_movies_tags[movie_id]
                    all_movies_tags_values[movie_id]
                except:
                    all_movies_tags[movie_id] = []
                    all_movies_tags_values[movie_id] = {}

                index += 1
                header = 1

                if index % 500000 == 0:
                    print('Reading genome scores file: {:.2f}% done.'.format(
                        index/len(genome_scores)*100))
        # print(movies)
        print(average_tags/number_of_movies)

        movies_genres = {}
        movies_genres_values = {}
        with open(self.movies_file, 'r', encoding='utf-8') as movies:
            index = 0
            header = 0
            movies = movies.readlines()
            print(len(movies))
            for line in movies[1:]:
                # if index == 2:
                #     break
                # if header:
                movie_info = line.split(',')

                movie_id = movie_info[0]
                movie_genres = movie_info[-1][:-1].split('|')
                movies_genres[movie_id] = [self.genre_ids[name]
                                            for name in movie_genres]
                movies_genres_values[movie_id] = {}
                for name in movie_genres:
                    movies_genres_values[movie_id][self.genre_ids[name]] = 1

                try:
                    for movie_tag in all_movies_tags[movie_id]:
                        movies_genres[movie_id].append(movie_tag)
                        movies_genres_values[movie_id][movie_tag] = all_movies_tags_values[movie_id][movie_tag]
                except:
                    print('The movie with id {} is not present in the list of movies'.format(movie_id))

                header = 1
                index += 1
                if index % 10000 == 0:
                    print('Reading movies file to fetch genres: {:.2f}% done.'.format(
                        index/len(movies)*100))

        # print(movies_genres)
        with open(self.movies_tags_file, 'w', encoding='utf-8') as movies_tags:
            movies_tags.write(json.dumps(movies_genres))

        with open(self.movies_tags_values_file, 'w', encoding='utf-8') as movies_tags_values:
            movies_tags_values.write(json.dumps(movies_genres_values))

    def append_tag_ids(self):
        with open(self.genome_tags_file, 'r', encoding='utf-8') as genome_tags:
            genome_tags = genome_tags.readlines()
            with open(self.all_tags_file, 'w', encoding='utf-8') as all_tags:
                all_tags.write('')
                for line in genome_tags:
                    genome_tag = line.split(',')
                    all_tags.write('{},{}'.format(genome_tag[0], genome_tag[1]))
                for genre in self.genre_ids:
                    all_tags.write('{},{}\n'.format(self.genre_ids[genre], genre))

if __name__ == '__main__':
    tagExtractor = TagExtractor()
    # tagExtractor.append_tag_ids()
    tagExtractor.define_tags()
