from TwitterSentiment.scraper.models import Tweet
from time import mktime
from math import ceil


def graphHashtags(hashtags, startTime, endTime):
    tweets = [{"polarity": float(t.polarity), "time": int(mktime(t.created_at.timetuple()))}
                      for hashtag in hashtags
                      for t in Tweet.objects.filter(hashtag= hashtag, created_at__gt=startTime, created_at__lt=endTime)]

    startTime = min(tweets, key=lambda l:l["time"])["time"]
    startTime -= startTime%3600
    endTime = max(tweets, key=lambda l:l["time"])["time"]
    endTime += 3600 - (endTime%3600)

    timeDiff = endTime - startTime

    intervals = [900, 1800, 3600, 7200, 14400, 28800, 86400, 259200, 604800, 1209600, 2419200]
    intervalSize = findFirstLargerOrEqual(timeDiff/25, intervals)

    numBins = int(ceil(timeDiff/intervalSize))
    polar, labels = [[] for i in xrange(numBins)], [(startTime+intervalSize*i)*1000 for i in xrange(numBins)]

    for tweet in tweets:
        index = (tweet["time"] - startTime)//intervalSize
        polar[index if index < numBins else -1].append(tweet["polarity"])


    xAxis = {"categories": labels, "labels": {"format": '{value:%e %b %H:%M}'}}
    yAxis = [{"name": "Frequency", "type": "column", "yAxis": 1, "data": [len(pol) for pol in polar]},
             {"name": "Polarity", "type": "spline", "yAxis": 0, "data": [sum(pol)/len(pol) if len(pol)>0 else 0 for pol in polar]}]

    return {"xAxis": xAxis, "yAxis": yAxis}


def findFirstLargerOrEqual(num, sortedList):
    '''Finds the smallest index in the sortedList
    of the element which is greater-than or equal to num'''

    slen = len(sortedList)
    start = 0

    while slen > 0:
        m = start + slen//2

        if sortedList[m] < num:
            slen -= m + 1 - start
            start = m+1
            continue

        if start < m and sortedList[m-1] >= num:
            slen = m - start
            continue

        return sortedList[m]
    return sortedList[-1]

