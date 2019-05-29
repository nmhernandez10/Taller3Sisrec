import datetime
import time

import pandas as pd
import requests
import surprise


class Collaborative:
    reviewCSVRoute = '../../ml-latest/ratings.csv'
    dataset_columns = ['userId', 'movieId', 'rating']

    databaseAddress = 'http://127.0.0.1:8080/api/{}'
    userUpdateDatabaseAddress = 'http://127.0.0.1:8080/api/user/{}'
    getUserNumber = 'http://127.0.0.1:8080/api/user/formodel/count'
    getUserReviews = 'http://127.0.0.1:8080/api/user/formodel/forsvd/{}'

    # getNewReviews = 'http://172.24.101.30:8080/api/review/formodel/forsvdonline/'
    getNewReviews = 'http://127.0.0.1:8080/api/review/formodel/forsvdonline/{}'
    updateReview = 'http://127.0.0.1:8080/api/review/{}'

    def __init__(self, userId):
        self.update_trainset(userId)
        self.create_model()

    def update_trainset(self, userId):
        r = requests.get(self.getNewReviews.format(
            userId))  # Cambiar el endpoint pls
        data = r.json()

        df = pd.DataFrame(data)
        df = df[['UserId', 'MovieId', 'stars']]

        reader = surprise.Reader(rating_scale=(1.0, 5.0))
        data = surprise.Dataset.load_from_df(df, reader)
        full_trainset_temp = data.build_full_trainset()
        self.full_trainset = full_trainset_temp

    def create_model(self):
        print('Building SVD model')
        algo_temp = surprise.SVD(
            n_factors=1, n_epochs=50, lr_all=0.004, reg_all=0.14)
        algo_temp.fit(self.full_trainset)
        self.algorithm = algo_temp

    def get_top_n(self, predictions, n=8):
        top_n = {}
        for uid, iid, _, est, _ in predictions:
            if uid not in top_n:
                top_n[uid] = [(iid, est)]
            else:
                top_n[uid].append((iid, est))

        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n

    def predict(self, user_id, top_n=8):
        """
        Returns all predictions for the given user
        """

        user_ratings = self.full_trainset.ur[self.full_trainset.to_inner_uid(
            user_id)]
        items = self.full_trainset.ir
        items_raw_ids = []

        # Transform inner ids to raw ids
        for item in items:
            item_raw_id = self.full_trainset.to_raw_iid(item)
            items_raw_ids.append(item_raw_id)

        # Predict for the given raw user id, for all raw item ids
        predictions = [self.algorithm.predict(
            user_id, item_id) for item_id in items_raw_ids]

        # Get the top predictions, as a list of item and ratings
        top_n_predictions = self.get_top_n(
            predictions, n=top_n + len(user_ratings))

        # Retrieve only item ids from the given user
        predicted_items = [predicted_item_id for predicted_item_id,
                           predicted_item_rating in top_n_predictions[user_id]]

        # Remove already rated items from the list
        for item_id, _ in user_ratings:
            item_raw_id = self.full_trainset.to_raw_iid(item_id)
            if item_raw_id in predicted_items:
                predicted_items.remove(item_raw_id)

        # Return only 5 items
        return ['{}'.format(top) for top in predicted_items[:top_n]]

    def predict_all(self):
        # for user in users predict(user)
        pass

    def update(self):
        # self.put_ranking()
        self.update()
        self.create_model()
        self.predict_all()


if __name__ == '__main__':
    millis = int(round(time.time() * 1000))
    svd = Collaborative(2)
    print(svd.predict(2))
    millis = int(round(time.time() * 1000)) - millis
    print(millis)
