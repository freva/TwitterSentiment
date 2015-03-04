from TwitterSentiment.scraper.models import Tweet
from math import sqrt, pow, log

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
    def searchHashtags(hashtags):
        dictionary = [{"lat": float(t.lat), "lng": float(t.lng), "polarity": [float(t.polarity)]}
                      for hashtag in hashtags
                      for t in Tweet.objects.filter(hashtag= hashtag)]

        results =  JsonConverter.doCluster(dictionary)
        return [{"lat": t["lat"], "lng": t["lng"], "count": len(t["polarity"]),
                    "polarity": t["polarity"]} for t in results]


    @staticmethod
    def groupPolarities(tweets):
        for t in tweets:
            groups = [0, 0, 0]
            for pol in t["polarity"]:
                if pol < -0.3:
                    groups[0] += 1
                elif pol < 0.3:
                    groups[1] += 1
                else:
                    groups[2] += 1
            t["polarityDistribution"] = [i/len(t["polarity"]) for i in groups]

        return tweets

