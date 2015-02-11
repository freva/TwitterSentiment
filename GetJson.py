import db
from data.models import Tweet
import json
import socket

def get_tweets(tag):
	tag = "#%s" %(tag)
	return Tweet.objects.filter(hashtag=tag)

def main():
	dictionary = []
	hashtags = [
		"fiftyshadesofgrey",
		"50shades",
		"50shadesofgrey",
		"fsog",
		"fiftyshades",
		"mrgreywillseeyounow",
		"mrgrey",
		"fiftyshadesofgreymovie"
	]
	for tag in hashtags:
		for tweet in get_tweets(tag):
			dictionary.append({"lat":float(tweet.lat), "lng":float(tweet.lng), "polarity":float(tweet.polarity)})

	if '3883' in socket.gethostname():
		with open("/root/TwitterSentiment/map.json", "w+") as output_file:
			json.dump(dictionary, output_file)
	else:
		with open("map.json", "w+") as output_file:
			json.dump(dictionary, output_file)

if __name__ == "__main__":
	main()