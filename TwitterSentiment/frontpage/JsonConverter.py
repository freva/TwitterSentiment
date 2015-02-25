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
        return dist - 0.15*(log(len(obj1["polarity"])+2) + log(len(obj2["polarity"])+2)) < 0


    @staticmethod
    def searchHashtags(hashtags):
        dictionary = [{"lat": float(t.lat), "lng": float(t.lng), "polarity": [float(t.polarity)]}
                      for hashtag in hashtags
                      for t in Tweet.objects.filter(hashtag= hashtag)]

        #results = JsonConverter.doCluster([t for t in dictionary if t["polarity"][0] < 0]) + JsonConverter.doCluster([t for t in dictionary if t["polarity"][0] >= 0])
        results = JsonConverter.doCluster(dictionary)
        results = [{"lat": t["lat"], "lng": t["lng"], "count": len(t["polarity"]),
                    "polarity": sum(t["polarity"])/len(t["polarity"]),
                    "variance": sum([i*i for i in t["polarity"]])/len(t["polarity"])}
                    for t in results]
        return results

