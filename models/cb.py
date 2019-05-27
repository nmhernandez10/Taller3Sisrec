import datetime
import json
import time
from csv import reader

import numpy as np
import pandas as pd
import requests


class ContentBased:

    businessJsonRoute = '../../yelp_dataset~/business.json'

    businessAttributes = '../../yelp_dataset~/businessAttributes.json'
    businessCategories = '../../yelp_dataset~/businessCategories.json'
    businessTags = '../../yelp_dataset~/businessTags.json'
    businessIndexes = '../../yelp_dataset~/businessIndexes.csv'

    IDFFile = '../../yelp_dataset~/idfVector.csv'
    TFFile = '../../yelp_dataset~/tfVector.csv'
    TFIDFFile = '../../yelp_dataset~/tfIdfMatrix.csv'

    databaseAddress = 'http://127.0.0.1:8080/api/{}'
    userUpdateDatabaseAddress = 'http://127.0.0.1:8080/api/user/{}'
    getUserTagsAddress = 'http://127.0.0.1:8080/api/user/formodel/forcontent'

    def __init__(self):

        self.allTagsList = []
        with open(self.businessTags, 'r', encoding='utf-8') as allTags:
            self.allTagsList = json.load(allTags)

    def predict(self, rawUserTags=[], businessesReviewed=[]):

        userTags = []
        tagRandomizer = 0
        for tag in self.allTagsList:
            if not rawUserTags:
                tagRandomizer += 1
                if tagRandomizer % 10 == 0:
                    userTags.append(-1)
                elif tagRandomizer % 3 == 0:
                    userTags.append(0)
                else:
                    userTags.append(1)
            else:
                if tag in rawUserTags['positive']:
                    userTags.append(1)
                elif tag in rawUserTags['negative']:
                    userTags.append(-1)
                else:
                    userTags.append(0)

        userTags = np.array(userTags, dtype=int)
        userPredictions = np.array([])
        with open(self.TFIDFFile, 'r', encoding='utf-8') as TFIDFFile:
            header = 0
            businessIndex = 0
            for business in TFIDFFile:
                # if businessIndex == 20:
                #     break
                if not header:
                    header = 1
                else:
                    df = np.array(business[:-1].split(',')[1:], dtype=float)
                    predict = np.dot(df, userTags)
                    userPredictions = np.append(userPredictions, predict)

                businessIndex += 1
                if businessIndex % 10000 == 0:
                    print('Loading predictions for user: {}% done.'.format(
                        businessIndex / 158527 * 100))
            print('Normalizing predictions')
            userPredictions = userPredictions / np.max(userPredictions) * 5
            print('Extracting top 5 predictions')
            alreadySeen = len(businessesReviewed)
            topn = np.argpartition(userPredictions, -(4 + alreadySeen))[-(4 + alreadySeen):][::-1]
            for business in businessesReviewed:
                businessS = business - 1
                if businessS in topn:
                    index = np.argwhere(topn == businessS)
                    topn = np.delete(topn, index)

            return ['{}'.format(top+1) for top in topn[:4]]

    def predict_all(self):

        print('Getting all users to update content')
        r = requests.get(self.getUserTagsAddress)
        usersToUpdate = r.json()
        
        # usersToUpdate = [
        #     {
        #         "id": 1,
        #         "names": "Rashmi",
        #         "yelp_id": "l6BmjZMeQD3rDxWUbiAiow",
        #         "email": "l6BmjZMeQD3rDxWUbiAiow",
        #         "password": "l6BmjZMeQD3rDxWUbiAiow",
        #         "image": "https://freeyork.org/wp-content/uploads/2016/09/1pjUBUzNU_Q.jpg",
        #         "top": "24629,69008,5364,104129",
        #         "content_updated": False,
        #         "createdAt": "2019-04-17T20:24:52.998Z",
        #         "updatedAt": "2019-04-21T21:49:42.066Z",
        #         "UserTags": [
        #             {
        #                 "id": 34,
        #                 "like": True,
        #                 "createdAt": "2019-04-21T21:49:40.524Z",
        #                 "updatedAt": "2019-04-21T21:49:40.524Z",
        #                 "TagId": 11,
        #                 "UserId": 1,
        #                 "Tag": {
        #                     "id": 11,
        #                     "name": "Sushi Bars",
        #                     "createdAt": "2019-04-17T18:49:04.198Z",
        #                     "updatedAt": "2019-04-17T18:49:04.198Z"
        #                 }
        #             }
        #         ],
        #         "Reviews": [
        #             {
        #                 "id": 725331,
        #                 "stars": 3,
        #                 "date": "2015-12-04T01:37:32.000Z",
        #                 "svd_updated": True,
        #                 "createdAt": "2019-04-17T23:54:12.377Z",
        #                 "updatedAt": "2019-04-17T23:54:12.377Z",
        #                 "BusinessId": 19,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 725331,
        #                 "stars": 3,
        #                 "date": "2015-12-04T01:37:32.000Z",
        #                 "svd_updated": True,
        #                 "createdAt": "2019-04-17T23:54:12.377Z",
        #                 "updatedAt": "2019-04-17T23:54:12.377Z",
        #                 "BusinessId": 3,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 754564,
        #                 "stars": 5,
        #                 "date": "2015-09-12T19:59:21.000Z",
        #                 "svd_updated": True,
        #                 "createdAt": "2019-04-17T23:55:46.054Z",
        #                 "updatedAt": "2019-04-17T23:55:46.054Z",
        #                 "BusinessId": 86893,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 15116,
        #                 "stars": 2,
        #                 "date": "2015-09-11T03:47:42.000Z",
        #                 "svd_updated": True,
        #                 "createdAt": "2019-04-17T23:16:17.513Z",
        #                 "updatedAt": "2019-04-17T23:16:17.513Z",
        #                 "BusinessId": 1668,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 84206,
        #                 "stars": 5,
        #                 "date": "2015-09-21T08:36:39.000Z",
        #                 "svd_updated": True,
        #                 "createdAt": "2019-04-17T23:19:59.282Z",
        #                 "updatedAt": "2019-04-17T23:19:59.282Z",
        #                 "BusinessId": 10936,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 312403,
        #                 "stars": 5,
        #                 "date": "2015-09-12T21:18:52.000Z",
        #                 "svd_updated": True,
        #                 "createdAt": "2019-04-17T23:32:09.951Z",
        #                 "updatedAt": "2019-04-17T23:32:09.951Z",
        #                 "BusinessId": 41405,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 1456660,
        #                 "stars": 3,
        #                 "date": "2019-04-21T22:01:59.730Z",
        #                 "svd_updated": False,
        #                 "createdAt": "2019-04-21T22:02:00.140Z",
        #                 "updatedAt": "2019-04-21T22:02:00.140Z",
        #                 "BusinessId": 104129,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 1456661,
        #                 "stars": 2,
        #                 "date": "2019-04-21T22:03:38.210Z",
        #                 "svd_updated": False,
        #                 "createdAt": "2019-04-21T22:03:38.932Z",
        #                 "updatedAt": "2019-04-21T22:03:38.932Z",
        #                 "BusinessId": 69008,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 1456663,
        #                 "stars": 2,
        #                 "date": "2019-04-21T22:07:10.580Z",
        #                 "svd_updated": False,
        #                 "createdAt": "2019-04-21T22:07:10.869Z",
        #                 "updatedAt": "2019-04-21T22:07:10.869Z",
        #                 "BusinessId": 5364,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 1456662,
        #                 "stars": 5,
        #                 "date": "2019-04-21T22:08:25.923Z",
        #                 "svd_updated": False,
        #                 "createdAt": "2019-04-21T22:06:40.541Z",
        #                 "updatedAt": "2019-04-21T22:08:26.712Z",
        #                 "BusinessId": 24629,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 1456659,
        #                 "stars": 5,
        #                 "date": "2019-04-21T22:11:12.156Z",
        #                 "svd_updated": False,
        #                 "createdAt": "2019-04-21T21:33:37.531Z",
        #                 "updatedAt": "2019-04-21T22:11:12.936Z",
        #                 "BusinessId": 17415,
        #                 "UserId": 1
        #             },
        #             {
        #                 "id": 1456664,
        #                 "stars": 3,
        #                 "date": "2019-04-21T22:11:32.244Z",
        #                 "svd_updated": False,
        #                 "createdAt": "2019-04-21T22:11:32.515Z",
        #                 "updatedAt": "2019-04-21T22:11:32.515Z",
        #                 "BusinessId": 25,
        #                 "UserId": 1
        #             }
        #         ]
        #     }
        # ]
        for userToUpdate in usersToUpdate:
            userId = userToUpdate['id']
            print('Predicting for user {}.'.format(userId))
            userTags = self.extract_tags(userToUpdate['UserTags'])
            userReviewedBusinesses = self.extract_reviews(userToUpdate['Reviews'])
            
            oldTop = userToUpdate['top']

            top4 = self.predict(rawUserTags=userTags, businessesReviewed=userReviewedBusinesses)
            
            newTop = self.new_top(oldTop, top4)

            print({'top': newTop, 'content_updated': True})

            r = requests.put(
                self.userUpdateDatabaseAddress.format(userId),
                json={'top': newTop, 'content_updated': True})

            if r.status_code >= 300:
                print("Error updating content for user {}".format(userId))

    def new_top(self, oldTop, top4):
        newTop = ''

        if not oldTop:
            for top in top4:
                newTop += ',{}'.format(top) if newTop else '{}'.format(top)
        else:
            oldTopList = oldTop.split(',')
            if len(oldTopList) > 6:
                for top in top4:
                    newTop += ',{}'.format(top) if newTop else '{}'.format(top)
                for top in oldTopList[4:]:
                    newTop += ',{}'.format(top)
            else:
                if '{}'.format(oldTop)[0] == ',':
                    for top in top4:
                        newTop += ',{}'.format(
                            top) if newTop else '{}'.format(top)
                    for top in oldTopList[1:]:
                        newTop += ',{}'.format(top)
                else:
                    for top in top4:
                        newTop += ',{}'.format(
                            top) if newTop else '{}'.format(top)
        return newTop

    def extract_reviews(self, reviews):
        businessIds = []
        for review in reviews:
            businessIds.append(review['BusinessId'])
        return businessIds

    def extract_tags(self, tags):
        userTags = {'positive': [], 'negative': []}
        for tag in tags:
            tagObject = tag['Tag']
            if tag['like']:
                userTags['positive'].append(tagObject['name'])
            else:
                userTags['negative'].append(tagObject['name'])
        return userTags

    def update(self):
        while True:
            self.predict_all()
            time.sleep(30)


if __name__ == "__main__":
    cb = ContentBased()
    cb.update()
