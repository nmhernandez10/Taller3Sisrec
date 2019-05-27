import datetime
import math
import time

import pandas as pd
import requests
import surprise
from scipy.special import ndtri



class Collaborative:
    reviewCSVRoute = '../../ml-latest/ratings.csv'
    dataset_columns = ['userId', 'movieId', 'rating']

    databaseAddress = 'http://127.0.0.1:8080/api/{}'
    userUpdateDatabaseAddress = 'http://127.0.0.1:8080/api/user/{}'
    getUserNumber = 'http://127.0.0.1:8080/api/user/formodel/count'
    getUserReviews = 'http://127.0.0.1:8080/api/user/formodel/forsvd/{}'
    rankingUser = 409286
    getNewReviews = 'http://127.0.0.1:8080/api/review/formodel/forsvd/'
    updateReview = 'http://127.0.0.1:8080/api/review/{}'

    def __init__(self):
        self.build_trainset()
        self.create_model()

    def build_trainset(self):
        print('Building trainset for collaborative filtering')
        dfcsv = pd.read_csv(self.reviewCSVRoute, header=None,
                            names=self.dataset_columns)
        reader = surprise.Reader(rating_scale=(1.0, 5.0))
        data = surprise.Dataset.load_from_df(dfcsv, reader)
        full_trainset_temp = data.build_full_trainset()
        self.full_trainset = full_trainset_temp

    def update_trainset(self):
        df = pd.DataFrame()
        
        self.userTops = {}
        r = requests.get(self.getNewReviews)
        userData = r.json()
        if not userData:
            return False
        print('Updating trainset for collaborative filtering')
####################
        dfcsv = pd.read_csv(self.reviewCSVRoute, header=None,
                            names=self.dataset_columns)
####################
        newReviews = []
        self.reviewsToUpdate = []
        for r in userData:
            self.reviewsToUpdate.append(r['id'])
            dftemp = dfcsv.loc[dfcsv['movieId'] == r['MovieId']]
            dftemp = dftemp.loc[dfcsv['userId'] == r['UserId']]

            dfcsv.loc[(dfcsv['movieId'] == r['MovieId']) & (
                dfcsv.UserId == r['UserId']), 'rating'] = r['stars']
            user = r['User']
            self.userTops[r['UserId']] = user['top']
            if dftemp.empty:
                newReviews.append(
                    {'UserId': r['UserId'],
                     'BusinessId': r['BusinessId'],
                     'stars': r['stars']})

        df = pd.DataFrame(newReviews)
        df = df[self.dataset_columns]
####################
        dfcsv = dfcsv.append(df, ignore_index=True)

        reader = surprise.Reader(rating_scale=(1.0, 5.0))
        data = surprise.Dataset.load_from_df(dfcsv, reader)
        full_trainset_temp = data.build_full_trainset()
        self.full_trainset = full_trainset_temp
        return True

    def create_model(self):
        print('Building SVD model')
        algo_temp = surprise.SVD(
            n_factors=1, n_epochs=50, lr_all=0.004, reg_all=0.14)
        algo_temp.fit(self.full_trainset)
        self.algorithm = algo_temp

    def get_top_n(self, predictions, n=5):
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

    def predict(self, user_id, top_n=4):
        """
        Returns all predicitions for the given user
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
        for r in self.reviewsToUpdate:
            rr = requests.put(
                self.updateReview.format(r),
                json={'svd_updated': True})

            if rr.status_code >= 300:
                print("Error updating svd_updated for review {}".format(r))

        for u in self.userTops:
            try:
                oldTop = self.userTops[u]
                top4 = self.predict(u)
                newTop = self.new_top(oldTop, top4)
                print('id: {}, newTop: {}'.format(u, newTop))
                r = requests.put(
                    self.userUpdateDatabaseAddress.format(u),
                    json={'top': newTop})

                if r.status_code >= 300:
                    print(
                        "Error updating collaborative predictions for user {}".format(u))
            except:
                print('User has no ratings')

    def new_top(self, oldTop, top4):
        newTop = ''

        if not oldTop:
            for top in top4:
                newTop += ',{}'.format(top)
        else:
            oldTopList = oldTop.split(',')
            if len(oldTopList) > 6:
                for top in oldTopList[:4]:
                    newTop += ',{}'.format(top) if newTop else '{}'.format(top)
                for top in top4:
                    newTop += ',{}'.format(top)
            else:
                if '{}'.format(oldTop)[0] == ',':
                    for top in top4:
                        newTop += ',{}'.format(
                            top)
                else:
                    for top in oldTopList:
                        newTop += ',{}'.format(top) if newTop else '{}'.format(top)
                    for top in top4:
                        newTop += ',{}'.format(
                            top)
        return newTop

    def ranking(self, top_n=8):
        items = self.full_trainset.ir
        items_ranking = {}
        for item in items:
            item_raw_id = self.full_trainset.to_raw_iid(item)
            n = 0
            average = 0
            pos = 0
            for _, rating in items[item]:
                n += 1
                average += rating
            average = average / n
            pos = len(
                [rating for user, rating in items[item] if rating > average])
            confidence = 0.95
            items_ranking[item_raw_id] = self.ci_lower_bound(
                pos, n, confidence)
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
            self.userUpdateDatabaseAddress.format(self.rankingUser),
            json={'top': newTop})

        if r.status_code >= 300:
            print("Error updating ranking")

    def update(self):
        self.put_ranking()
        while True:
            print('Scanning for changes in reviews')
            if self.update_trainset():
                self.create_model()
                self.predict_all()
                print('Getting the general ranking')
                self.put_ranking()
            time.sleep(30)


if __name__ == '__main__':
    svd = Collaborative()
    svd.update()
