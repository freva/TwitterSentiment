import db
from data.models import Tweet
import json
import socket
from django.db.models import Q

def get_tweets():
	return Tweet.objects.filter(
			Q(hashtag="#fiftyshadesofgrey") |
			Q(hashtag="#50shades") |
			Q(hashtag="#50shadesofgrey") |
			Q(hashtag="#fsog") |
			Q(hashtag="#fiftyshades") |
			Q(hashtag="#mrgreywillseeyounow") |
			Q(hashtag="#mrgrey") |
			Q(hashtag="#fiftyshadesofgreymovie")
		)

def main():
	dictionary = []
	for tweet in get_tweets():
		dictionary.append({"lat":float(tweet.lat), "lng":float(tweet.lng), "polarity":float(tweet.polarity)})

	if '3883' in socket.gethostname():
		with open("/root/TwitterSentiment/map.json", "w+") as output_file:
			json.dump(dictionary, output_file)
	else:
		with open("map.json", "w+") as output_file:
			json.dump(dictionary, output_file)

if __name__ == "__main__":
	main()
