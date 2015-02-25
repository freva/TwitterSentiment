import json
from TwitterSentiment.scraper.models import Tweet

# with open('tweets.json', 'r') as f:
# 	d = json.loads(f.read())

# for x, i in enumerate(d, 0):
# 	# print d[x]['pk']
# 	# d[x]['pk'] = d[x]['pk'] + 10000
# 	d[x]['model'] = 'scraper.tweet'

# with open('tweets.json', 'w+') as f:
# 	json.dump(d, f)

# with open('')


# 		with open(self.filename, "w+") as output_file:
# 			json.dump(self.dictionary, output_file)

# def loadtweets():
# 	with open('tweets.json', 'r') as f:
# 		d = json.loads(f.read())

# 	for t in d[:2]:
# 		print t['fields']

def load():
	with open('/root/TwitterSentiment/tweets.json', 'r') as f:
		d = json.loads(f.read())

	for i, e in enumerate(d, 0):
		e = e['fields']
		t = Tweet(id=i+1)

		try:
			t.tweet_id = e['tweet_id']
		except:
			pass

		try:
			t.hashtag = e['hashtag']
		except:
			pass

		try:
			t.created_at = e['created_at']
		except:
			pass

		try:
			t.retweet_count = e['retweet_count']
		except:
			pass

		try:
			t.favorite_count = e['favorite_count']
		except:
			pass

		try:
			t.lat = e['lat']
		except:
			pass

		try:
			t.lng = e['lng']
		except:
			pass

		try:
			t.state = e['state']
		except:
			pass

		try:
			t.city = e['city']
		except:
			pass

		try:
			t.subjectivity = e['subjectivity']
		except:
			pass

		try:
			t.polarity = e['polarity']
		except:
			pass

		t.save()
