import io

class UserExtractor:
    ratings_file = '../../ml-latest/ratings.csv'
    users_file = '../../ml-latest/users.csv'

    def extract_users(self):
        with io.open(self.ratings_file, 'r', encoding='utf-8') as ratings:
            ratings = ratings.readlines()
            current_user = -1
            user_count = 0
            for line in ratings[1:]:
                rating = line.split(',')
                new_user = rating[0]
                if new_user != current_user:
                    current_user = new_user
                    user_count += 1
            print(user_count)
                


if __name__ == '__main__':
    user_extractor = UserExtractor()
    user_extractor.extract_users()