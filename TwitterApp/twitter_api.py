# From tweepy's examples
# https://github.com/tweepy/tweepy/blob/master/examples/streaming.py

from tweepy.streaming import StreamListener
import json
import tweepy
from collections import Counter

consumer_key = "yD8HPKtfdHpMKVyfrYtjcJhih"
consumer_secret = "o5ZiidfbuRt9i1tnOvAUPbjfzlvzMCzDYs9m92k80tIwc2eL4z"

access_token = "151019558-pGUFmAHM6ZZrHK4g2GEv7Vk2DCmlt1FJfeD23HF9"
access_token_secret = "Ek8gONd27KJF6nYWz3AMtNhB0KWJCVd4BUZqUYK4Uouab"

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}

class twitter_stream_listener(StreamListener):
    """A listener that handles tweets received from the stream
    Basic listener that prints received tweets
    """

    def __init__(self, num_tweets=10, retweet_count=10000):
        self.counter = 0
        self.num_tweets = num_tweets # Numbber of tweets
        self.languages = [] #language of the tweet
        self.retweet_count = retweet_count
        self.top_languages = []

    # Tells tweepy what to do when a new tweet is available
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            retweet_count = json_data["retweeted_status"]["retweet_count"]

            # Top tweets
            if retweet_count >= self.retweet_count:
                print(json_data["text"], retweet_count, langs[json_data["lang"]])
                self.top_languages.append(langs[json_data["lang"]])

            self.languages.append(langs[json_data["lang"]])
            self.counter += 1
            if self.counter == self.num_tweets:
                print(json_data)
                print(self.languages)
                print(Counter(self.languages))
                return False # causes the class to exit
            else:
                return True # continues to look for a new tweet
        except:
            # @TODO: come back to this
            pass

    # Prints the status if an error occurs
    def on_error(self, status_code):
        print(status_code)

if __name__=='__main__':
    listener = twitter_stream_listener(num_tweets=20)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['wimbledon'])

    # Search for a given query
    # twitter_api = tweepy.API(auth)
    # search_results = tweepy.Cursor(twitter_api.search, q="wimbledon").items(20)
    # for result in search_results:
    #     print(result.text)
    #
    # # Trends
    # trends = twitter_api.trends_place(1) #Global trends
    #
    # for trend in trends[0]["trends"]:
    #     print(trend['name'])
