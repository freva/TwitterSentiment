import dateutil.parser, time, twitter

CONSUMER_KEY        = 'DtujIqtFFl9Bg18b2WeMTFPwd'
CONSUMER_SECRET     = 'mpDz7M0ZsU9dowCPmIJePxfqrvEFy4moCyCkgzx4UZPrgffyqN'
OAUTH_TOKEN         = '3014396297-AuZwIXKpP9oosXx4XSpbrQ8Pu64QFTdoDVAH9TU'
OAUTH_TOKEN_SECRET  = 'NLWiducniEd2y9lgDFQH9LUg3Lwb6caur0RKmwMcPwCWF'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


def getTweets(query, placeID=None, start_id='', end_id=''):
    if placeID:
        query = query + " place:" + placeID
    search_results = twitter_api.search.tweets(q=query, lang='en', result_type='recent', count=100, since_id=start_id, max_id=end_id)
    statuses, results = search_results['statuses'], []

    print len(statuses),
    for tweet in statuses:
        timestamp = int(time.mktime(dateutil.parser.parse(tweet["created_at"]).timetuple()))
        text = tweet["text"].encode('ascii', errors='ignore').replace('\n', ' ')

        results.append({"id": tweet["id"], "tweetTime": timestamp, "text": text, "coordinates": tweet["coordinates"]["coordinates"]})
    print len(results)
    return {"low": statuses[-1]["id"], "high": statuses[0]["id"], "tweets": results}


def getTwitterPlaceID(query, granularity):
    places = ["poi", "neighborhood", "city", "admin", "country"]
    if granularity not in places:
        raise ValueError("Granularity parameter must be one of ", places)

    places = twitter_api.geo.search(query=query, granularity=granularity)
    return places['result']['places'][0]['id']