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
        params["t"] = search_term
        r = requests.get(base_url, params=params)
        response = json.loads(r.text)

        CACHE_DICTION["OMDB"][search_term] = response
        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()
    return response






#Define the Movie class here
class Movie(object):
    #Define the instance variables, title, director, imdb rating, languages and actors here

    #Constructor here
    def __init__(self, structured_data):
        self.title = structured_data["Title"]
        self.director = structured_data["Director"]
        self.imdb_rating = structured_data["imdbRating"]
        self.languages = structured_data["Language"]
        self.actors = [actor for actor in structured_data["Actors"].split(",")]
        return

    #Implement the __str__ class method, it takes no input and returns a readable Movie string
    def __str__(self):
        return(self.title + ", directed by " + self.director)

    #Implement get_actors class method, it takes an integer input and returns that many actors
    def get_actors(self, num_actors = 1):
        actors_returned = []
        for index, actor in enumerate(self.actors):
            if index == num_actors:
                break
            actors_returned.append(actor)
        return actors_returned


#TODO define these classes below
#Define the Tweet class here, the variables and methods are still to be determined
class Tweet(object):
    def __init__(self):
        return


#Define the TwitterUser class here, the variables and methods are still to be determined
class TwitterUser(object):
    def __init__(self):
        return





#Create variable movie_search_terms to to store 3 strings of movies to search for using the get_OMDB_data function above
movie_search_terms = ["The Dark Knight", "Captain America: Civil War", "The Big Short"]

#Create a list of dictionaries called movie_info containing movie data from the movie_search_terms movies, List Comprehension
movie_info = [get_OMDB_data(movie) for movie in movie_search_terms]

#Create a list of instances of the class Movie using the movie_info list
movie_instance_list = [Movie(structured_data) for structured_data in movie_info]

#Create a list of the top paid actor from each of the movies called top_actors, list comprehension
top_actors = [dictionary['Actors'].split(",")[0] for dictionary in movie_info]

#Create a dictionary called top_actor_tweets containing movie data from the movie_search_terms movies
top_actor_tweets = {}
for actor in top_actors:
        top_actor_tweets[actor] = get_twitter_search_data(actor)

#print(top_actor_tweets["Christian Bale"]["statuses"][:5])

#Create a list of users that are mentioned in any of the tweets in top_actor_tweets called neighborhood_users
neighborhood_users = []
for actor in top_actors:
        for status in top_actor_tweets[actor]["statuses"]:
                neighborhood_users.append(status['user']['id_str'])

#Get twitter data about all neighborhood_users and store in a list variable called user_data
user_data = []
for user in neighborhood_users:
        user_data.append(get_twitter_user_data(user))




#Start database implementation here
#Setup the connection and drop tables Tweets, Users, and Movies if they exist
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

dropStatement = 'DROP TABLE IF EXISTS Tweets'
cur.execute(dropStatement)
dropStatement = 'DROP TABLE IF EXISTS Movies'
cur.execute(dropStatement)
dropStatement = 'DROP TABLE IF EXISTS Users'
cur.execute(dropStatement)

#CREATE TABLE Users
#Properties: user_id(primary key), screen_name, num_favorites_made, desciption
createStatement = 'CREATE TABLE IF NOT EXISTS Users '
createStatement += '(user_id TEXT PRIMARY KEY, '
createStatement += 'screen_name TEXT, '
createStatement += 'num_favorites_made INTEGER, '
createStatement += 'description TEXT)'
cur.execute(createStatement)

#CREATE TABLE Movies
#Properties: movie_id(primary key), title, director, num_languages, imdb_rating, top_billed_actor
createStatement = 'CREATE TABLE IF NOT EXISTS Movies '
createStatement += '(movie_id TEXT PRIMARY KEY, '
createStatement += 'title TEXT, '
createStatement += 'director INTEGER, '
createStatement += 'num_languages INTEGER, '
createStatement += 'imdb_rating REAL, '
createStatement += 'top_billed_actor TEXT)'
cur.execute(createStatement)

#CREATE TABLE Tweets
#Properties: text, tweet_id(primary key), user_id, movie_id, num_favorites, num_retweets
createStatement = 'CREATE TABLE IF NOT EXISTS Tweets '
createStatement += '(text TEXT, '
createStatement += 'tweet_id TEXT PRIMARY KEY, '
createStatement += 'user_id TEXT, '
createStatement += 'movie_id INTEGER, '
createStatement += 'num_favorites INTEGER, '
createStatement += 'num_retweets INTEGER, '
createStatement += 'FOREIGN KEY (user_id) REFERENCES Users(user_id),'
createStatement += 'FOREIGN KEY (movie_id) REFERENCES Movies(user_id))'
cur.execute(createStatement)

conn.commit()
#Load data into Users database from the user_data variable defined earlier, user_id will be the primary key
for user in user_data:
    select_sql = "SELECT * FROM Users WHERE user_id = ?"
    cur.execute(select_sql, (user["id_str"],))
    if not cur.fetchone():
        info = []
        insertStatement = 'INSERT INTO Users VALUES (?, ?, ?, ?)'
        info.append(user["id_str"])
        info.append(user["screen_name"])
        info.append(user["favourites_count"])
        info.append(user["description"])
        cur.execute(insertStatement, info)
        conn.commit()

#Load data into Tweets database

#Load data into Movies database



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
    structured_data = get_OMDB_data("the dark knight rises")
    def test_movie_title(self):
        movie = Movie(self.structured_data)
        self.assertEqual(movie.title, "The Dark Knight Rises")
    def test_movie_actors(self):
        movie = Movie(self.structured_data)
        self.assertEqual(type(movie.actors), type(["actor1", "actor2"]))
    def test_movie_get_actors(self):
        movie = Movie(self.structured_data)
        self.assertEqual(movie.get_actors(1), ["Christian Bale"])
    def test_movie_str(self):
        movie = Movie(self.structured_data)
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
        self.assertEqual(len(result[0]), 4)
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
