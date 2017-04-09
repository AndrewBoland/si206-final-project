## Your name: Andrew Boland
## The option you've chosen: Option 2

# Put import statements you expect to need here!
import unittest
import itertools
import collections
import requests
import tweepy
import twitter_info
import json
import sqlite3


# Write your test cases here.
class MovieTests(unittest.TestCase):
    base_url = "http://www.omdbapi.com/"
    params = {}
    params["t"] = "the dark knight rises"
    r = requests.get(base_url, params=params)
    structured_data = json.loads(r.text)
    def test_movie_title(self):
        movie = Movie(structured_data)
        self.assertEqual(movie.title, "The Dark Knight Rises")
    def test_movie_actors(self):
        movie = Movie(structured_data)
        self.assertEqual(type(movie.authors), type(["author1", "author2"]))
    def test_movie_get_actors(self):
        movie = Movie(structured_data)
        self.assertEqual(movie.get_actors(1), "Christian Bale")
    def test_movie_str(self):
        movie = Movie(structured_data)
        self.assertEqual(movie.__str__(), "The Dark Knight Rises, directed by Christopher Nolan")

class DatabaseTests(unittest.TestCase):
    def test_movie_db_columns(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Movies')
        result = cur.fetchall()
        self.assertEqual(len(result[0]), 6)
        conn.close()
    def test_users_db_columns(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users')
        result = cur.fetchall()
        self.assertEqual(len(result[0]), 3)
        conn.close()
    def test_tweets_db_columns(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Tweets')
        result = cur.fetchall()
        self.assertEqual(len(result[0]), 6)
        conn.close()

class ResultsTests(unittest.TestCase):
    def test_user_tweet_dict(self):
        self.assertEqual(type(user_tweet_dict), type({"uid":["tweet", "tweet"], "uid":["tweet", "tweet"]}) )


## Remember to invoke all your tests...
if __name__ == "__main__":
    unittest.main(verbosity=2)
