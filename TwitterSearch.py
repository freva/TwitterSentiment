import dateutil.parser
import twitter


class TwitterSearch:
    def __init__(self, username):
        self.TWITTER_API = TwitterSearch.setUser(username)


    @staticmethod
    def setUser(option):
        if option == "jon":
            OAUTH_TOKEN         = "2321486359-9o9S5F095e9wOcfLF2j9BEVgpCilaT4tJxnAkUJ"
            OAUTH_TOKEN_SECRET  = "FPrE6SifIPOc4Cv4MuiwpKIE2myFmRHKZwPHmwVjtf90t"
            CONSUMER_KEY        = "03wJEEb99nygHwMQWoGeEgiwL"
            CONSUMER_SECRET     = "9u2c2K4V1PLS8eYfjnnFefOIVWhGguztSldNASKYyXcBPSINyL"
        elif option == "oyv":
            OAUTH_TOKEN         = "1149321716-4lUNiaF0bDLieONt2ElPRaoC6n0a9qELFQmzxnL"
            OAUTH_TOKEN_SECRET  = "IC0pwj9GoWjVvYp4rHjYesrgrYpgSFloaNFmMeVNPb4"
            CONSUMER_KEY        = "Hff8xWsJiMpfjoIsUXeWw"
            CONSUMER_SECRET     = "VbUQ3QKrGj8kimKrNo9ZNbioh5VxPMx4KdH8uB7h9cg"
        elif option == "val":
            OAUTH_TOKEN         = "3014396297-AuZwIXKpP9oosXx4XSpbrQ8Pu64QFTdoDVAH9TU"
            OAUTH_TOKEN_SECRET  = "NLWiducniEd2y9lgDFQH9LUg3Lwb6caur0RKmwMcPwCWF"
            CONSUMER_KEY        = "DtujIqtFFl9Bg18b2WeMTFPwd"
            CONSUMER_SECRET     = "mpDz7M0ZsU9dowCPmIJePxfqrvEFy4moCyCkgzx4UZPrgffyqN"
        else:
            raise ValueError("Illegal username")

        auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        return twitter.Twitter(auth=auth)


    def getTweets(self, query, placeID=None, start_id='', end_id=''):
        if placeID:
            query = query + " place:" + placeID
        search_results = self.TWITTER_API.search.tweets(q=query, lang='en', result_type='recent', count=100, since_id=start_id, max_id=end_id)
        statuses, results = search_results['statuses'], []

        print query, end_id
        for tweet in statuses:
            twitterDatetime = dateutil.parser.parse(tweet["created_at"]).date()
            text = tweet["text"].encode('ascii', errors='ignore').replace('\n', ' ')

            results.append({"id": tweet["id"], "datetime": twitterDatetime, "text": text, "coordinates": tweet["coordinates"]["coordinates"]})
        return {"low": statuses[-1]["id"], "high": statuses[0]["id"], "tweets": results}


    def getTwitterPlaceID(self, query, granularity):
        places = ["poi", "neighborhood", "city", "admin", "country"]
        if granularity not in places:
            raise ValueError("Granularity parameter must be one of ", places)

        places = self.TWITTER_API.geo.search(query=query, granularity=granularity)
        return places['result']['places'][0]['id']