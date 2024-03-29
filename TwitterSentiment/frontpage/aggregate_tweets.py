from TwitterSentiment.scraper.models import Tweet
from math import sqrt, pow, log
import random
import time

class JsonConverter(object):
    @staticmethod
    def doCluster(results):
        while True:
            clusters = []
            for result in results:
                JsonConverter.addCluster(result, clusters)

            if clusters == results:
                return clusters
            results = clusters


    @staticmethod
    def addCluster(result, clusters):
        for cluster in clusters:
            if JsonConverter.overlap(result, cluster):
                numObjects1, numObjects2 = len(cluster["polarity"]), len(result["polarity"])
                cluster["lat"] = (cluster["lat"]*numObjects1 + result["lat"]*numObjects2)/(numObjects1 + numObjects2)
                cluster["lng"] = (cluster["lng"]*numObjects1 + result["lng"]*numObjects2)/(numObjects1 + numObjects2)
                cluster["polarity"].extend(result["polarity"])
                return
        clusters.append(result)


    @staticmethod
    def overlap(obj1, obj2):
        dist = sqrt(pow(obj1["lat"]-obj2["lat"], 2) + pow(obj1["lng"]-obj2["lng"], 2))
        return dist - 0.25*(log(len(obj1["polarity"])+2) + log(len(obj2["polarity"])+2)) < 0


    @staticmethod
    def searchHashtags(hashtags, startTime, endTime):
        dictionary = [{"lat": float(t.lat), "lng": float(t.lng), "polarity": [(float(t.polarity), t.tweet_id, t.text, int(time.mktime(t.created_at.timetuple())))]}
                      for hashtag in hashtags
                      for t in Tweet.objects.filter(hashtag= hashtag, created_at__gt=startTime, created_at__lt=endTime)]

        results =  JsonConverter.doCluster(dictionary)
        for t in results:
            groups = [[], [], []]

            for pol, tweetID, tweetText, tweetTime in t["polarity"]:
                out = {"tweetID": tweetID, "tweetText": tweetText, "tweetTime": tweetTime, "tweetPolarity": pol}
                if pol < -0.2:
                    groups[0].append(out)
                elif pol < 0.2:
                    groups[1].append(out)
                else:
                    groups[2].append(out)

            t["count"] = len(t["polarity"])
            t["polarity"] = [0.1+len(group) for group in groups]
            t["ids"] = [sorted(group, key=lambda l:l["tweetTime"], reverse=True)[:4] for group in groups]

        return results

