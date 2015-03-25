from datetime import datetime

def convertToDate(timestring):
	return datetime.strptime(
			"2015 %s" %(timestring),
			"%Y %d/%m %H:%M"
		)

def getNumberOfTweets(line):
	line = line.replace(
			"INFO Searched through ",
			""
		).replace(
			" tweets",
			""
		)
	return int(line)

class Reading(object):
	def __init__(self, time, tweets):
		self.time = time
		self.tweets = tweets
		self.start, self.end = False, False

	def isStart(self):
		self.start = True

	def isEnd(self):
		self.end = True

class Reader(object):
	def __init__(self):
		self.readings = []

	def findStartsAndEnds(self):
		temp = None
		for r in self.readings:
			if r.tweets == 10000:
				r.isStart()
				if temp:
					temp.isEnd()
			temp = r
		if temp:
			temp.isEnd()

	def calculateFrequency(self):
		self.intervals = []
		temp = {}
		for r in self.readings:
			if r.start:
				temp['start'] = r.time
			elif r.end:
				temp['end'] = r.time
				temp['duration'] = (temp['end'] - temp['start']).total_seconds()
				temp['tweets'] = r.tweets
				self.intervals.append(temp)
				temp = {}
		if temp != {}:
			self.intervals.append(temp)

	def display(self):
		total_tweets, total_duration = 0, 0
		tweets_per_second, tweets_per_hour, tweets_per_minute, tweets_per_day = 0, 0, 0, 0
		for l in self.intervals:
			total_tweets += l['tweets']
			total_duration += l['duration']

		tweets_per_second = total_tweets / float(total_duration)
		tweets_per_minute = tweets_per_second * 60.0
		tweets_per_hour = tweets_per_minute * 60.0
		tweets_per_day = tweets_per_hour * 24.0

		print "%15s%15s%15s%15s%15s%15s" %("Total", "Duration (s)", "t/s", "t/m", "t/h", "t/d")
		print "%15s%15s%15s%15s%15s%15s" %(
				total_tweets,
				total_duration,
				round(tweets_per_second, 1),
				round(tweets_per_minute, 1),
				round(tweets_per_hour, 1),
				round(tweets_per_day, 1),
			)

	def getDataFromLog(self):
		for date, tweets in self.getLines():
			self.readings.append(
					Reading(date, tweets)
				)

	def getLines(self):
		for line in self.getLog():
			if "Searched through" in line:
				date = convertToDate(line.split(": ")[0])
				tweets = getNumberOfTweets(line.split(": ")[-1])
				yield date, tweets

	def getLog(self):
		with open('logger.log', 'r') as f:
			return [l for l in f.readlines()]

if __name__ == "__main__":
	reader = Reader()
	reader.getDataFromLog()
	reader.findStartsAndEnds()
	reader.calculateFrequency()
	reader.display()