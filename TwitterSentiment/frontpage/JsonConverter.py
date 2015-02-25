from TwitterSentiment.scraper.models import Tweet


class JsonConverter(object):
    @staticmethod

    def insert_to_dictonary(lat, lng, polarity, dictionary):
        """
        Insert tweet into dictionary

        :param lat: latitude
        :param lng: longtitude
        :param polarity: polarity
        """
        in_dictionary = False
        for t in dictionary:
            if t['lat'] == lat and t['lng'] == lng:
                t['count'] += 1
                t['polarity'].append(polarity)
                in_dictionary = True
                break
        if not in_dictionary:
            dictionary.append(
                {
                "lat": lat,
                "lng": lng,
                "polarity": [polarity],
                "count": 1
                }
            )


    @staticmethod
    def calculate_polarity(dictionary):
        """
        Calculate average polarity
        """
        for t in dictionary:
            tot_polarity = sum(t['polarity'])
            t['polarity'] = tot_polarity / t['count']


    @staticmethod
    def get_tweets(hashtag):
        """
        Returns tweets for hashtag
        """
        return Tweet.objects.filter(hashtag=hashtag)


    @staticmethod
    def searchHashtags(hashtags):
        dictionary = {}

        for t in JsonConverter.get_tweets(hashtags):
            JsonConverter.insert_to_dictonary(
                round(float(t.lat), 0),
                round(float(t.lng), 0),
                float(t.polarity),
                dictionary
            )

        JsonConverter.calculate_polarity(dictionary)
        return dictionary

