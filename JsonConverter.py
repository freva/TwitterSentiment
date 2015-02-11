import db
from data.models import Tweet
import json
import socket

class JsonConverter(object):
	def __init__(self):
		"""
		Configure the converter.
		"""
		self.set_filename()
		self.dictionary = []

	def insert_to_dictonary(self, lat, lng, polarity):
		"""
		Insert tweet into dictionary

		:param lat: latitude
		:param lng: longtitude
		:param polarity: polarity
		"""
		in_dictionary = False
		for t in self.dictionary:
			if t['lat'] == lat and t['lng'] == lng:
				t['count'] += 1
				in_dictionary = True
				break
		if not in_dictionary:
			self.dictionary.append(
					{
						"lat":lat,
						"lng":lng,
						"polarity":polarity,
						"count":1
					}
				)

	def run(self):
		"""
		Saves entities to json file
		"""
		for tag in self.get_hashtags():
			for tweet in self.get_tweets(tag):
				self.insert_to_dictonary(
						round(float(tweet.lat), 1),
						round(float(tweet.lng), 1),
						float(tweet.polarity),
					)

		self.dump_to_file()

	def set_filename(self):
		"""
		Sets filename depending on host
		"""
		if '3883' in socket.gethostname():
			self.filename = "/root/TwitterSentiment/map.json"
		else:
			self.filename = "map.json"

	def get_tweets(hashtag):
		"""
		Returns tweets for hashtag
		"""
		return Tweet.objects.filter(hashtag=hashtag)

	def get_hashtags(self):
		"""
		Generator returning hashtags
		"""
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
		for h in hashtags:
			yield h

	def dump_to_file(self):
		"""
		Writes the dictionary to json file
		"""
		with open(self.filename, "w+") as output_file:
			json.dump(self.dictionary, output_file)

def main():
	"""
	Main function
	"""
	worker = JsonConverter()
	worker.run()

if __name__ == "__main__":
	main()