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
				t['polarity'].append(polarity)
				in_dictionary = True
				break
		if not in_dictionary:
			self.dictionary.append(
					{
						"lat":lat,
						"lng":lng,
						"polarity":[polarity],
						"count":1
					}
				)

	def calculate_polarity(self):
		"""
		Calculate average polarity
		"""
		for t in self.dictionary:
			tot_polarity = sum(t['polarity'])
			t['polarity'] = tot_polarity / t['count']

	def run(self):
		"""
		Saves entities to json file
		"""
		for tag in self.get_hashtags():
			print "Tag: %s" %(tag)
			for t in self.get_tweets(tag):
				self.insert_to_dictonary(
						round(float(t.lat), 1),
						round(float(t.lng), 1),
						float(t.polarity),
					)

		self.calculate_polarity()
		self.dump_to_file()

	def set_filename(self):
		"""
		Sets filename depending on host
		"""
		if '3883' in socket.gethostname():
			self.filename = "/root/TwitterSentiment/map.json"
		else:
			self.filename = "map.json"

	def get_tweets(self, hashtag):
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