import db
from data.models import Tweet
import json

def main():
	dictionary = []
	for tweet in Tweet.objects.all():
		dictionary.append({"lat":float(tweet.lat), "lng":float(tweet.lng), "polarity":float(tweet.polarity)})

	with open("map.json", "w+") as output_file:
		json.dump(dictionary, output_file)

if __name__ == "__main__":
	main()