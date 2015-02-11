import db
from textblob import TextBlob
from TwitterSearch import TwitterSearch
from data.models import Tweet


def main():
    twitter_api = TwitterSearch("val")
    searchTag = "#superbowl"
    placeID = twitter_api.getTwitterPlaceID("USA", "country")

    endid = ""
    for i in xrange(10):
        results = twitter_api.getTweets(searchTag, placeID=placeID, end_id=endid)

        for tweet in results["tweets"]:
            sent = TextBlob(tweet["text"])

            Tweet.objects.create(hashtag=searchTag, created_at=tweet["datetime"], polarity=sent.polarity, subjectivity=sent.subjectivity, lat=tweet["coordinates"][1], lng=tweet["coordinates"][0])
        endid = results["low"]
        print results

#main()

Tweet.objects.all().delete()
print Tweet.objects.all().count()
