# From tweepy's examples
# https://github.com/tweepy/tweepy/blob/master/examples/streaming.py

from tweepy.streaming import StreamListener
import json
import tweepy
from collections import Counter
import sqlite3

consumer_key = "yD8HPKtfdHpMKVyfrYtjcJhih"
consumer_secret = "o5ZiidfbuRt9i1tnOvAUPbjfzlvzMCzDYs9m92k80tIwc2eL4z"

access_token = "151019558-pGUFmAHM6ZZrHK4g2GEv7Vk2DCmlt1FJfeD23HF9"
access_token_secret = "Ek8gONd27KJF6nYWz3AMtNhB0KWJCVd4BUZqUYK4Uouab"

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}
db = "db/twitter_db_temp.db"

class stats():
    def __init__(self):
        self.lang = []
        self.top_lang = []
        self.top_tweets = []

    def add_lang(self, lang):
        self.lang.append(lang)

    def add_top_lang(self, top_lang):
        self.top_lang.append(top_lang)

    def add_top_tweets(self, tweet_html):
        self.top_tweets.append(tweet_html)

    def get_stats(self):
        return self.lang, self.top_lang, self.top_tweets

class twitter_stream_listener(StreamListener):
    """A listener that handles tweets received from the stream
    Basic listener that prints received tweets
    """

    def __init__(self, num_tweets, retweet_count, stats, get_tweet_html):
        self.counter = 0
        self.num_tweets = num_tweets # Numbber of tweets
        self.languages = [] #language of the tweet
        self.retweet_count = retweet_count
        self.top_languages = []
        self.stats = stats
        self.get_tweet_html = get_tweet_html

    # Tells tweepy what to do when a new tweet is available
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            retweet_count = json_data["retweeted_status"]["retweet_count"]
            self.stats.add_lang(langs[json_data["lang"]])

            # Top tweets
            if retweet_count >= self.retweet_count:
                # print(json_data["text"], retweet_count, langs[json_data["lang"]])
                self.stats.add_top_tweets(self.get_tweet_html(json_data['id']))
                self.stats.add_top_lang(langs[json_data["lang"]])

            self.counter += 1
            if self.counter == self.num_tweets:
                return False # causes the class to exit
            else:
                return True # continues to look for a new tweet
        except:
            # @TODO: come back to this
            pass

    # Prints the status if an error occurs
    def on_error(self, status_code):
        print(status_code)

class twitterMain():
    def __init__(self, num_tweets, retweet_count, sql_conn):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.twitter_api = tweepy.API(self.auth)
        self.num_tweets = num_tweets
        self.retweet_count = retweet_count
        self.stats = stats()
        self.sql_conn = sql_conn
        self.c = self.sql_conn.cursor()

    def get_streaming_data(self, search_keywords):
        listener = twitter_stream_listener(self.num_tweets, self.retweet_count, self.stats, self.get_tweet_html)
        stream = tweepy.Stream(self.auth, listener)
        stream.filter(track=search_keywords)

        lang, top_lang, top_tweets = self.stats.get_stats()

        # print(Counter(lang))
        # print(Counter(top_lang))
        # print(top_tweets)

        self.c.execute("INSERT INTO lang_data VALUES (?,?, DATETIME('now'))",
                       (str(list(Counter(lang).items())), str(list(Counter(top_lang).items()))))

        for t in top_tweets:
            self.c.execute("INSERT INTO twit_data VALUES (?, DATETIME('now'))", (t, ))

        self.sql_conn.commit()

    def get_trends(self):
        trends = self.twitter_api.trends_place(23424977)
        trend_data = []

        for trend in trends[0]["trends"]:
            trend_tweets = []
            trend_tweets.append(trend['name'])
            tt = tweepy.Cursor(self.twitter_api.search, q = trend['name']).items(3)

            for t in tt:
                trend_tweets.append(self.get_tweet_html(t.id))

            trend_data.append(tuple(trend_tweets))
        print("Inserting trend data into SQL")
        self.c.executemany("INSERT INTO trend_data VALUES (?,?,?,?, DATETIME('now'))", (trend_data, ))
        self.sql_conn.commit()

    def get_tweet_html(self, id):
        oembed = self.twitter_api.get_oembed(id=id, hide_media=True, hide_thread=True)
        tweet_html = oembed['html'].strip("\n")

        return tweet_html


if __name__=='__main__':
    num_tweets = 20
    retweet_count = 100

    try:
        conn = sqlite3.connect(db)
        tw = twitterMain(num_tweets, retweet_count, conn)
        tw.get_streaming_data(search_keywords=['Wimbledon'])
        tw.get_trends()
    except Exception as e:
        print(e.__doc__)
    finally:
        conn.close()
