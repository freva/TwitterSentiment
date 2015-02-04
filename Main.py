from textblob import TextBlob
from TwitterSearch import getTweets, getTwitterPlaceID
import db
from data.models import Tweet
from datetime import datetime



def main():
    searchTag = "#obama"
    placeID = getTwitterPlaceID("USA", "country")

    endid = ""
    for i in xrange(10):
        results = getTweets(searchTag, placeID=placeID, end_id=endid)

        for tweet in results["tweets"]:
            sent = TextBlob(tweet["text"])

            Tweet.objects.create(hashtag=searchTag, created_at=datetime.fromtimestamp(tweet["tweetTime"]), polarity=sent.polarity, subjectivity=sent.subjectivity, x=tweet["coordinates"][0], y=tweet["coordinates"][1])
        endid = results["low"]
        print results

print Tweet.objects.all().count()

