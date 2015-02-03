from textblob import TextBlob
import dateutil.parser, time, twitter

CONSUMER_KEY = 'DtujIqtFFl9Bg18b2WeMTFPwd'
CONSUMER_SECRET ='mpDz7M0ZsU9dowCPmIJePxfqrvEFy4moCyCkgzx4UZPrgffyqN'
OAUTH_TOKEN = '3014396297-AuZwIXKpP9oosXx4XSpbrQ8Pu64QFTdoDVAH9TU'
OAUTH_TOKEN_SECRET = 'NLWiducniEd2y9lgDFQH9LUg3Lwb6caur0RKmwMcPwCWF'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

search_results = twitter_api.search.tweets(q='#Obama', lang='en', result_type='recent', count=100, max_id='')
statuses = search_results['statuses']

for tweet in statuses:
    timestamp = int(time.mktime(dateutil.parser.parse(tweet["created_at"]).timetuple()))
    text = tweet["text"].encode('ascii',errors='ignore').replace('\n', ' ')
    score = TextBlob(text)

    print tweet["user"]["id"], timestamp, score.polarity, score.subjectivity, text