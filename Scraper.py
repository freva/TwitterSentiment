import db
from data.models import Tweet
from textblob import TextBlob
from TwitterSearch import TwitterSearch


class Scraper(object):
    def __init__(self, twitterSearch, query):
        self.twitter_search = twitterSearch
        self.query = query
        self.endID = ""


    def load_endid(self):
        try:
            with open('state.txt', 'r') as input_file:
                self.endID = input_file.read().strip()
        except IOError:
            print "Could not read endid =("


    def save_endid(self):
        with open('state.txt', 'w+') as output_file:
            output_file.write(str(self.endID))


    def run(self):
        self.load_endid()
        placeID = self.twitter_search.getTwitterPlaceID("USA", "country")

        for i in xrange(10):
            results = self.twitter_search.getTweets(self.query, placeID=placeID, end_id=self.endID)

            for tweet in results["tweets"]:
                sent = TextBlob(tweet["text"])

                Tweet.objects.create(hashtag=self.query, created_at=tweet["datetime"], polarity=sent.polarity,
                                     subjectivity=sent.subjectivity, lat=tweet["coordinates"][1], lng=tweet["coordinates"][0])
            self.endID = results["low"]
        self.save_endid()


def main():
    for user in ["jon", "oyv", "val"]:
        scraper = Scraper(TwitterSearch(user), "#obama")
        scraper.run()


if __name__ == "__main__":
    main()
