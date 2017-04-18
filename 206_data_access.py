###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest
import itertools
import collections
import requests
import tweepy
import twitter_info
import json
import sqlite3

# Begin filling in instructions....

#Tweepy setup
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


#Set up the caching structure here and define a cache file name variable
#Taken from my project 3 code
CACHE_FNAME = "SI206_final_project_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}
	CACHE_DICTION["OMDB"] = {}
	CACHE_DICTION["Twitter"] = {}
	CACHE_DICTION["Twitter"]["Search"] = {}
	CACHE_DICTION["Twitter"]["User"] = {}

#Write two functions to get and cache data from twitter
def get_twitter_search_data(search_term):
    if search_term in CACHE_DICTION["Twitter"]["Search"]:
        response = CACHE_DICTION["Twitter"]["Search"][search_term]
    else:
        response = api.search(search_term)
        CACHE_DICTION["Twitter"]["Search"][search_term] = response

        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()
    return response

def get_twitter_user_data(user):
    if user in CACHE_DICTION["Twitter"]["User"]:
        response = CACHE_DICTION["Twitter"]["User"][user]
    else:
        response = api.get_user(user)
        CACHE_DICTION["Twitter"]["User"][user] = response

        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()
    return response



#Write a function to get and cache data from OMDB
def get_OMDB_data(search_term):
    if search_term in CACHE_DICTION["OMDB"]:
        response = CACHE_DICTION["OMDB"][search_term]
    else:
        base_url = "http://www.omdbapi.com/"
        params = {}
        params["t"] = "the dark knight rises"
        r = requests.get(base_url, params=params)
        response = json.loads(r.text)

        CACHE_DICTION["OMDB"][search_term] = response
        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()
    return response


#TODO write code to invoke each of the above functions and put info into a variable





#Define the Movie class here

    #Constructor here

    #Define the instance variables, title, director, imdb rating, languages and actors here

#Define the Tweet class here

#Define the TwitterUser class here





#Define the Movie class here

    #Define the instance variables, title, director and actors here

    #Implement the __str__ class method, it takes no input and returns a readable Movie string

    #Implement get_actors class method, it takes an integer input and returns that many actors





#Make list of movie search terms and put into a variable





#Make requests to OMDB and store in a list





#Make invocations to twitter functions





# TODO all database stuff below
#Start database implementation here

    #Setup the connection

    #CREATE TABLE Tweets

    #CREATE TABLE Users

    #CREATE TABLE Movies

    #TODO load data with useful info and primary key
    #Load data into all databases




#Define variable to store a list of users queried from the database (List Comprehension)

#Define a dictionary to store user, list of tweet pairs (Dictionary Comprehension)





#Output all gained information into a text file

    #Movie searched for with highest rating

    #User with the most retweeted tweet from a movie




#Close the database connection here
conn.commit()
conn.close()







# Put your tests here, with any edits you now need from when you turned them in with your project plan.

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

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
    unittest.main(verbosity=2)
