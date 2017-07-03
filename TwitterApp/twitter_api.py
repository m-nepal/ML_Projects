# From tweepy's examples
# https://github.com/tweepy/tweepy/blob/master/examples/streaming.py

from tweepy.streaming import StreamListener
import json
import tweepy

consumer_key = "yD8HPKtfdHpMKVyfrYtjcJhih"
consumer_secret = "o5ZiidfbuRt9i1tnOvAUPbjfzlvzMCzDYs9m92k80tIwc2eL4z"

access_token = "151019558-pGUFmAHM6ZZrHK4g2GEv7Vk2DCmlt1FJfeD23HF9"
access_token_secret = "Ek8gONd27KJF6nYWz3AMtNhB0KWJCVd4BUZqUYK4Uouab"

class twitter_stream_listener(StreamListener):
    """A listener that handles tweets received from the stream
    Basic listener that prints received tweets
    """

    def __init__(self, num_tweets=10):
        self.counter = 0
        self.num_tweets = num_tweets

    # Tells tweepy what to do when a new tweet is available
    def on_data(self, data):
        try:
            j = json.loads(data)
            print("New Tweet")
            print(j["text"])
            self.counter += 1
            if self.counter == self.num_tweets:
                return False # causes the class to exit
            else:
                return True # continues to look for a new tweet
        except:
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
    twitter_api = tweepy.API(auth)
    search_results = tweepy.Cursor(twitter_api.search, q="wimbledon").items(20)
    for result in search_results:
        print(result.text)

    # Trends
    trends = twitter_api.trends_place(1) #Global trends

    for trend in trends[0]["trends"]:
        print(trend['name'])
